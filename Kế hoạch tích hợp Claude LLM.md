# Kế hoạch tích hợp Claude LLM

Dưới đây là kế hoạch để giúp bạn mua token Claude và cấu hình hệ thống RAG để sử dụng model này thay vì (hoặc song song với) Google Gemini.

## 1. Hướng dẫn mua Token Claude (Anthropic API)

Để mua token (credits), bạn thực hiện các bước sau trên Console của Anthropic:

1.  Truy cập: [console.anthropic.com](https://console.anthropic.com/)
2.  Đăng ký hoặc Đăng nhập vào tài khoản của bạn.
3.  Đi tới phần **Billing** (thường nằm ở góc trên bên phải hoặc thanh menu bên trái).
4.  Thêm phương thức thanh toán (Thẻ Visa/Mastercard).
5.  Chọn **Add Funds** để mua Credits. Anthropic hoạt động theo mô hình trả trước (Prepaid) - bạn nạp tiền vào tài khoản và token sẽ bị trừ dần khi sử dụng.
6.  Sau khi đã có Credits, hãy vào mục **API Keys** để tạo một Key mới.

## 2. Các thay đổi đề xuất cho Codebase

### [MÔI TRƯỜNG]
#### [MODIFY] .env.example
*   Thêm biến `ANTHROPIC_API_KEY`.

### [BACKEND]
#### [MODIFY] requirements.txt
*   Thêm `llama-index-llms-anthropic`.

#### [MODIFY] rag_engine.py
*   Cập nhật logic để cho phép chuyển đổi giữa Gemini và Claude.

## 3. Kế hoạch xác minh

### Kiểm tra thủ công
*   Xác nhận Key hoạt động bằng cách chạy một script test nhỏ gọi tới Claude API.
*   Chạy `test_rag.py` để đảm bảo hệ thống phản hồi chính xác khi dùng Claude.
