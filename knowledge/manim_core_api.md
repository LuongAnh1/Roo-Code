# Manim Core API Cheat Sheet

## 1. Mobjects (Objects)
- **Shapes**: `Circle(radius=1.0)`, `Square(side_length=2.0)`, `Rectangle(width=4.0, height=2.0)`.
- **Text**: `Text("Nội dung", font="Segoe UI", font_size=40)`.
- **Math**: `MathTex(r"a^2 + b^2 = c^2")` (Luôn dùng tiền tố r).
- **Groups**: `VGroup(obj1, obj2).arrange(DOWN, buff=0.5)`.

## 2. Positioning (Vị trí)
- `obj.to_edge(UP/DOWN/LEFT/RIGHT, buff=1.0)`
- `obj.next_to(target, direction=DOWN, buff=0.5)`
- `obj.shift(UP * 2 + LEFT * 1)`
- `obj.move_to(ORIGIN)` hoặc `obj.move_to(target.get_center())`

## 3. Animations (Hiệu ứng)
- `Create(obj)`: Vẽ hình khối.
- `Write(text)`: Viết chữ.
- `FadeIn(obj, shift=UP)`: Hiện hình với hướng bay.
- `FadeOut(obj)`: Biến mất.
- `ReplacementTransform(old_obj, new_obj)`: Biến đổi vật thể này thành vật thể kia.
- `Indicate(obj, color=YELLOW)`: Làm vật thể nhấp nháy/phóng to để gây chú ý.

## 4. Updaters (Hiệu ứng thời gian)
- **Lấy thời gian**: `self.renderer.time`.
- **Cú pháp**: `obj.add_updater(lambda m: m.set_opacity(abs(math.sin(self.renderer.time))))`.
- **Lưu ý**: Luôn gọi `obj.remove_updater(obj.updaters[0])` khi kết thúc scene để giải phóng bộ nhớ.

## 5. Agent Note
- CẤM: `obj.animate().method()`.
- ĐÚNG: `obj.animate.method()`.
- Luôn sử dụng `VGroup` để quản lý layout phức tạp.