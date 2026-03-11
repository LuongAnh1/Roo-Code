# Manim Math & LaTeX Syntax

## 1. Cấu trúc chuẩn
- `MathTex(r"content")`: Luôn có tiền tố **r**.
- Để đổi màu từng phần: `MathTex(r"{{a^2}} + {{b^2}} = {{c^2}}")`.
- Sau đó dùng: `formula.set_color_by_tex("a^2", YELLOW)`.

## 2. Ký hiệu phổ biến
- **Phân số**: `\frac{tu}{mau}`
- **Căn bậc hai**: `\sqrt{x}`
- **Số mũ/Chỉ số**: `a^{2}`, `x_{i}`
- **Dấu nhân**: `\cdot`, `\times`
- **Xác suất**: `P(A|B)`
- **Vector**: `\vec{v}`
- **Góc**: `\angle ABC`

## 3. Linh kiện hỗ trợ
- `Brace(obj, direction=DOWN)`: Vẽ dấu ngoặc nhọn ôm vật thể.
- `Brace.get_text("Label")`: Thêm nhãn cho dấu ngoặc.
- `DecimalNumber(0, num_decimal_places=2)`: Hiển thị số chạy.

## 4. Agent Note
- Kiểm tra kỹ các dấu ngoặc nhọn `{ }` trong LaTeX để tránh lỗi render.
- Nếu công thức quá dài, dùng `{{...}}` để tự động ngắt dòng hoặc scale nhỏ lại.