# Goal Description
Triển khai tính năng **Kiểm duyệt kiến thức (Knowledge Feedback Loop)** để chống nhiễu loạn dữ liệu (Data Poisoning) cho hệ thống RAG. 
Khi AI trả lời sai thông tin về phụ tùng hoặc cách lắp ráp, nhân viên có thể gửi "Kiến thức đính chính". Các kiến thức này không được đưa ngay vào Vector Database mà sẽ lưu ở trạng thái "Chờ duyệt" (Pending). Người quản lý cửa hàng (Manager) sẽ có một trang Dashboard để xem xét, nếu đúng thì "Duyệt" (Approve) đưa vào Vector DB, nếu sai thì "Từ chối" (Reject).

## Proposed Changes

### 1. Database (SQLite)
Tạo thêm bảng `knowledge_feedbacks` để lưu trữ các đóng góp tạm thời.
- **Fields:** `id`, `original_query`, `ai_response`, `corrected_knowledge`, `status` (PENDING, APPROVED, REJECTED), `created_at`.

### 2. Backend (FastAPI)
#### Thêm các API Endpoints mới:
- `POST /api/knowledge/feedback`: Dành cho nhân viên Gửi feedback từ màn hình Chat. API này sẽ insert dữ liệu vào bảng `knowledge_feedbacks` với status `PENDING`.
- `GET /api/admin/knowledge/pending`: Lấy danh sách các feedback đang chờ duyệt.
- `POST /api/admin/knowledge/{id}/approve`: Quản lý duyệt -> Cập nhật status thành `APPROVED` -> **Insert `corrected_knowledge` vào LlamaIndex Vector DB**.
- `POST /api/admin/knowledge/{id}/reject`: Quản lý từ chối -> Cập nhật status thành `REJECTED`.

#### [MODIFY] `backend/rag_engine.py`
- Thêm hàm `add_knowledge_to_vector_db(text: str)` để hỗ trợ append thêm document mới vào index và lưu (persist) xuống đĩa.

#### [MODIFY] `backend/main.py`
- Đăng ký các API routing mới cho feedback và admin.

#### [MODIFY] `backend/database/store.db` (Schema)
- Tạo bảng `knowledge_feedbacks`.

---

### 3. Frontend (Next.js)
#### [MODIFY] Chat Interface (`src/components/MessageList.tsx`)
- Thêm nút "Báo sai / Cập nhật kiến thức" dưới mỗi câu trả lời của AI.
- Mở ra một Modal Form để nhân viên nhập kiến thức đúng và bấm Gửi.

#### [NEW] Admin Dashboard (`src/app/admin/knowledge-review/page.tsx`)
- Xây dựng giao diện bảng (Table) hiển thị các kiến thức đang `PENDING`.
- Hiển thị Câu hỏi của khách, Câu trả lời cũ của AI, và Kiến thức đính chính của nhân viên.
- Thêm 2 nút hành động: **[Duyệt]** (Màu xanh) và **[Từ chối]** (Màu đỏ).

## Verification Plan

### Automated Tests
- Viết kịch bản test API (Integration Test) kiểm tra luồng: Tạo Feedback -> Lấy danh sách Pending -> Approve (kiểm tra trạng thái đổi thành APPROVED) -> Reject.

### Manual Verification
1. Mở trang Chat (Frontend), hỏi một câu kiến thức. 
2. Bấm nút "Báo sai" và nhập kiến thức mới "Kính AB 2018 dùng ngàm 10 ly thuận".
3. Vào trang `/admin/knowledge-review`, xác nhận thấy hiển thị dòng kiến thức vừa nhập đang ở trạng thái chờ duyệt.
4. Bấm "Duyệt".
5. Quay lại trang Chat, hỏi lại câu hỏi cũ, xác nhận AI đã trả lời dựa trên kiến thức mới vừa được nạp vào Vector DB.
