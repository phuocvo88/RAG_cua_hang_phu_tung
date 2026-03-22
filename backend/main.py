from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import os
import sqlite3
from dotenv import load_dotenv

# Import RAG Engine (sẽ viết sau)
from rag_engine import query_rag_system, add_knowledge_to_vector_db

load_dotenv()

app = FastAPI(title="RAG Chatbot Cửa Hàng Phụ Tùng", version="1.0.0")

# CORS config cho Frontend (Next.js)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Trong thực tế nên để localhost:3000
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str
    source: str = "Tư vấn tổng hợp"

# Knowledge Feedback Models
class FeedbackSubmitRequest(BaseModel):
    user_query: str
    ai_response: str
    corrected_knowledge: str
    submitted_by: Optional[str] = "Staff"

class FeedbackItem(BaseModel):
    id: int
    user_query: str
    ai_response: str
    corrected_knowledge: str
    submitted_by: str
    status: str
    created_at: str
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[str] = None
    notes: Optional[str] = None

class FeedbackActionRequest(BaseModel):
    reviewed_by: str
    notes: Optional[str] = None

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Backend API đang hoạt động."}

@app.post("/api/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    user_message = request.message

    # Gọi RAG engine ở đây
    try:
        reply = query_rag_system(user_message)
    except Exception as e:
        reply = f"Lỗi truy vấn AI hoặc chưa cấu hình API Key: {e}"

    return ChatResponse(reply=reply)

# ==========================================
# KNOWLEDGE FEEDBACK ENDPOINTS
# ==========================================

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect('./database/store.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.post("/api/knowledge/feedback")
def submit_feedback(request: FeedbackSubmitRequest):
    """Staff submits knowledge correction/feedback"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO knowledge_feedbacks
            (user_query, ai_response, corrected_knowledge, submitted_by, status)
            VALUES (?, ?, ?, ?, 'pending')
        ''', (
            request.user_query,
            request.ai_response,
            request.corrected_knowledge,
            request.submitted_by
        ))

        conn.commit()
        feedback_id = cursor.lastrowid
        conn.close()

        return {
            "success": True,
            "message": "Góp ý đã được gửi thành công",
            "feedback_id": feedback_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi lưu góp ý: {str(e)}")

@app.get("/api/admin/knowledge/pending", response_model=List[FeedbackItem])
def get_pending_feedbacks(status: Optional[str] = "pending"):
    """Get list of pending feedback items for admin review"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, user_query, ai_response, corrected_knowledge,
                   submitted_by, status, created_at, reviewed_by, reviewed_at, notes
            FROM knowledge_feedbacks
            WHERE status = ?
            ORDER BY created_at DESC
        ''', (status,))

        rows = cursor.fetchall()
        conn.close()

        feedbacks = []
        for row in rows:
            feedbacks.append(FeedbackItem(
                id=row['id'],
                user_query=row['user_query'],
                ai_response=row['ai_response'],
                corrected_knowledge=row['corrected_knowledge'],
                submitted_by=row['submitted_by'],
                status=row['status'],
                created_at=row['created_at'],
                reviewed_by=row['reviewed_by'],
                reviewed_at=row['reviewed_at'],
                notes=row['notes']
            ))

        return feedbacks
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi lấy danh sách góp ý: {str(e)}")

@app.post("/api/admin/knowledge/{feedback_id}/approve")
def approve_feedback(feedback_id: int, request: FeedbackActionRequest):
    """Approve feedback and add knowledge to Vector DB"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Get feedback details
        cursor.execute('''
            SELECT corrected_knowledge FROM knowledge_feedbacks
            WHERE id = ? AND status = 'pending'
        ''', (feedback_id,))

        row = cursor.fetchone()
        if not row:
            conn.close()
            raise HTTPException(status_code=404, detail="Góp ý không tồn tại hoặc đã được xử lý")

        corrected_knowledge = row['corrected_knowledge']

        # Update feedback status
        cursor.execute('''
            UPDATE knowledge_feedbacks
            SET status = 'approved',
                reviewed_by = ?,
                reviewed_at = CURRENT_TIMESTAMP,
                notes = ?
            WHERE id = ?
        ''', (request.reviewed_by, request.notes, feedback_id))

        conn.commit()
        conn.close()

        # Add knowledge to Vector DB
        try:
            add_knowledge_to_vector_db(corrected_knowledge)
        except Exception as e:
            # Rollback status if vector DB update fails
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE knowledge_feedbacks
                SET status = 'pending', reviewed_by = NULL, reviewed_at = NULL
                WHERE id = ?
            ''', (feedback_id,))
            conn.commit()
            conn.close()
            raise HTTPException(status_code=500, detail=f"Lỗi khi cập nhật Vector DB: {str(e)}")

        return {
            "success": True,
            "message": "Góp ý đã được phê duyệt và thêm vào hệ thống",
            "feedback_id": feedback_id
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi phê duyệt góp ý: {str(e)}")

@app.post("/api/admin/knowledge/{feedback_id}/reject")
def reject_feedback(feedback_id: int, request: FeedbackActionRequest):
    """Reject feedback"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if feedback exists and is pending
        cursor.execute('''
            SELECT id FROM knowledge_feedbacks
            WHERE id = ? AND status = 'pending'
        ''', (feedback_id,))

        row = cursor.fetchone()
        if not row:
            conn.close()
            raise HTTPException(status_code=404, detail="Góp ý không tồn tại hoặc đã được xử lý")

        # Update feedback status
        cursor.execute('''
            UPDATE knowledge_feedbacks
            SET status = 'rejected',
                reviewed_by = ?,
                reviewed_at = CURRENT_TIMESTAMP,
                notes = ?
            WHERE id = ?
        ''', (request.reviewed_by, request.notes, feedback_id))

        conn.commit()
        conn.close()

        return {
            "success": True,
            "message": "Góp ý đã được từ chối",
            "feedback_id": feedback_id
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi từ chối góp ý: {str(e)}")

# ==========================================
# RUN SERVER
# ==========================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
