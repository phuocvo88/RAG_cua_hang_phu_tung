# Planning Gradle Integration

Dự án RAG_cua_hang_phu_tung sẽ sử dụng Gradle để quản lý quy trình xây dựng (build) cho cả Backend (Python) và Frontend (Next.js).

## Cấu trúc dự án Gradle (Dự kiến)

- `settings.gradle`: Khai báo các module con (`backend`, `frontend`).
- `build.gradle` (Gốc): Cấu hình chung cho toàn bộ dự án.
- `backend/build.gradle`: Quản lý môi trường ảo Python, cài đặt dependencies từ `requirements.txt`, chạy server FastAPI và tests.
- `frontend/build.gradle`: Sử dụng `gradle-node-plugin` để quản lý `npm install`, `next build` và `next dev`.

## Lợi ích của việc sử dụng Gradle

1. **Thống nhất CLI**: Bạn chỉ cần dùng lệnh `./gradlew` để thực hiện các tác vụ khác nhau cho cả backend và frontend.
2. **Quản lý phụ thuộc chéo**: Dễ dàng thực thi các chuỗi tác vụ, ví dụ: chạy backend trước khi khởi động frontend test.
3. **Môi trường nhất quán**: Sử dụng Gradle Wrapper đảm bảo mọi thành viên trong team sử dụng cùng một phiên bản Gradle.

## Các bước triển khai

1. Khởi tạo Gradle Wrapper.
2. Tạo tệp `settings.gradle` và `build.gradle` ở thư mục gốc.
3. Cấu hình module `backend` với các task Python `Exec`.
4. Cấu hình module `frontend` với Gradle Node plugin.
5. Kiểm tra khả năng chạy và build của toàn bộ hệ thống.

---
*Kế hoạch được lập ngày 24/03/2026 bởi Antigravity AI.*
