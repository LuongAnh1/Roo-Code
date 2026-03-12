# TIÊU CHUẨN VIẾT CODE MANIM COMMUNITY (BEST PRACTICES)

## 0. CẤU TRÚC CODE (MANDATORY)
- Mọi file code trong `scripts/` BẮT BUỘC phải bắt đầu bằng đoạn code sau để Python tìm thấy thư mục `skills/`:
```python
import sys
import os
# Trỏ đường dẫn về thư mục gốc để import thư viện skills
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from skills.fami_lib import *
```
- **Kế thừa**: Mọi Scene class phải kế thừa từ `FaMIBaseScene`.
- **An toàn (Safe-Guard)**: 
  - Mọi `Text` hoặc `Paragraph` tạo ra BẮT BUỘC kiểm tra độ rộng: `if obj.width > 7.5: obj.scale_to_fit_width(7.5)`.
  - Không bao giờ dùng `to_edge(UP)` cho tiêu đề, hãy dùng `self.create_title()` từ thư viện.
  - **Tiêu đề**: Luôn dùng `title = self.create_title("Dòng 1", "Dòng 2")`. (Hàm này đã tự định vị đúng chỗ).
  - **Phụ đề**: Trong mọi khối `with self.voiceover(...)`, dòng lệnh đầu tiên phải là: `self.update_subtitle("Nội dung phụ đề")`.
  - **Màu sắc**: Dùng các hằng số màu có sẵn: `FAMI_CYAN`, `FAMI_BLUE`, `ACCENT`, `SUCCESS`, `DANGER`.

## 1. QUY TẮC VOICEOVER & SUBTITLE
- Mỗi khối `with self.voiceover(text=...)` BẮT BUỘC phải có `self.update_subtitle(...)` ngay dòng đầu tiên.
- Không được dùng `run_time=tracker.duration` cho mọi hiệu ứng. Phải chia tỉ lệ (ví dụ: `0.4 * tracker.duration`) để tạo nhịp điệu.

## 2. QUY ĐỊNH TOÁN HỌC & CÚ PHÁP
- **Toán học**: Luôn có `import math` và `import numpy as np`. CẤM dùng `sin()`, phải dùng `np.sin()` hoặc `math.sin()`.
- **LaTeX**: Luôn dùng `MathTex(r"...")` (có tiền tố r).
- **Animation**: Bắt buộc dùng `obj.animate.method(...)`. CẤM dùng `obj.animate(...)`.
- **Updaters**: KHÔNG khởi tạo `Text` hay Mobject mới bên trong hàm updater (gây tràn RAM). CẤM dùng `self.get_time()`, phải dùng `self.renderer.time`.

## 3. TEXT, MARKUP & ANTI-CRASH
- **CẤM**: Không sử dụng `get_part_by_text()` hoặc `set_color_by_text()` với đối tượng `Text`.
- **MARKUPTEXT**: Khi cần tô màu 1 từ hoặc có ký tự đặc biệt (€, $, @), BẮT BUỘC dùng `MarkupText` và thẻ `<span>`.
    - *Ví dụ:* `MarkupText(f'Chữ <span color="{ACCENT}">Vàng</span>', font="Segoe UI")`

## 4. QUY TẮC HIỆU ỨNG GÕ CHỮ (CHỐNG LỆCH CHỮ)
Để dòng chữ không bị bay ra ngoài, CẤM dùng `Text(" ")` hoặc `VGroup()` rỗng làm mốc.
**Bắt buộc bắt chước cấu trúc sau:**
```python
last_char = obj_moc_ban_dau # VD: magnifying_glass
current_buff = 0.3 

for i, char in enumerate(text_str):
    if char == " ":
        current_buff = 0.3 # Tăng khoảng cách khi gặp dấu cách
        continue
        
    new_char = Text(char, font="Segoe UI", font_size=40, color=WHITE)
    # aligned_edge=DOWN giữ các chữ đứng trên cùng 1 mặt phẳng
    new_char.next_to(last_char, RIGHT, buff=current_buff, aligned_edge=DOWN)
    
    # KHÓA TRỤC Y: Bắt buộc để chữ không nhảy lên xuống
    new_char.match_y(search_bar)
    
    self.play(FadeIn(new_char), run_time=0.08)
    
    last_char = new_char
    current_buff = 0.08 # Trả về khoảng cách bình thường
  ```
## 5. ĐỒNG BỘ THỜI GIAN (TIMING & PACING)
- **CẤM DOUBLE WAIT**: Tuyệt đối KHÔNG dùng `self.wait(tracker.duration)` hay `self.wait(tracker.get_remaining_duration())` ở cuối khối voiceover. Thư viện đã TỰ ĐỘNG CHỜ.
- **CHIA NHỎ %**: Nếu thoại dài, hãy chia nhỏ Animation: `run_time = tracker.duration * 0.4`.

## 6. NÂNG CẤP THẨM MỸ (PREMIUM LOOK)
- Gradient: `obj.set_color([FAMI_CYAN, ACCENT])`
- Nền chữ (Layering): Thêm `BackgroundRectangle(my_text, color=BLACK, fill_opacity=0.6, buff=0.2)`
- Hiệu ứng Juicy (TikTok style): `self.play(FadeIn(obj, scale=0.5, shift=UP*0.5), rate_func=rate_functions.ease_out_back)`
- Neon Glow (Phát sáng):
`glow = main_obj.copy().set_stroke(color=ACCENT, width=15, opacity=0.3).set_fill(opacity=0)`

## 7. QUY TẮC BỐ CỤC 9:16 (CHỐNG TRÀN CHỮ)
- **CẤM CHIA CỘT NGANG**: Tuyệt đối không đặt 2 khối văn bản cạnh nhau theo chiều ngang (RIGHT/LEFT). Màn hình dọc quá hẹp sẽ làm chữ bị tràn hoặc bé xíu. 
- **LUÔN XẾP DỌC**: Mọi danh sách, so sánh phải dùng `arrange(DOWN)`.
- **FONT TRONG MARKUP**: `MarkupText` không tự nhận font global tốt bằng `Text`. BẮT BUỘC luôn khai báo `font="Segoe UI"` bên trong hàm `MarkupText`.
- **ANTI-WAIT**: Tuyệt đối không dùng `self.wait(tracker.get_remaining_duration() - x)`. Hãy để Manim tự chờ. Nếu muốn ngắt quãng, dùng `tracker.duration * tỉ_lệ`.

## 8. QUY TẮC VỀ HẰNG SỐ & MÃ HÓA (ENCODING)
- **Hằng số tọa độ**: TUYỆT ĐỐI KHÔNG dùng `CENTER`. Bắt buộc dùng **`ORIGIN`** cho tọa độ trung tâm `[0,0,0]`.
- **Căn lề VGroup**: Khi dùng `arrange()`, nếu muốn căn giữa các vật thể, hãy dùng `aligned_edge=ORIGIN`.
- **Lỗi Tiếng Việt (Encoding)**: 
    - Tuyệt đối không để mã nguồn xuất hiện các ký tự kiểu `\u1ed7i` hay ``. 
    - Agent phải đảm bảo file được lưu dưới định dạng **UTF-8**. 
    - Khi viết `MarkupText`, nếu chuỗi có chứa dấu nháy hoặc ký tự đặc biệt, hãy sử dụng dấu nháy đơn `'` bao ngoài dấu nháy kép `"` hoặc ngược lại để tránh lỗi lồng chuỗi.