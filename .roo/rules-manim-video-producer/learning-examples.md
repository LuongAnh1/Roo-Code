# NHẬT KÝ LỖI & CÁCH KHẮC PHỤC (CRASH PREVENTION)

Agent BẮT BUỘC phải đối chiếu code với danh sách này trước khi chạy lệnh render để đảm bảo không mắc các lỗi "ảo tưởng cú pháp" gây Crash (văng) chương trình.

---

## 1. LỖI TỌA ĐỘ VÀ KHÔNG GIAN (VGROUP & TEXT)
- **❌ SAI (Lỗi Trống Tọa Độ)**: `VGroup().align_to(...)` hoặc `Text("").next_to(...)` hoặc `Text(" ").match_y(...)`
  *(Lỗi: `IndexError: too many indices`. Do Mobject rỗng hoặc chỉ có dấu cách không có điểm (points), Manim không thể tính toán tọa độ).*
- **❌ SAI (Lỗi Tâm Bị Lệch)**: Dùng `VGroup` đang trong vòng lặp `add()` làm mốc cho lệnh `next_to`. Chữ sẽ bị bay lung tung vì tâm VGroup thay đổi liên tục.
- **✅ ĐÚNG (Cách làm chuẩn)**:
  1. Dùng một vật thể đã có sẵn trên màn hình làm mốc ban đầu (`last_item = search_bar`).
  2. Các vật thể sau bám vào vật thể trước đó (`new_item.next_to(last_item)`).
  3. CẤM dùng các hàm vị trí trên một Group rỗng. Đối với dấu cách, hãy dùng biến `buff` để cộng dồn khoảng cách thay vì tạo `Text(" ")`.

## 2. LỖI CÚ PHÁP ANIMATION (.animate)
- **❌ SAI**: `self.play(obj.animate(path_arc=PI).move_to(UP))` *(animate không phải là hàm).*
- **❌ SAI**: `self.play(obj.animate().scale(2))` *(Thừa dấu ngoặc).*
- **✅ ĐÚNG**: `self.play(obj.animate.move_to(UP))`
- **✅ ĐÚNG**: `self.play(obj.animate.move_to(UP), path_arc=PI/3)` (Các tham số phụ nằm trong self.play).

## 3. LỖI TOÁN HỌC & MATH TEX
- **❌ SAI (Thiếu thư viện)**: `m.set_opacity(sin(self.renderer.time))` *(Lỗi `NameError`)*.
- **✅ ĐÚNG**: Phải có `import math` hoặc `import numpy as np` ở đầu file và gọi `math.sin()` hoặc `np.sin()`.
- **❌ SAI (Lỗi LaTeX)**: `MathTex("\frac{a}{b}")` *(Lỗi ký tự escape).*
- **✅ ĐÚNG**: LUÔN sử dụng tiền tố **r** (raw string): `MathTex(r"\frac{a}{b}")`.

## 4. LỖI TIẾNG VIỆT & UNICODE
- **❌ SAI**: Dùng `BulletedList("Ý 1", "Ý 2")`. 
  *(Lỗi: `Latex Error`. BulletedList sử dụng backend LaTeX, không tương thích tốt với Unicode Tiếng Việt).*
- **✅ ĐÚNG**: Dùng `VGroup` và `Text` thủ công:
  ```python
  list = VGroup(
      Text("• Ý 1", font="Segoe UI"), 
      Text("• Ý 2", font="Segoe UI")
  ).arrange(DOWN, aligned_edge=LEFT)
  ```

## 5. LỖI TRÀN RAM DÀNH CHO UPDATERS (CRITICAL)
- **❌ SAI** (Sinh rác bộ nhớ):
  ```python
  mob.add_updater(lambda m: m.become(Text("...")))
  ```  
  *Lỗi: Tạo hàng nghìn object Text mới mỗi giây sẽ làm treo máy/crash RAM*
- **❌ SAI** (Phình to vô hạn): `mob.add_updater(lambda m: m.scale(1.1))`
- **✅ ĐÚNG**: Chỉ dùng Updater để cập nhật thuộc tính dựa trên thời gian thực `self.renderer.time`:
  ```python
    mob.set_scale(initial_scale * (1 + 0.1 * np.sin(self.renderer.time * 5)))
  ```

## 6. LỖI THANH BIỂU ĐỒ (PROGRESS BAR)
- **❌ SAI**: Khởi tạo `height=0` rồi dùng `.animate.set(height=5)`. (Lỗi chia cho 0 hoặc dãn nở 2 chiều).
- **✅ ĐÚNG**: Khởi tạo mỏng và ép neo đáy.  
  ```python
    bar = Rectangle(height=0.01, width=1.5)
    bar.align_to(ground_line, DOWN)
    self.play(bar.animate.stretch_to_fit_height(5).align_to(ground_line, DOWN))
  ```
## 10. CÁC LỖI HỆ THỐNG (SYSTEM ERRORS)
- **Lỗi `ModuleNotFoundError: No module named 'pkg_resources'`**: 
  - Đừng sửa code. 
  - Đây là lỗi thiếu thư viện `setuptools`.
  - **Cách fix**: Chạy lệnh `pip install setuptools` trong terminal.

## 11. CÁC LỖI MỚI TỰ HỌC (AUTO-LEARNED ERRORS)
*Agent: Nếu bạn tự động sửa thành công một lỗi code mới trong quá trình Auto-Debug, hãy dùng công cụ Edit File để ghi chép lỗi đó vào ngay dưới dòng này theo đúng format ❌ SAI / ✅ ĐÚNG*

### Lỗi Logic Chuyển Cảnh (VGroup lồng nhau)
- **❌ SAI**: Dùng `ReplacementTransform` để chuyển từ một Mobject (vd: `MathTex`) thành một `VGroup` phức tạp đã được `arrange`. Manim sẽ không thể tính toán chính xác phép biến đổi cho từng phần tử con, gây lỗi tọa độ hoặc animation không như ý.
- **❌ SAI**: Dùng `VGroup` lồng nhau (`VGroup` của các `VGroup` đã `arrange`) và cố gắng `animate` các nhóm con. Tọa độ sẽ bị xung đột.
- **✅ ĐÚNG**: Với các chuyển cảnh phức tạp, hãy dùng cặp `FadeOut(old_group)` và `FadeIn(new_group)`. Cách này đảm bảo layout ổn định, dễ quản lý và trông vẫn chuyên nghiệp.

### Lỗi Cú pháp MarkupText với f-string
- **❌ SAI**: `MarkupText('f.e. “<span color='{ACCENT}'>...</span>”')`. Dấu nháy đơn bên ngoài và bên trong f-string gây lỗi `SyntaxError`.
- **✅ ĐÚNG**: Dùng dấu nháy kép cho thuộc tính của thẻ HTML: `MarkupText(f'...“<span color="{ACCENT}">...</span>”...')`. Hoặc dùng ba dấu nháy kép/đơn để bao bọc toàn bộ chuỗi.

