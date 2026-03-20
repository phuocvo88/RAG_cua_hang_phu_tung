from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Import RAG Engine (sẽ viết sau)
from rag_engine import query_rag_system

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
