# TIÊU CHUẨN THẨM MỸ VIDEO DỌC 9:16 (TIKTOK / REELS / SHORTS)

Video dọc có một nhược điểm chí mạng: Giao diện nền tảng (UI) như nút Like, Share, Tên kênh, Caption sẽ CHÉP KHUẤT rất nhiều diện tích màn hình. Agent BẮT BUỘC tuân thủ bảng thông số dưới đây để không bị mất nội dung.

## 1. Thông số Config Bắt Buộc
(Phải khai báo ở đầu file hoặc trước khi định nghĩa Class)
```python
config.pixel_height = 1920
config.pixel_width = 1080
config.frame_height = 16.0
config.frame_width = 9.0
```

## 2. Bố cục An toàn (The Safe Zones) - QUY TẮC SỐNG CÒN
Trục Y (Chiều dọc) của Manim đi từ +8 (Trên cùng) đến -8 (Dưới đáy). Trục X đi từ -4.5 (Trái) đến +4.5 (Phải).
Agent TUYỆT ĐỐI CẤM đặt bất kỳ văn bản (Text) hoặc Công thức quan trọng nào vào các VÙNG CHẾT (Dead Zones) sau:
- ❌ Dead Zone 1 (Trên cùng): Y từ +7.5 đến +8.0 (Bị che bởi thanh trạng thái điện thoại).
- ❌ Dead Zone 2 (Dưới đáy - Rất nguy hiểm): Y từ -5.5 đến -8.0 (Bị che 100% bởi Tên kênh, Caption dài, thanh nhạc của Reels/TikTok).
- ❌ Dead Zone 3 (Bên phải): X từ +3.5 đến +4.5 (Bị che bởi dải nút Like, Comment, Share).

**CÁCH PHÂN VÙNG CHUẨN (Zoning):**
Mọi hoạt ảnh chỉ được phép diễn ra trong khu vực từ `Y = -5` đến `Y = +7`.
- ✅ Vùng 1: Header (`Y = +5.5` đến `+7.0`): Chỉ dành cho Tiêu đề Scene (Title). Dùng `to_edge(UP, buff=1.5)`.
- ✅ Vùng 2: Main Stage (`Y = -1.0` đến `+4.0`): Khu vực diễn ra animation chính, đồ thị, hình khối. Đây là trung tâm sự chú ý.
- ✅ Vùng 3: Sub-Stage (`Y = -2.0` đến `-4.5`): Dành cho chú thích phụ, công thức bổ trợ, hoặc text dài.
- ✅ Vùng 4: Footer/CTA (`Y = -5.0`): Mức THẤP NHẤT cho phép đối với dòng Kêu gọi hành động (Subscribe/Comment). Không được thấp hơn -5.

## 3. Quy tắc Tránh Tràn Viền (Anti-Overflow)
- Chiều ngang (Width): Khung hình dọc rất hẹp (`frame_width = 9`). Trước khi add bất kỳ đối tượng nào (đặc biệt là Text hoặc MathTex dài), BẮT BUỘC dùng lệnh `scale_to_fit_width` để ép nó nằm gọn trong màn hình:
```python
# Nếu công thức/Text vượt quá bề ngang 8 units, tự động thu nhỏ lại:
if my_text.width > 8:
    my_text.scale_to_fit_width(8)
```
- Text nhiều dòng: Nếu kịch bản có một câu text dài hơn 8 từ, KHÔNG dùng `Text("...")` một dòng duy nhất. Bắt buộc ngắt dòng bằng ký tự \n hoặc chia thành nhiều biến Text nhỏ xếp chồng lên nhau bằng VGroup.

4. Bảng Màu Hiện Đại (Modern Palette)
Tuyệt đối KHÔNG dùng các màu gốc (nguyên bản) như RED, GREEN, BLUE, YELLOW của Manim vì chúng trông rất rẻ tiền và chói mắt.
Hãy khởi tạo bảng màu neon/pastel sau ở đầu mỗi Class và sử dụng chúng:
```python
PRIMARY = "#00d4ff"  # Cyan sáng (Dành cho viền, điểm nhấn chính)
ACCENT = "#fffa65"   # Vàng Pastel (Dành cho Text quan trọng, kết quả)
DANGER = "#ff4d4d"   # Đỏ Coral (Dành cho cảnh báo, lỗi sai)
SUCCESS = "#00e676"  # Xanh lục Neon (Dành cho đúng, xác nhận)
TEXT_COLOR = "#ffffff" # Trắng tinh (Dành cho text thông thường)
```