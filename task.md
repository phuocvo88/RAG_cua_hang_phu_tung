# Knowledge Feedback Loop Implementation

## 1. Backend Modifications
- [ ] Create `knowledge_feedbacks` table in SQLite
- [ ] Create API Endpoint: `POST /api/knowledge/feedback` (Staff submits correction)
- [ ] Create API Endpoint: `GET /api/admin/knowledge/pending` (List pending for Manager)
- [ ] Create API Endpoint: `POST /api/admin/knowledge/{id}/approve` (Approve -> Insert to Vector DB)
- [ ] Create API Endpoint: `POST /api/admin/knowledge/{id}/reject` (Reject -> Discard)
- [ ] Update `rag_engine.py` to support adding new documents to Vector Database dynamically

## 2. Frontend Modifications (Next.js)
- [ ] Update Chat Interface: Add "Góp ý / Cập nhật" button on AI responses
- [ ] Create Feedback Modal: Form for staff to input correct knowledge
- [ ] Create Admin Dashboard Page: `/admin/knowledge-review`
- [ ] Implement Approve/Reject UI and connect to Admin APIs

## 3. Verification & Testing
- [ ] Write integration test for the feedback API
- [ ] Write integration test for approve/reject logic
- [ ] Manual test: Submit feedback from Chat UI -> See in Dashboard -> Approve -> Verify Vector DB is updated.
