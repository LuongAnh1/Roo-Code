# BẢN ĐỒ KHÔNG GIAN TIKTOK 9:16 (SPATIAL MENTAL MODEL)

File này định hình "Tư duy không gian" cho Agent khi thiết kế các Custom Mobjects trong vùng Sáng tạo (Creative Zone) của Template.

## 1. HỆ TỌA ĐỘ VÀ CÁC VÙNG CẤM (DEAD ZONES)
Màn hình dọc có `Y` từ `+8.0` (Đỉnh) đến `-8.0` (Đáy), `X` từ `-4.5` (Trái) đến `+4.5` (Phải).
Khi bạn tự do sáng tạo nội dung, BẮT BUỘC phải né các vùng UI của ứng dụng:

- ❌ **Dead Zone 1 (Đỉnh - Y > 5.5):** Vùng của Logo. Không vẽ gì ở đây.
- ❌ **Dead Zone 2 (Đáy - Y < -4.0):** Vùng "Tử địa" chứa Caption dài, Tên kênh, Thanh nhạc. Không một object nào được thò xuống dưới `Y = -4.0`.
- ❌ **Dead Zone 3 (Sườn Phải - X > 3.5):** Dải nút Like, Comment, Share. Tránh để Text quan trọng lẹm vào đây.

## 2. VÙNG VÀNG SÁNG TẠO (THE GOLDEN STAGE)
Mọi ma thuật, đồ thị, hình khối của bạn PHẢI diễn ra gọn gàng trong khu vực:
**Trục Y: Từ `-3.5` đến `+4.0`**

## 3. TƯ DUY XẾP HÌNH (TOP-DOWN FLOW)
Để không bao giờ bị đè hình lên nhau khi màn hình quá chật:
1. **Luôn xây từ trên xuống:** Lấy `title` làm mốc gốc.
2. **Dùng vị trí tương đối:** Thay vì ước lượng tọa độ cứng (`move_to(UP*2)`), hãy dùng `next_to(obj_phía_trên, DOWN, buff=...)` để các khối tự đẩy nhau xuống dưới một cách an toàn.
3. **Cột dọc thay vì hàng ngang:** Ưu tiên `arrange(DOWN)` thay vì `arrange(RIGHT)` vì chiều ngang chỉ có 7.5 units khả dụng.

## 4. CHIẾN LƯỢC CHỐNG TRÀN BỀ NGANG
Dù bạn vẽ bất kỳ cụm Group, Đồ thị hay Phương trình nào phức tạp đến đâu, **trước khi đưa vào `self.play`**, hãy nhẩm tính:
*"Cụm này có rộng quá 7.5 units không?"* 
Nếu có nguy cơ, bắt buộc dùng `scale_to_fit_width(7.5)` làm lưới bảo vệ cuối cùng.