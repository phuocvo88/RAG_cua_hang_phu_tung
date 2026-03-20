# Goal Description
Dự án nhằm xây dựng một hệ thống Chatbot AI ứng dụng công nghệ **RAG (Retrieval-Augmented Generation)** để giải quyết vấn đề tra cứu thông tin cho nhân viên cửa hàng phụ tùng xe máy. 
Cửa hàng có hơn 2000 sản phẩm và nhiều kiến thức ngầm (ví dụ: tính tương thích phụ tùng giữa các đời xe như gương AB 2018 dùng chung ngàm với AB 2020). Hệ thống RAG sẽ giúp kết hợp cơ sở dữ liệu cấu trúc (SQL) và tri thức phi cấu trúc (Vector DB) để AI có thể tự động truy xuất và trả lời chính xác các câu hỏi tự nhiên của nhân viên. Sự phán đoán của bạn hoàn toàn chính xác, RAG là kiến trúc chuẩn mực sinh ra để giải quyết bài toán này.

## User Review Required
> [!IMPORTANT]
> Đây là bản thiết kế kiến trúc và kế hoạch triển khai ban đầu. Hãy xem qua phần Tech Stack và Lộ trình bên dưới. Nếu bạn đồng ý, tôi sẽ bắt đầu tiến hành khởi tạo dự án và viết code.
> 
> **Một số tùy chọn cần bạn quyết định:**
> 1. Bạn muốn dùng LLM nào cho hệ thống này (Ví dụ: OpenAI GPT-4o-mini, Google Gemini Flash, hay là dùng Local LLM mã nguồn mở nếu bạn muốn dữ liệu hoàn toàn bảo mật offline)?
> 2. Bạn đã có sẵn database (MySQL/SQL Server) hay muốn tôi tạo một database SQLite mẫu trong dự án để làm prototype (bản nháp) trước?

## Tech Stack Đề Xuất
Hệ thống sẽ được chia làm 2 phần chính độc lập để dễ bảo trì, mở rộng:

**1. Giao diện (Frontend Web):**
  - Next.js (React) + Tailwind CSS để tạo giao diện Chat thân thiện, mượt mà (responsive mượt mà, có thể mở trên cả máy tính bàn và điện thoại của nhân viên).

**2. Xử lý & AI (Backend):**
  - Ngôn ngữ: Python + FastAPI (Tốc độ khởi tạo API cực nhanh).
  - LLM Framework: LlamaIndex hoặc LangChain.
  - Database Truyền thống (SQL): Lưu trữ danh mục 2000+ sản phẩm (Tên, Mã, Giá).
  - Vector Database: Qdrant hoặc ChromaDB lưu trữ trữ các quy tắc tương thích, mẹo sửa chữa không có cấu trúc.

## Proposed Changes
Dự án sẽ được khởi tạo tại `f:\side_projects\RAG_cua_hang_phu_tung`.

### 1. Xây dựng lõi Backend (Python)
- Tạo thư mục `backend/`.
- [NEW] `backend/requirements.txt`: Chứa danh sách các thư viện cần thiết.
- [NEW] `backend/database/`: Thư mục chứa SQL DB và Vector DB nội bộ.
- [NEW] `backend/main.py`: Khởi tạo FastAPI Server và endpoint API `/api/chat`.
- [NEW] `backend/rag_engine.py`: Xây dựng luồng RAG kết hợp tra cứu SQL (Text-to-SQL) và tra cứu Vector (Semantic Search).
- [NEW] `backend/seed_data.py`: Script để nạp dữ liệu giả định 1 vài sản phẩm mẫu và kinh nghiệm thực tế vào hệ thống db để test.

### 2. Xây dựng giao diện Frontend (Next.js)
- Tạo thư mục `frontend/`.
- Xây dựng giao diện Chatbot chuyên nghiệp theo ngôn ngữ thiết kế UI hiện đại, kết hợp gọi API sang Backend và có các hiệu ứng loading thân thiện.

## Verification Plan
### Manual Verification
1. Chạy Backend API server (Python) tại localhost.
2. Chạy Frontend Web App (Next.js) tại localhost.
3. Nhập câu hỏi tình huống mẫu của bạn: *"Cho hỏi mã và giá của kính chiếu hậu xe honda airblade 2018, và nhân viên mới có thể lấy loại này gắn cho xe airblade 2020 được không?"*
4. Xác nhận xem RAG hệ thống có trả lời đủ 3 ý: Mã sản phẩm, Giá sản phẩm (lấy từ SQL) và kết luận là gắn được (lấy từ Vector DB kinh nghiệm) hay không.
