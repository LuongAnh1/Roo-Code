# TIÊU CHUẨN THẨM MỸ VIDEO DỌC (DESIGN THEORY)

Mục đích của file này là hướng dẫn Agent cách sắp xếp không gian sao cho video chuyên nghiệp và không bị giao diện TikTok che khuất. Các thông số kỹ thuật và màu sắc đã có sẵn trong `fami_lib.py`.

## 1. TƯ DUY VÙNG AN TOÀN (SAFE ZONE REASONING)
Agent phải hiểu rằng màn hình điện thoại bị che khuất bởi 3 yếu tố ngoại cảnh:

1. **Thanh Trạng Thái (Clock/Battery):** Chiếm vùng `Y > +7.2`. 
   - *Hành động:* Logo FaMI đã được đặt ở vùng này bằng `setup()`, không đặt thêm gì khác ở đây.
2. **Giao Diện Nền Tảng (Like/Comment/Share):** Chiếm dải bên phải màn hình `X > +3.5`.
   - *Hành động:* Luôn giữ nội dung chính co cụm vào tâm hoặc dạt sang trái một chút.
3. **Caption & Username (Phần chữ dài bên dưới):** Chiếm vùng `Y < -5.0`.
   - *Hành động:* Phụ đề (Subtitle) đã được khóa ở `Y = -4.5`. **TUYỆT ĐỐI CẤM** đặt bất kỳ thông tin quan trọng nào thấp hơn vị trí của Phụ đề.

## 2. QUY TẮC "DÀN HÀNG NGANG" (HORIZONTAL LIMITS)
Dù `frame_width = 9.0`, nhưng diện tích "nhìn rõ" chỉ có 7.5 units.
- **Quy tắc 7.5:** Mọi `VGroup` hoặc đoạn văn bản dài phải được ép kích thước: 
  `if obj.width > 7.5: obj.scale_to_fit_width(7.5)`
- **Quy tắc Ngắt dòng:** Nếu một câu dài hơn 30 ký tự, Agent **phải chủ động** chia thành 2-3 dòng bằng `Paragraph()` thay vì cố ép nhỏ nó lại (gây khó đọc).

## 3. PHÂN CẤP THỊ GIÁC (VISUAL HIERARCHY)
Agent đóng vai trò Giám đốc Nghệ thuật, phải sắp xếp theo thứ tự ưu tiên:
1. **Tiêu đề (Bắt buộc):** Luôn gọi `self.create_title()` để nằm ngay dưới Logo.
2. **Nội dung chính (Focus):** Phải nằm ở "Vùng Vàng" (`Y = -1.0` đến `+4.0`). Đây là nơi mắt người dùng tập trung nhiều nhất.
3. **Chú thích/CTA:** Nằm ở vùng `Y = -3.0` đến `-3.5`.

## 4. TỐI ƯU HÓA CHUYỂN ĐỘNG (MOTION DESIGN)
- **Nhịp độ:** Video TikTok cần nhanh. Sử dụng `skill_pop_in` (Scale & Ease Out) thay cho `FadeIn` đơn điệu.
- **Tính đồng nhất:** Giữ cho các vật thể có cùng một "ngôn ngữ chuyển động" (Ví dụ: Tất cả đều bay từ dưới lên hoặc đều hiện ra từ tâm).