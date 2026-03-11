# TikTok 9:16 Layout & Aesthetics Guide

## 1. Camera System (Vertical)
- `frame_height = 16.0`
- `frame_width = 9.0`
- Tọa độ Y: Từ `+8.0` (Đỉnh) đến `-8.0` (Đáy).
- Tọa độ X: Từ `+4.5` (Phải) đến `-4.5` (Trái).

## 2. Safe Zone & Horizontal Constraints (QUAN TRỌNG)
- **Chiều rộng khả dụng**: Màn hình có `frame_width=9`. Để tránh tràn viền, tổng chiều rộng các đối tượng trong 1 hàng (row) **không được vượt quá 7.0 units**.
- **Quy tắc dàn hàng ngang**: Luôn sử dụng `VGroup().arrange(RIGHT, buff=0.5)` thay vì dùng `next_to` liên tiếp, vì `arrange` sẽ tự động co giãn nếu bạn kết hợp với `scale_to_fit_width`.

## 3. Typography (Cỡ chữ)
- **Title (Tiêu đề)**: `font_size=50` đến `60`. Vị trí: `to_edge(UP, buff=1.5)`.
- **Body (Nội dung)**: `font_size=35` đến `45`.
- **Note (Ghi chú)**: `font_size=25` đến `30`.

## 4. Màu sắc chuyên nghiệp (HEX)
- Cyan (Chính): `#00d4ff`
- Yellow (Nhấn mạnh): `#fffa65`
- Red (Cảnh báo): `#ff4d4d`
- Background: `#1a1a1a` (Dark Grey, không dùng Pure Black).

## 5. Agent Note
- Video TikTok cần nhịp điệu nhanh. 
- Không để màn hình trống quá 0.5 giây.
- Sử dụng `Indicate()` cho các từ khóa quan trọng khi giọng đọc nhắc đến.

## 6. PROTOCOL TỰ ĐỘNG BỐ CỤC (MANDATORY CHECKLIST)
Trước khi đưa bất kỳ đối tượng nào vào `self.play(...)`, Agent BẮT BUỘC thực hiện quy trình sau để tránh tràn viền:

### Quy tắc 1: Kiểm soát kích thước ngang (Horizontal Width Limit)
- Mọi nội dung (Text, VGroup, Mobject) **KHÔNG ĐƯỢC VƯỢT QUÁ 8.0 units** bề ngang. 
- **Lệnh ép buộc**: Mọi Mobject/VGroup chứa Text hoặc nhiều đối tượng phải đi kèm lệnh:
  `my_group.scale_to_fit_width(8.0)`
- Nếu nội dung dài, **BẮT BUỘC** dùng `Paragraph` để ngắt dòng thay vì co bóp Text quá mức làm chữ bị méo.

### Quy tắc 2: Thứ tự logic của Layout (The "Layout-First" Rule)
- Tuyệt đối không vẽ Arrow, Line nối giữa các vật thể trước khi các vật thể đó được `arrange()` hoặc `scale()`.
- **Thứ tự đúng:**
  1. Khai báo đối tượng (Mobject).
  2. Gom nhóm (VGroup) & Căn lề (`arrange`, `scale_to_fit_width`).
  3. Định vị cuối cùng (`center`, `to_edge`).
  4. **CUỐI CÙNG**: Mới tạo Arrow, Line nối giữa các đối tượng (vì lúc này tọa độ của vật thể mới chính xác).

### Quy tắc 3: Kiểm tra Title
- Title không được dùng `Text()` nếu nó dài hơn 30 ký tự. 
- **Bắt buộc dùng**: `Paragraph` hoặc tách thành 2 câu trên 2 dòng để giữ font size chuẩn (50-60).