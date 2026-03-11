# BẢNG ĐỐI CHIẾU LỖI SAI & CÁCH KHẮC PHỤC (ANTI-PATTERNS)

Agent BẮT BUỘC phải kiểm tra danh sách này trước khi xuất code để đảm bảo không mắc các lỗi "ảo tưởng" cú pháp.

---

## 1. Cú pháp Animation (.animate)
- **❌ SAI**: `self.play(obj.animate(path_arc=PI).move_to(UP))`  
  *(Lỗi: animate không phải là hàm, không được có ngoặc đơn ngay sau nó).*
- **❌ SAI**: `self.play(obj.animate().scale(2))`  
  *(Lỗi: Thừa dấu ngoặc).*
- **✅ ĐÚNG**: `self.play(obj.animate.move_to(UP))`
- **✅ ĐÚNG (với hiệu ứng cong)**: `self.play(obj.animate.move_to(UP), path_arc=PI/3)`
- **QUY TẮC**: `.animate` là một thuộc tính. Các tham số như `path_arc`, `rate_func`, `run_time` phải nằm trong hàm `self.play()`.

---

## 2. Công thức Toán học (MathTex)
- **❌ SAI**: `MathTex("\frac{a}{b}")`  
  *(Lỗi: \f sẽ bị Python hiểu là ký tự đặc biệt 'form feed', gây lỗi render LaTeX).*
