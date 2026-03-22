# Knowledge Feedback Loop - Implementation Guide

## Overview
This document describes the complete implementation of the Knowledge Feedback Loop feature for the RAG-based auto parts store chatbot system.

## Architecture

### Workflow
1. **Staff submits feedback** → User interacts with chatbot and finds incorrect/incomplete information
2. **Click "Góp ý / Cập nhật"** → Opens feedback modal
3. **Submit corrected knowledge** → Saved to database with status "pending"
4. **Manager reviews** → Views pending feedbacks in admin dashboard
5. **Approve/Reject** → Manager makes decision
   - **If approved**: Knowledge is added to Vector Database
   - **If rejected**: Knowledge is discarded

---

## Backend Implementation

### 1. Database Schema

**Table: `knowledge_feedbacks`**

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PRIMARY KEY | Auto-increment ID |
| user_query | TEXT | Original user question |
| ai_response | TEXT | AI's response that was incorrect |
| corrected_knowledge | TEXT | Correct information provided by staff |
| submitted_by | TEXT | Name of staff member who submitted |
| status | TEXT | pending / approved / rejected |
| reviewed_by | TEXT | Name of manager who reviewed |
| created_at | TIMESTAMP | When feedback was submitted |
| reviewed_at | TIMESTAMP | When feedback was reviewed |
| notes | TEXT | Manager's notes on the decision |

**Created by:** `backend/create_feedback_table.py`

### 2. API Endpoints

#### POST /api/knowledge/feedback
Submit new feedback from staff

**Request:**
```json
{
  "user_query": "Giá phanh trước SH 2023?",
  "ai_response": "Giá phanh trước SH 2023 là 450,000 VND",
  "corrected_knowledge": "Giá phanh trước SH 2023 là 520,000 VND. Mã SKU: SH23-BRK-FR, bảo hành 12 tháng.",
  "submitted_by": "Nhân viên A"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Góp ý đã được gửi thành công",
  "feedback_id": 1
}
```

#### GET /api/admin/knowledge/pending?status=pending
Get list of feedbacks by status (pending/approved/rejected)

**Response:**
```json
[
  {
    "id": 1,
    "user_query": "...",
    "ai_response": "...",
    "corrected_knowledge": "...",
    "submitted_by": "...",
    "status": "pending",
    "created_at": "2026-03-21 15:30:00",
    "reviewed_by": null,
    "reviewed_at": null,
    "notes": null
  }
]
```

#### POST /api/admin/knowledge/{id}/approve
Approve feedback and add to Vector DB

**Request:**
```json
{
  "reviewed_by": "Manager",
  "notes": "Đã xác minh với nhà cung cấp"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Góp ý đã được phê duyệt và thêm vào hệ thống",
  "feedback_id": 1
}
```

#### POST /api/admin/knowledge/{id}/reject
Reject feedback

**Request:**
```json
{
  "reviewed_by": "Manager",
  "notes": "Thông tin không chính xác"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Góp ý đã được từ chối",
  "feedback_id": 1
}
```

### 3. RAG Engine Updates

**Function: `add_knowledge_to_vector_db(knowledge_text: str)`**

Location: `backend/rag_engine.py`

This function:
1. Loads existing Vector DB index
2. Creates a new Document from the knowledge text
3. Inserts the document into the index
4. Persists the updated index back to storage

---

## Frontend Implementation

### 1. Chat Interface Updates (`frontend/src/app/page.tsx`)

**Added:**
- "Góp ý / Cập nhật" button on each bot message
- `userQuery` field in Message interface to track original question
- Click handler to open feedback modal

### 2. Feedback Modal Component

**Features:**
- Displays original user query
- Shows AI's response
- Text area for corrected knowledge
- Input for staff name
- Submit button with loading state
- Success message after submission

### 3. Admin Dashboard (`frontend/src/app/admin/knowledge-review/page.tsx`)

**Features:**
- Status filter tabs (Pending / Approved / Rejected)
- List of all feedbacks with detailed information
- Approve/Reject buttons for pending items
- Action modal for confirming decisions
- Real-time data refresh after actions

**Access:** `http://localhost:3000/admin/knowledge-review`

---

## Testing

### Automated Integration Tests

**File:** `backend/test_knowledge_feedback.py`

**Tests:**
1. Submit feedback
2. Get pending feedbacks
3. Approve feedback
4. Reject feedback
5. Get approved feedbacks
6. Get rejected feedbacks

**Run tests:**
```bash
cd backend
python test_knowledge_feedback.py
```

