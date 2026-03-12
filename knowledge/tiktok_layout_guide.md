# TikTok 9:16 Layout & Aesthetics Guide (FaMI Version)

## 1. Camera System (Vertical Standard)
- `frame_height = 16.0` | `frame_width = 9.0`
- Tọa độ Y: Từ `+8.0` (Đỉnh) đến `-8.0` (Đáy).
- Tọa độ X: Từ `+4.5` (Phải) đến `-4.5` (Trái).

## 2. Quy tắc Phân vùng Tọa độ (Vertical Zoning)
Agent BẮT BUỘC phải tuân thủ các mốc tọa độ Y sau để tránh bị UI của TikTok che khuất:

| Vùng | Khoảng Tọa độ Y | Chức năng | Quy tắc |
| :--- | :--- | :--- | :--- |
| **Header** | `+5.5` đến `+7.5` | Logo & Thương hiệu | Dùng `FaMIBaseScene` |
| **Title** | `+4.5` đến `+5.5` | Tiêu đề bài học | Dùng `self.create_title()` |
| **Main Content** | `-3.5` đến `+4.0` | **VÙNG AN TOÀN TUYỆT ĐỐI** | Mọi animation chính nằm ở đây |
| **Subtitle** | `-4.5` | Phụ đề lời thoại | Dùng `self.update_subtitle()` |
| **Dead Zone Bottom** | `-5.0` đến `-8.0` | **VÙNG CẤM** | Bị che bởi Caption/Username TikTok |

## 3. Typography & Horizontal Constraints
- **Ép kích thước ngang**: Mọi `VGroup` nội dung chính KHÔNG ĐƯỢC VƯỢT QUÁ **7.5 units**.
- **Lệnh thực thi**: `if obj.width > 7.5: obj.scale_to_fit_width(7.5)`
- **Font chữ**: Luôn dùng `font="Segoe UI"` cho `Text` và `MarkupText`.

## 4. Bố cục Thông minh (Relative Positioning)
Thay vì dùng tọa độ cứng (`UP*3`), hãy sử dụng vị trí tương đối để tránh chồng lấn:
1. **Title**: Luôn là mốc cao nhất.
2. **Body**: Luôn đặt dưới Title: `obj.next_to(title, DOWN, buff=0.8)`.
3. **CTA/Question**: Luôn đặt ở đáy vùng an toàn: `obj.move_to(DOWN * 3.5)`.

## 5. PROTOCOL TỰ ĐỘNG BỐ CỤC (CHECKLIST TRƯỚC KHI CODE)
Trước khi viết mã nguồn, Agent phải tự trả lời 3 câu hỏi:

1. **Vị trí**: Đối tượng này có nằm dưới Tiêu đề (`next_to`) và trên Subtitle (Y > -4) không?
2. **Kích thước**: Nếu mình thêm 1 mũi tên vào 2 bên, tổng bề ngang có vượt quá 8.0 không? hoặc câu hỏi tương tự thế trong các trường hợp dàn trải ngang (Nếu có -> phải `.scale_to_fit_width(7.5)`).
3. **Thứ tự**: Mình đã `arrange()` và `scale()` nhóm đối tượng XONG XUÔI rồi mới vẽ Mũi tên nối chưa? (Mũi tên phải vẽ cuối cùng) và các câu hỏi tương tự vậy.

## 6. Màu sắc Thương hiệu (Brand Colors)
Sử dụng các hằng số từ `skills/fami_lib.py`:
- `FAMI_CYAN`, `ACCENT`, `SUCCESS`, `DANGER`, `TEXT_COLOR`.
- Tránh dùng màu gốc `BLUE`, `RED`, `GREEN` của Manim.