- **✅ ĐÚNG**: `MathTex(r"\frac{a}{b}")`
- **QUY TẮC**: Luôn sử dụng tiền tố **r** (raw string) cho mọi chuỗi MathTex có dấu gạch chéo ngược `\`.

---

## 3. Manim-Voiceover Tracker
- **❌ SAI**: `self.wait(tracker.last_wait_time)`
- **❌ SAI**: `self.wait(tracker.remaining_duration)`  
  *(Lỗi: Các thuộc tính này không tồn tại trong phiên bản hiện tại).*
- **✅ ĐÚNG**: `run_time=tracker.duration`
- **✅ ĐÚNG**: `self.wait(tracker.duration * 0.1)` (nếu muốn nghỉ một chút).
- **QUY TẮC**: Chỉ sử dụng `tracker.duration`. Hệ thống sẽ tự động chờ hết âm thanh khi kết thúc khối `with self.voiceover`.

---

## 4. Hiệu suất & Updaters (CRITICAL)

- **❌ SAI (Lỗi Tràn Bộ Nhớ)**: 
  ```python
  mob.add_updater(lambda m: m.become(Text("...")))
  ```
  (Lỗi: Tạo hàng nghìn object Text mới mỗi giây sẽ làm treo máy/crash RAM).

- **❌ SAI (Lỗi Phình To Vô Hạn)**:
```python
mob.add_updater(lambda m: m.scale(1.1))
```
(Lỗi: Tỉ lệ bị nhân dồn liên tục mỗi frame khiến vật thể biến mất).

- **❌ SAI: self.get_time()**
(Lỗi: Hàm này không tồn tại trong Manim Community).
✅ ĐÚNG: self.renderer.time
✅ ĐÚNG (Số chạy): Dùng DecimalNumber và ChangeDecimalToValue.
✅ ĐÚNG (Nhấp nháy/Pulse):
mob.set_scale(initial_scale * (1 + 0.1 * np.sin(self.renderer.time * 5)))

## 5. Thanh biểu đồ & Progress Bar
❌ SAI: Khởi tạo height=0 rồi dùng .animate.set(height=5).
(Lỗi: Vật thể sẽ giãn nở từ tâm ra hai hướng hoặc bị lỗi tỉ lệ 0).
✅ ĐÚNG:
```python
bar = Rectangle(height=0.01, width=1.5, ...) # Khởi tạo mỏng
bar.align_to(ground_line, DOWN) # Đặt điểm neo ở đáy
self.play(bar.animate.stretch_to_fit_height(5).align_to(ground_line, DOWN))
```
QUY TẮC: Luôn dùng stretch_to_fit_height và phải đi kèm .align_to(..., DOWN) để thanh bar "mọc" từ dưới lên.

## 6. Tiếng Việt & Font chữ
❌ SAI: Text("Tiếng Việt", font="Times New Roman")
(Lỗi: Font này thường bị lỗi dấu Ậ, Ế, Ủ trên nhiều hệ thống).
✅ ĐÚNG: Text("Tiếng Việt", font="Segoe UI") (Ưu tiên số 1 trên Windows).
✅ ĐÚNG: Text("Tiếng Việt", font="Arial") (Ưu tiên số 2).
QUY TẮC: Nếu thấy ký tự lạ hoặc ô vuông trong file render, Agent phải đổi sang Segoe UI ngay lập tức.

## 7. Bố cục Video Dọc (9:16 TikTok)
❌ SAI: Dùng tọa độ UP * 2 hoặc DOWN * 2.
(Lỗi: Màn hình dọc TikTok rất dài, vị trí này sẽ bị quá sát trung tâm).
✅ ĐÚNG:
Tiêu đề: to_edge(UP, buff=1.5)
Chú thích đáy: to_edge(DOWN, buff=2.0)
Công thức chính: ORIGIN hoặc UP * 0.5
QUY TẮC: Frame dọc có frame_height = 16. Phải sử dụng không gian từ +7 đến -7 một cách hợp lý.

## 8. Quản lý biến & Logic
❌ SAI: Gọi self.play(FadeIn(percent)) khi chưa khai báo percent = ....
✅ ĐÚNG: Luôn định nghĩa đối tượng (Mobjects) ở dòng trên, sau đó mới gọi Animation ở dòng dưới.
- QUY TẮC: Kiểm tra NameError bằng cách rà soát biến trước khi render.

## 9. Lỗi hàm toán học thiếu thư viện (Math NameError)
- **❌ SAI**: `comment.add_updater(lambda m: m.set_opacity(sin(self.renderer.time)))`
  *(Lỗi: NameError: name 'sin' is not defined)*
- **✅ ĐÚNG**: 
  ```python
  import math # Phải có ở đầu file
  ...
  comment.add_updater(lambda m: m.set_opacity(math.sin(self.renderer.time)))
  ```
- QUY TẮC: Mọi hàm toán học bên trong add_updater hoặc tính toán tọa độ phải đi kèm với math. hoặc np.

## 10. CÁC LỖI MỚI TỰ HỌC (AUTO-LEARNED ERRORS)
- **❌ SAI**: `VGroup` đang tăng trưởng làm mốc `next_to`.
  *(Lỗi: Khi `VGroup` dài ra, tâm của nó thay đổi, khiến các chữ cái sau bị đẩy đi một cách hỗn loạn.)*
- **✅ ĐÚNG**: Dùng một biến `last_item` để làm mốc cho item tiếp theo.
- **QUY TẮC**: Khi làm hiệu ứng Typing hoặc dàn hàng ngang thủ công, hãy dùng một biến `last_item` để làm mốc cho item tiếp theo, thay vì dùng `next_to` vào một `VGroup` đang tăng trưởng.


- **❌ SAI (Lỗi Trống Tọa Độ)**: `VGroup().align_to(...)` hoặc `Text("").next_to(...)` hoặc `Text(" ").move_to(...)`
  *(Lỗi: `IndexError: too many indices for array`. Do Mobject rỗng không có điểm (points), Manim không thể tính toán tọa độ để căn lề).*
- **✅ ĐÚNG**: 
    1. Chỉ căn lề sau khi đã thêm ít nhất 1 vật thể vào Group.
    2. Hoặc xác định một điểm mốc trước: `point = other_obj.get_right() + RIGHT*0.5`.
    3. Đặt vật thể đầu tiên vào điểm mốc đó, rồi các vật thể sau mới `next_to` vào vật thể đầu tiên.
- **QUY TẮC**: CẤM tuyệt đối sử dụng các hàm vị trí (`align_to`, `next_to`, `move_to`, `shift`) trên một `VGroup` rỗng hoặc `Text` không chứa ký tự hiển thị được.

- **❌ SAI**: Sử dụng `BulletedList` cho Tiếng Việt.
  *(Lỗi: Latex Error. BulletedList dùng LaTeX truyền thống không hỗ trợ tốt Unicode Tiếng Việt).*
- **✅ ĐÚNG**: Dùng `VGroup` chứa các dòng `Text` và tự thêm dấu chấm `•`.
  ```python
  list = VGroup(Text("• Ý 1", font="Segoe UI"), Text("• Ý 2", font="Segoe UI")).arrange(DOWN, aligned_edge=LEFT)
  ```
  
- **❌ SAI**: `self.wait(tracker.duration - 1.5)`
*(Lỗi: ValueError nếu kết quả ra số âm).*
- **✅ ĐÚNG**: Không dùng wait thủ công trong khối voiceover, hãy để thư viện tự động chờ đến khi hết âm thanh.


