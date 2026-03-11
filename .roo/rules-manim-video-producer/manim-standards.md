# TIÊU CHUẨN VIẾT CODE MANIM COMMUNITY (BEST PRACTICES)

Đây là bộ quy chuẩn BẮT BUỘC về cú pháp lập trình và hiệu ứng nâng cao. Agent phải tuân thủ để code chạy mượt mà, không sinh lỗi và đạt chất lượng "Premium".

## 0. Quy định về Thư viện Toán học (CRITICAL)
- **Import bắt buộc**: Luôn đảm bảo có `import math` và `import numpy as np` ở đầu file. Manim xử lý tọa độ bằng mảng Numpy.
- **TUYỆT ĐỐI CẤM** sử dụng các hàm toán học đứng độc lập như `sin()`, `cos()`, `pi()`.
- **Cú pháp chuẩn**:
  - Khi tính toán số liệu thông thường: Dùng `math.sin()`, `math.cos()`, `math.pi`.
  - Khi thao tác với tọa độ, trục, hoặc Updater của Manim: Ưu tiên dùng `np.sin()`, `np.cos()`, `np.pi`.

## 1. Cú pháp Hoạt ảnh (Animation Syntax)
- **LaTeX**: Luôn dùng `MathTex(r"...")` (có tiền tố `r` để tránh lỗi ký tự escape `\`).
- **Animation Method**: Bắt buộc dùng `obj.animate.method(...)`. CẤM dùng `obj.animate(...)`.
- **Time**: Luôn dùng `self.renderer.time` cho các hiệu ứng thời gian thực. (CẤM dùng `self.get_time()`).
- **Updaters an toàn**: KHÔNG khởi tạo Mobject mới bên trong hàm updater (gây tràn RAM). 
  - *Ví dụ nhấp nháy chuẩn:* `mob.add_updater(lambda m: m.set_scale(1 + 0.05 * np.sin(self.renderer.time * 5)))`

## 2. Quản lý Đối tượng & Chuyển cảnh
- **Thứ tự logic**: Khai báo và tùy chỉnh toàn bộ Mobject (màu sắc, tọa độ, kích thước) ở các dòng trên. Sau đó mới đưa vào `self.play(...)` ở dòng dưới.
- **Gom nhóm**: Luôn sử dụng `VGroup(obj1, obj2)` để quản lý cụm đối tượng có liên quan (ví dụ: Tiêu đề + Đường gạch chân).
- **Dọn dẹp Scene (Cleanup)**: Khi chuyển sang ý mới, CẤM dùng `self.clear()`. 
  - *Cú pháp chuẩn:* `self.play(FadeOut(*self.mobjects))` để màn hình mờ dần đi một cách sang trọng.

## 3. Nâng cấp Thẩm mỹ & Hiệu ứng Chuyên nghiệp (Premium Look)
Agent đóng vai trò là Giám đốc Nghệ thuật, BẮT BUỘC phải áp dụng các kỹ thuật sau để video trông "đắt tiền":

- **1. Gradient Colors (Màu chuyển sắc)**: 
  Thay vì dùng 1 màu đơn điệu cho khối lớn, hãy dùng mảng màu:
  `obj.set_color([PRIMARY, ACCENT])` hoặc `obj.set_fill([COLOR1, COLOR2], opacity=1)`

- **2. Layering (Tạo chiều sâu cho Text)**: 
  Khi Text đè lên đồ thị hoặc mớ bòng bong, LUÔN thêm nền mờ đằng sau để dễ đọc:
  `bg = BackgroundRectangle(my_text, color=BLACK, fill_opacity=0.6, buff=0.2)`
  `self.add(bg, my_text)`

- **3. Hiệu ứng "Juicy/Bouncy" (Sinh động)**: 
  Không dùng `FadeIn(obj)` hay `Create(obj)` đơn điệu. Hãy kết hợp Scale, Shift và Rate Functions:
  - *Mẫu hiện ra nảy lên:* 
    `self.play(FadeIn(obj, scale=0.5, shift=UP*0.5), rate_func=rate_functions.ease_out_back)`
  - *Mẫu vẽ cơ khí mượt mà:* 
    `self.play(Create(obj), rate_func=rate_functions.smooth)`

- **4. Drop Shadow (Bóng đổ Hiện đại)**:
  Tạo chiều sâu 3D cho các hộp thông tin (Box) bằng cách copy chính nó làm bóng:
  ```python
  box = RoundedRectangle(corner_radius=0.2, color=PRIMARY, fill_opacity=0.2)
  shadow = box.copy().set_color(BLACK).set_fill(opacity=0.4).set_stroke(width=0).shift(DOWN*0.1 + RIGHT*0.1)
  ui_group = VGroup(shadow, box) # Phải add shadow trước để nằm dưới
  ```
- 5. Neon Glow (Hiệu ứng Phát sáng):
Khi cần nhấn mạnh (Highlight) một từ khóa hay công thức, tạo hào quang phát sáng:
```python
# Tạo viền dày, mờ ảo nằm dưới vật thể chính
glow = main_obj.copy().set_stroke(color=ACCENT, width=15, opacity=0.3).set_fill(opacity=0)
self.play(FadeIn(glow))
```

## 4. QUY TẮC CLASS KẾ THỪA (MANDATORY)
- **CẤM** kế thừa trực tiếp từ `VoiceoverScene`.
- Mọi Scene (từ Scene1 đến Scene4) **BẮT BUỘC PHẢI KẾ THỪA** từ `FaMIBaseScene` ở trong file `manim-standards.md`. 
- `FaMIBaseScene` đã tự động xử lý Logo FaMI và `set_speech_service`, Agent KHÔNG ĐƯỢC viết lại các lệnh này trong hàm `construct()`.
- **Vị trí Tiêu đề:** Vì Logo đã chiếm ngự trên cùng (`to_edge(UP)`), mọi Tiêu đề (Title) của Scene phải được định vị bằng lệnh: `title.next_to(self.logo, DOWN,  weight=BOLD, buff=0.5)`. Cấm dùng `to_edge(UP)` cho Title kẻo bị đè lên logo.
- **File mẫu tham chiếu**: Luôn lấy file `test_logo.py` làm chuẩn mực về: khoảng cách logo, độ đậm của chữ tiêu đề và cách căn lề theo chiều dọc.

## 5. QUY TẮC ĐỒNG BỘ NÂNG CAO (TIMING CONTROL)
- **CẤM** suy đoán thời gian bằng cách dùng `self.wait(2)`.
- **BẮT BUỘC** sử dụng kỹ thuật phân đoạn bằng `tracker.get_remaining_duration()`:
  - Nếu câu thoại có 3 ý: A, B, C. 
  - Chia nhỏ Animation: `self.play(Effect_A, run_time=tracker.duration * 0.3)`.
  - Kiểm tra thời gian còn lại: `self.wait(tracker.get_remaining_duration())`.
- **Luôn luôn kết thúc bằng**: `self.wait(tracker.get_remaining_duration())` sau khi các animation chính đã xong để đảm bảo hình ảnh đứng yên khớp với âm thanh.

## 6. QUY TẮC HIỆU ỨNG GÕ CHỮ (XỬ LÝ KHOẢNG TRẮNG)
Để tránh lỗi `IndexError` khi gặp dấu cách, Agent BẮT BUỘC tuân thủ logic sau:
1. **Bỏ qua dấu cách**: KHÔNG tạo `Text(" ")`. 
2. **Cộng dồn khoảng cách**: Nếu gặp dấu cách, hãy tăng biến `buff` cho chữ cái kế tiếp.
3. **Logic mẫu chuẩn (Bắt buộc bắt chước)**:
    ```python
    last_char = magnifying_glass # Mốc ban đầu là vật thể có thật
    current_buff = 0.3 # Buff khởi đầu
    
    for i, char in enumerate(search_text_str):
        if char == " ":
            current_buff = 0.3 # Gặp dấu cách thì tăng buff cho chữ sau, không tạo object
            continue
            
        new_char = Text(char, font="Segoe UI", font_size=40, color=TEXT_COLOR)
        new_char.next_to(last_char, RIGHT, buff=current_buff)
        
        # CHỈ match_y trên vật thể có points
        new_char.match_y(search_bar)
        
        self.play(FadeIn(new_char), run_time=0.08)
        
        # Cập nhật mốc và trả buff về mặc định
        last_char = new_char
        current_buff = 0.08 
    ```

## 7. QUY TẮC VỀ TEXT & MARKUP (ANTI-CRASH)
- **CẤM TUYỆT ĐỐI**: Không sử dụng `get_part_by_text()` hoặc `set_color_by_text()` với đối tượng `Text`. Các hàm này không tồn tại trong Manim Community và sẽ gây lỗi `TypeError`.
- **MARKUPTEXT**: Khi cần tô màu từng từ trong câu hoặc dùng ký tự đặc biệt (như €, $, @), BẮT BUỘC dùng `MarkupText` và thẻ `<span>`.
    - *Ví dụ:* `MarkupText(f'Chữ <span color="{YELLOW}">Vàng</span>', font="Segoe UI")`
- **KÝ TỰ ĐẶC BIỆT**: Hạn chế dùng các ký tự hiếm gặp trực tiếp trong `Text` nếu định dùng chúng làm mốc để animation, vì dễ lỗi Encoding.

## 8. QUY TẮC DÙNG THƯ VIỆN SKILLS
- **Kế thừa**: Luôn luôn dùng `class SceneName(FaMIBaseScene):`.
- **Tiêu đề**: Luôn dùng `title = self.create_title("Dòng 1", "Dòng 2")`. Hàm này đã tự động xử lý font đậm và vị trí dưới logo.
- **Phụ đề**: Trong mỗi khối `voiceover`, lệnh đầu tiên phải là `self.update_subtitle(nội_dung)`.
- **Màu sắc**: Sử dụng các biến màu có sẵn: `FAMI_CYAN`, `ACCENT`, `SUCCESS`, `DANGER`.