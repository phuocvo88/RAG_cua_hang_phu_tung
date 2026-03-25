# Project Backlog Items

Tài liệu này dùng để lưu trữ các yêu cầu, tính năng mới và các câu hỏi cần nghiên cứu trong tương lai cho dự án.

## Tính năng / Yêu cầu (Features & Requirements)

1. **AI Clarification Prompt (Hỏi lại để xác nhận):** 
   - Nếu nhân viên hỏi một câu hỏi mà AI chat bot không tìm được câu trả lời match với câu hỏi, hệ thống phải confirm lại là: *"Có phải bạn muốn hỏi <điều mà AI hiểu>?"*.

2. **Cơ chế phân quyền quản lý kiến thức (Role-based Access Control):** 
   - Xây dựng cơ chế để cấp quyền (grant quyền) `manager` hoặc `approver` cho trang "Quản lý góp ý kiến thức". 
   - Người `manager` có thể chia sẻ quyền cho một hoặc nhiều người khác để họ có thể phê duyệt (approve) kiến thức mới cho AI.

## Nghiên cứu / Câu hỏi kỹ thuật (Research & Technical Questions)

1. **Dung lượng lưu trữ cho Vector Database Local:** 
   - **Vấn đề:** Nếu kiến thức ngày càng nhiều thì nên dùng database local với dung lượng ổ cứng bao nhiêu là đủ để chứa kiến thức cho chatbot AI? 
   - **Cần làm:** Ước tính xem vector database hiện tại có thể chứa được dung lượng kiến thức nhiều bao nhiêu để có kế hoạch nâng cấp dung lượng. 
   - **Cần làm:** Gợi ý các dịch vụ cloud để làm database lưu trữ knowledge.

2. **Chiến lược Local vs. Cloud Database & Migration Plan:** 
   - **Vấn đề:** Làm sao xác định được khi nào cần chuyển database lên cloud, hay chỉ cần dùng vector database ở local server của cửa hàng là đủ?
   - **Cần làm:** Đánh giá mức độ khó của việc migration (chuyển đổi) vector database từ local server lên cloud.
   - **Cần làm:** Lên một kế hoạch cụ thể cho việc migration này nếu cần thiết.

---

## Ghi chú tham khảo (Notes)

### 1. Dung lượng ổ cứng cho Vector Database Local

- **Ước tính dung lượng:** Vector Database lưu trữ kiến thức dưới dạng các "vector số" (embeddings) kèm theo metadata. Một chunk văn bản (khoảng 500-1000 từ) khi chuyển sang vector 1536 chiều tiêu tốn khoảng **6KB đến 10KB** không gian lưu trữ (bao gồm metadata).
- **Đánh giá:** Giả sử có **100,000 tài liệu/chunk** (số lượng rất lớn đối với kiến thức 1 cửa hàng), dung lượng lưu trữ chỉ rơi vào khoảng **1 Gigabyte (1 GB)**. 
- **Kết luận:** Dung lượng ổ cứng không phải là rào cản. Có thể chạy Vector DB gọn nhẹ ở local với ổ cứng SSD 256GB - 512GB thông thường.
- **Các dịch vụ Cloud Database phổ biến:** Pinecone (dễ dùng, serverless), Qdrant/Weaviate (mã nguồn mở phổ biến), Supabase (dùng add-on pgvector).

### 2. Có cần lên Cloud không & Việc migration có khó không?

- **Khi nào nên dùng Local:** Nếu hệ thống chỉ dùng nội bộ trong 1 cửa hàng, băng thông mạng ra ngoài không ổn định, và ưu tiên tiết kiệm chi phí hàng tháng.
- **Khi nào nên lên Cloud:** Chuỗi cửa hàng mở rộng nhiều chi nhánh, hoặc triển khai chatbot lên website/Zalo OA cho khách tiếp cận, cần độ sẵn sàng cao (High Availability) mà không lệ thuộc mạng/điện tại cửa hàng.
- **Đánh giá độ khó Migration:** Khá Đơn Giản (Easy to Moderate).
- **Kế hoạch Migration cơ bản:**
  1. Tạo tài khoản thẻ tín dụng/Database trống trên Cloud (VD: tạo Pinecone index).
  2. Cập nhật biến môi trường, đổi URL kết nối và API Key trong code backend sang Cloud.
  3. Viết và chạy 1 script để tiến hành đọc lại toàn bộ dữ liệu gốc (document text) đang có, embedding lại và đẩy (`upsert`) vào Database Cloud.
  4. Test thử các câu hỏi của chatbot để đảm bảo RAG trả về đúng kết quả, sau đó có thể tắt Vector Database dưới Local.
