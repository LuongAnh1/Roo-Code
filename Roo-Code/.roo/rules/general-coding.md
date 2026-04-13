# QUY TẮC LẬP TRÌNH CHUNG & QUẢN LÝ DỰ ÁN

Mọi mã nguồn Python và cấu trúc dự án phải tuân thủ các tiêu chuẩn kỹ thuật phần mềm dưới đây:

## 1. Tiêu chuẩn Python (PEP 8)
- **Đặt tên (Naming)**: 
    - Biến và hàm: dùng `snake_case` (ví dụ: `formula_color`, `create_main_title`).
    - Lớp (Classes): dùng `PascalCase` (ví dụ: `IntroScene`, `PythagorasTheorem`).
    - Hằng số: dùng `UPPER_SNAKE_CASE` (ví dụ: `BG_COLOR`, `DEFAULT_FONT_SIZE`).
- **Thụt lề**: Luôn dùng 4 khoảng trắng (spaces).
- **Imports**: Luôn đặt các thư viện hệ thống ở trên cùng, sau đó đến các thư viện bên thứ ba (Manim), cuối cùng là các module tự viết.

## 2. Tư duy Code sạch (Clean Code)
- **Tính mô-đun (Modularity)**: Chia nhỏ các đoạn code phức tạp thành các hàm riêng biệt. Nếu một logic (ví dụ: vẽ một mũi tên có nhãn) lặp lại > 2 lần, hãy viết một hàm cho nó.
- **Tên biến có ý nghĩa**: Tránh đặt tên biến vô nghĩa như `a`, `b`, `x1`. Hãy dùng `triangle_hypotenuse`, `header_text`, `spam_icon`. (Ngoại trừ các ký hiệu toán học chính thống trong MathTex).
- **DRY (Don't Repeat Yourself)**: Không lặp lại code. Sử dụng kế thừa (Inheritance) nếu nhiều Scene dùng chung cấu hình.

## 3. Quản lý thư mục dự án
Agent phải giữ cho dự án gọn gàng theo cấu trúc sau:
- `scripts/`: Chứa các file Python (.py) thực thi Manim.
- `scripts/temp/`: Chứa các file code nháp hoặc thử nghiệm.
- `media/`: Thư mục mặc định của Manim để xuất video/ảnh.
- `.roo/`: Thư mục chứa các quy tắc và template của Agent.
- `knowledge/`: Thư mục chứa tài liệu tra cứu API.

## 4. Chú thích & Giải trình (Documentation)
- **Comment**: Code phải có chú thích giải thích *tại sao* làm như vậy (logic chuyển cảnh, lý do chọn màu).
- **Docstrings**: Mỗi class Scene chính phải có một đoạn mô tả ngắn về mục đích của Scene đó ở đầu class.

## 5. Quy trình Sửa lỗi (Debugging)
- Khi gặp lỗi `Traceback`, Agent phải:
    1. Đọc dòng cuối cùng để xác định loại lỗi (NameError, TypeError, v.v.).
    2. Kiểm tra lại các file Rule tương ứng để xem mình có vi phạm cú pháp không.
    3. Tự động sửa code và chạy lại lệnh render ít nhất 2 lần trước khi hỏi người dùng.

## 6. Tương tác với Người dùng (User Interaction)
- Luôn báo cáo tiến độ theo từng bước: "Đã đọc xong kịch bản" -> "Đã lên kế hoạch layout" -> "Bắt đầu viết code".
- Khi gửi code, hãy kèm theo lệnh Terminal để người dùng có thể copy và chạy ngay (ví dụ: `manim -pql scripts/my_scene.py MyScene`).