### Manual Testing Steps

1. **Start Backend:**
   ```bash
   cd backend
   venv/Scripts/python.exe main.py
   ```

2. **Start Frontend:**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Test Workflow:**
   - Open chat: `http://localhost:3000`
   - Ask a question (e.g., "Giá phanh SH 2023?")
   - Click "Góp ý / Cập nhật" on AI response
   - Fill in corrected knowledge
   - Submit feedback
   - Open admin dashboard: `http://localhost:3000/admin/knowledge-review`
   - Review and approve/reject the feedback
   - Verify status changes

---

## Files Modified/Created

### Backend
- ✅ `backend/create_feedback_table.py` - Database migration script
- ✅ `backend/main.py` - Added API endpoints
- ✅ `backend/rag_engine.py` - Added `add_knowledge_to_vector_db()` function
- ✅ `backend/test_knowledge_feedback.py` - Integration tests
- ✅ `backend/database/store.db` - Updated with new table

### Frontend
- ✅ `frontend/src/app/page.tsx` - Updated chat interface with feedback button and modal
- ✅ `frontend/src/app/admin/knowledge-review/page.tsx` - New admin dashboard page

### Documentation
- ✅ `KNOWLEDGE_FEEDBACK_IMPLEMENTATION.md` - This file

---

## Database Migration

If starting fresh or updating an existing database:

```bash
cd backend
venv/Scripts/python.exe create_feedback_table.py
```

This will create the `knowledge_feedbacks` table with proper schema and indexes.

---

## API Testing with curl

### Submit Feedback
```bash
curl -X POST http://localhost:8000/api/knowledge/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "user_query": "Test query",
    "ai_response": "Test response",
    "corrected_knowledge": "Correct info",
    "submitted_by": "Test Staff"
  }'
```

### Get Pending Feedbacks
```bash
curl http://localhost:8000/api/admin/knowledge/pending?status=pending
```

### Approve Feedback
```bash
curl -X POST http://localhost:8000/api/admin/knowledge/1/approve \
  -H "Content-Type: application/json" \
  -d '{
    "reviewed_by": "Manager",
    "notes": "Approved"
  }'
```

### Reject Feedback
```bash
curl -X POST http://localhost:8000/api/admin/knowledge/1/reject \
  -H "Content-Type: application/json" \
  -d '{
    "reviewed_by": "Manager",
    "notes": "Rejected"
  }'
```

---

## Security Considerations

### Current Implementation (Development)
- No authentication/authorization
- Open CORS policy
- Direct database access

### Production Recommendations
1. **Add Authentication:**
   - JWT tokens for API access
   - Role-based access control (Staff vs Manager)

2. **Secure CORS:**
   - Restrict origins to specific domains
   - Remove wildcard `*`

3. **Input Validation:**
   - Sanitize user inputs
   - SQL injection prevention (already using parameterized queries)

4. **Rate Limiting:**
   - Prevent API abuse
   - Limit feedback submissions per user

5. **Audit Logging:**
   - Log all approve/reject actions
   - Track who made what changes

---

## Future Enhancements

1. **Email Notifications:**
   - Notify managers when new feedback arrives
   - Notify staff when their feedback is approved/rejected

2. **Bulk Operations:**
   - Approve/reject multiple feedbacks at once
   - Export feedback data to CSV

3. **Analytics Dashboard:**
   - Track feedback submission trends
   - Identify common knowledge gaps
   - Monitor approval/rejection ratios

4. **Version Control:**
   - Track knowledge updates over time
   - Rollback capability for incorrect approvals

5. **Search and Filter:**
   - Search feedbacks by keywords
   - Filter by date range, submitter, reviewer

---

## Troubleshooting

### Issue: Feedback submission fails
- **Check:** Backend server is running
- **Check:** Database table exists (run migration script)
- **Check:** Network connection between frontend and backend

### Issue: Approve action fails
- **Check:** Vector DB storage path is accessible
- **Check:** Sufficient disk space
- **Check:** No permission issues on storage directory

### Issue: Admin dashboard shows no data
- **Check:** API endpoint is responding
- **Check:** CORS is properly configured
- **Check:** Browser console for errors

---

## Conclusion

The Knowledge Feedback Loop has been successfully implemented with:
- ✅ Complete backend API
- ✅ Interactive frontend UI
- ✅ Database schema
- ✅ Vector DB integration
- ✅ Integration tests
- ✅ Documentation

The system is ready for testing and can be deployed to production after implementing the recommended security enhancements.
