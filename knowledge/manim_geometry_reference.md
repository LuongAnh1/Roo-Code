# MANIM GEOMETRY & LAYOUT REFERENCE

## 1. CÁC HÌNH KHỐI CƠ BẢN (SHAPES)
- **Rectangle**: `Rectangle(width=4, height=2, color=WHITE, fill_opacity=0.5)`
- **Circle**: `Circle(radius=1, color=FAMI_CYAN)`
- **Rounded Box**: `RoundedRectangle(corner_radius=0.2, width=3, height=1.5)`
- **Polygon**: `RegularPolygon(n=5)` (Ngũ giác), `Triangle()` (Tam giác).

## 2. QUẢN LÝ VỊ TRÍ (POSITIONING)
- **Hệ trục Y**: Nhớ rằng màn hình dọc có Y từ -8 đến +8.
- **Move to Point**: `obj.move_to(np.array([x, y, 0]))`
- **Align**: `obj.align_to(other_obj, LEFT)` (Căn lề trái theo vật thể khác).
- **Match**: `obj.match_x(other_obj)` (Ép cùng trục dọc), `obj.match_y(other_obj)` (Ép cùng trục ngang).

## 3. LỚP PHỦ (LAYERING)
- **z_index**: Nếu muốn vật thể nằm đè lên cái khác, dùng `.set_z_index(10)`.
- **Foreground**: Sử dụng `self.add_foreground_mobject(obj)` để khóa vật thể luôn hiện ở trên cùng (như Logo).