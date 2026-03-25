# Quick Start Guide - Knowledge Feedback Loop

## Prerequisites
- Python 3.11+ installed
- Node.js 18+ installed
- Backend virtual environment set up
- Frontend dependencies installed

## Step 1: Initialize Database

**Linux/Mac:**
```bash
cd backend
python create_feedback_table.py
```

**Windows:**
```powershell
cd backend
venv\Scripts\python.exe create_feedback_table.py
```

Expected output:
```
[OK] knowledge_feedbacks table created successfully
[OK] Table verification successful
```

## Step 2: Start Backend Server

**Linux/Mac:**
```bash
cd backend
source venv/bin/activate
python main.py
```

**Windows:**
```powershell
cd backend
venv\Scripts\activate
python main.py
```

Server will start at: `http://localhost:8000`

## Step 3: Start Frontend

```bash
cd frontend
npm run dev
```

Frontend will start at: `http://localhost:3000`

## Step 4: Test the Feature

### A. Submit Feedback from Chat

1. Open `http://localhost:3000`
2. Ask a question: "Giá phanh trước SH 2023?"
3. Wait for AI response
4. Click "Góp ý / Cập nhật" button below the response
5. Fill in the corrected knowledge
6. Click "Gửi góp ý"

### B. Review Feedback as Manager

1. Open `http://localhost:3000/admin/knowledge-review`
2. You'll see the pending feedback
3. Click "Phê duyệt" or "Từ chối"
4. Fill in reviewer name and optional notes
5. Confirm the action

### C. Verify Vector DB Update

After approving feedback:
1. Go back to chat
2. Ask the same question again
3. The AI should now incorporate the new knowledge in its response

## Step 5: Run Integration Tests (Optional)

```bash
cd backend
python test_knowledge_feedback.py
```

This will run all API endpoint tests automatically.

## Quick Commands Reference

### Backend

**Linux/Mac:**
```bash
# Create database table
python create_feedback_table.py

# Start server (with venv activated)
source venv/bin/activate
python main.py

# Run tests
python test_knowledge_feedback.py
```

**Windows:**
```powershell
# Create database table
venv\Scripts\python.exe create_feedback_table.py

# Start server
venv\Scripts\activate
python main.py

# Run tests
python test_knowledge_feedback.py
```

### Frontend
```bash
# Install dependencies (first time only)
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

## API Endpoints Quick Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/knowledge/feedback` | Submit new feedback |
| GET | `/api/admin/knowledge/pending?status=pending` | Get pending feedbacks |
| POST | `/api/admin/knowledge/{id}/approve` | Approve feedback |
| POST | `/api/admin/knowledge/{id}/reject` | Reject feedback |

## Troubleshooting

### Backend won't start
- Check if port 8000 is available
- Verify virtual environment is activated
- Check all dependencies are installed: `pip install -r requirements.txt`

### Frontend won't start
- Check if port 3000 is available
- Run `npm install` to ensure all dependencies are installed
- Clear `.next` folder and restart:
  - Linux/Mac: `rm -rf .next && npm run dev`
  - Windows: `rmdir /s .next` then `npm run dev`

### Database errors
- Make sure `backend/database/store.db` exists
- Run migration script again: `python create_feedback_table.py`
- Check file permissions

### CORS errors
- Ensure backend is running
- Check backend CORS settings in `main.py`
- Verify frontend is making requests to correct URL

## Next Steps

For detailed implementation information, see:
- [KNOWLEDGE_FEEDBACK_IMPLEMENTATION.md](KNOWLEDGE_FEEDBACK_IMPLEMENTATION.md)

For production deployment:
- Add authentication/authorization
- Configure production database
- Set up environment variables
- Enable HTTPS
- Configure proper CORS origins
