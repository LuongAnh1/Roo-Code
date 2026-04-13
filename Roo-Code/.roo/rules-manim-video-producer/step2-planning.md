# HƯỚNG DẪN BƯỚC 2: PHÁC THẢO & BỐ CỤC
Bạn phải trình bày Kế hoạch Hình ảnh cho người dùng phê duyệt. Trước khi báo cáo, hãy đọc `aesthetics-9-16.md` để nhớ Vùng an toàn.

## QUY TRÌNH KIỂM SOÁT BỐ CỤC (MANDATORY)
Trước khi vẽ Storyboard, BẮT BUỘC thực hiện:
1. **Đọc file**: `.roo/rules-manim-video-producer/tiktok_layout_guide.md`.
2. **Kiểm tra tọa độ**:
   - Mọi đối tượng quan trọng (Text, Box, Hình) phải nằm trong vùng `Y` từ `-3.5` đến `+4.0`.
   - **CẤM** đặt nội dung vào vùng `Y < -4.0` (Vùng Caption TikTok).
   - **CẤM** đặt tiêu đề vào vùng `Y > 5.5` (Vùng Logo).
3. **Báo cáo**: Trong phần "Bố cục", bạn phải liệt kê tọa độ Y dự kiến cho từng cụm đối tượng.

**BÁO CÁO PHẢI CÓ ĐỦ 3 MỤC SAU TRONG 1 TIN NHẮN:**

**1. VISUAL METAPHOR (Ý TƯỞNG ẨN DỤ)**
- Không chỉ hiện Text khô khan. Hãy đề xuất dùng hình khối, đồ thị, biểu tượng để minh họa cho lời thoại. Bạn CÓ QUYỀN sáng tạo mã Manim phức tạp.
- Có thể xem 1 lượt folder assets xem có hình ảnh định dạng `.svg` nào phù hợp để thêm vào kịch bản

**2. OBJECTS & SKILLS (ĐỐI TƯỢNG SỬ DỤNG)**
- Tiêu đề: BẮT BUỘC dùng `title = self.create_title(...)` từ `fami_lib.py`.
- Subtitle: BẮT BUỘC dùng `self.update_subtitle(...)` từ `fami_lib.py`.
- Liệt kê các Class Manim sẽ dùng (VD: `VGroup`, `MarkupText`, `Rectangle`).

**3. CHOREOGRAPHY (SẮP XẾP & CHUYỂN ĐỘNG)**
- Mô tả cách các vật thể nằm trên màn hình (Phải nằm trong khoảng Y từ +4.0 đến -3.5).
- Mô tả hiệu ứng xuất hiện.

🔴 **DỪNG LẠI (STOP):** Trình bày xong, yêu cầu người dùng duyệt kế hoạch.