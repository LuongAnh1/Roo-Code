import sys
import os
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from skills.fami_lib import *
from skills.fami_effects import *

class Scene2_MainBody(FaMIBaseScene):
    def construct(self):
        title = self.create_title("BỘ BA SỨC MẠNH", "TỐI ƯU HÓA")
        
        # ==========================================
        # 🎨 VÙNG SÁNG TẠO (CREATIVE ZONE)
        # ==========================================
        
        # --- THÀNH PHẦN CHO ĐOẠN 1 (AI VÀ CON SỐ) ---
        ai_circle = Circle(radius=1.5, color=FAMI_CYAN, stroke_width=2)
        ai_hex = RegularPolygon(n=6, color=FAMI_BLUE, fill_opacity=0.15).scale(1.6)
        ai_text = Text("AI", font="Segoe UI", font_size=65, weight=BOLD, color=WHITE)
        ai_logo = VGroup(ai_hex, ai_circle, ai_text).move_to(ORIGIN)
        
        numbers = VGroup()
        for _ in range(50):
            num = Text(str(np.random.randint(0, 255)), font="Consolas", font_size=24, color=ACCENT)
            angle = np.random.uniform(0, 2*PI)
            radius = np.random.uniform(3.5, 6.0)
            num.move_to(np.array([np.cos(angle)*radius, np.sin(angle)*radius, 0]))
            numbers.add(num)
        
        # --- THÀNH PHẦN CHO ĐOẠN 2 (3 SỨC MẠNH) ---
        color_icon = VGroup(
            Square(side_length=0.8, color=RED, fill_opacity=0.8),
            Square(side_length=0.8, color=GREEN, fill_opacity=0.8),
            Square(side_length=0.8, color=BLUE, fill_opacity=0.8)
        ).arrange(RIGHT, buff=0.1)
        color_text = Text("MÀU SẮC", font="Segoe UI", font_size=32, weight=BOLD, color=ACCENT)
        color_grp = VGroup(color_icon, color_text).arrange(DOWN, buff=0.3)
        
        space_icon = NumberPlane(
            x_range=[-2, 2, 1], y_range=[-2, 2, 1],
            x_length=2.6, y_length=2.6,
            background_line_style={"stroke_color": TEAL, "stroke_width": 2, "stroke_opacity": 0.5}
        )
        space_text = Text("KHÔNG GIAN", font="Segoe UI", font_size=32, weight=BOLD, color=ACCENT)
        space_grp = VGroup(space_icon, space_text).arrange(DOWN, buff=0.3)
        
        axes = Axes(
            x_range=[-3, 3], y_range=[0, 1],
            x_length=2.6, y_length=1.5,
            axis_config={"include_numbers": False, "stroke_width": 2}
        )
        curve = axes.plot(lambda x: np.exp(-x**2), color=YELLOW, stroke_width=4)
        norm_icon = VGroup(axes, curve)
        norm_text = Text("CHUẨN HÓA", font="Segoe UI", font_size=32, weight=BOLD, color=ACCENT)
        norm_grp = VGroup(norm_icon, norm_text).arrange(DOWN, buff=0.3)
        
        three_powers = VGroup(color_grp, space_grp, norm_grp).arrange(RIGHT, buff=0.5)
        if three_powers.height > 6.5:
            three_powers.scale_to_fit_height(6.5)
        if three_powers.width > 7.0:
            three_powers.scale_to_fit_width(7.0)
        three_powers.move_to(UP*0.5)
        
        # --- THÀNH PHẦN CHO ĐOẠN 3 (LĂNG KÍNH & MẠNG NƠ RON) ---
        # Ý tưởng mới: Vẽ Lăng kính thực sự (có tia sáng trắng chiếu vào và tán sắc ra RGB)
        prism_triangle = RegularPolygon(n=3, color=FAMI_CYAN, stroke_width=4, fill_color=BLACK, fill_opacity=0.8).scale(2.2)
        prism_triangle.move_to(UP * 0.5) # Đặt vị trí chuẩn trước khi vẽ các tia
        
        verts = prism_triangle.get_vertices()
        l1 = Line(verts[0], prism_triangle.get_center(), color=FAMI_CYAN, stroke_opacity=0.5)
        l2 = Line(verts[1], prism_triangle.get_center(), color=FAMI_CYAN, stroke_opacity=0.5)
        l3 = Line(verts[2], prism_triangle.get_center(), color=FAMI_CYAN, stroke_opacity=0.5)
        
        # Tọa độ chính xác trên mặt của tam giác (Không dùng get_left vì bounding box sẽ gây ra khoảng trống)
        left_mid = (verts[0] + verts[1]) / 2
        right_mid = (verts[0] + verts[2]) / 2
        
        # Tia sáng (Light beams) bám chính xác vào cạnh
        beam_in = Line(left_mid + LEFT*3.0 + DOWN*1.0, left_mid, color=WHITE, stroke_width=8)
        beam_out_r = Line(right_mid, right_mid + RIGHT*3.0 + UP*1.2, color=RED, stroke_width=5)
        beam_out_g = Line(right_mid, right_mid + RIGHT*3.0 + UP*0.1, color=GREEN, stroke_width=5)
        beam_out_b = Line(right_mid, right_mid + RIGHT*3.0 + DOWN*1.0, color=BLUE, stroke_width=5)
        
        prism_body = VGroup(beam_in, beam_out_r, beam_out_g, beam_out_b, prism_triangle, l1, l2, l3)
        
        prism_text = Text("LĂNG KÍNH ĐẠI SỐ", font="Segoe UI", font_size=32, weight=BOLD, color=ACCENT)
        prism_text.next_to(prism_triangle, DOWN, buff=0.5)
        
        prism_grp = VGroup(prism_body, prism_text) # Không dùng move_to ở đây nữa để tránh xô lệch tọa độ
        
        layers_config = [4, 5, 4]
        colors_nn = [FAMI_CYAN, ORANGE, SUCCESS]
        nn_layers = VGroup()
        for i, count in enumerate(layers_config):
            layer = VGroup(*[Circle(radius=0.22, color=colors_nn[i], fill_opacity=1) for _ in range(count)])
            layer.arrange(DOWN, buff=0.4)
            nn_layers.add(layer)
        nn_layers.arrange(RIGHT, buff=1.5)
        
        edges = VGroup()
        for i in range(len(nn_layers)-1):
            for node_a in nn_layers[i]:
                for node_b in nn_layers[i+1]:
                    edges.add(Line(node_a.get_center(), node_b.get_center(), stroke_width=2, color=WHITE, stroke_opacity=0.3))
        
        logic_structure = VGroup(edges, nn_layers).move_to(ORIGIN)
        logic_structure.scale_to_fit_width(6.5)
        all_nodes = VGroup(*[node for layer in nn_layers for node in layer])

        # ==========================================
        # 🎬 ĐỒNG BỘ VOICEOVER CHUẨN
        # ==========================================
        
        # ĐOẠN MỚI: Vậy là thay vì nhìn thấy tai hay mắt mèo...
        with self.voiceover(text="Vậy là, thay vì nhìn thấy tai hay mắt mèo như chúng ta, AI bắt đầu hành trình bằng việc giải mã những con số.") as tracker:
            self.update_subtitle("AI bắt đầu hành trình bằng việc giải mã những con số.")
            
            # Hiện Logo AI và Title nhanh
            self.play(FadeIn(ai_logo), Write(title), run_time=0.5)
            self.play(FadeIn(numbers), run_time=0.3)
            
            # Các con số hút vào tâm AI liên tục, dàn đều thời gian thoại
            self.play(
                LaggedStart(
                    *[m.animate.move_to(ai_logo.get_center()).scale(0.2).set_opacity(0) for m in numbers],
                    lag_ratio=0.08
                ),
                run_time=tracker.duration * 0.7
            )
            
            # Dọn dẹp
            self.play(FadeOut(ai_logo), run_time=0.4)

        with self.voiceover(text="Biến đổi màu sắc, biến đổi không gian và chuẩn hóa, đây chính là bộ ba sức mạnh giúp chúng ta tối ưu hóa dòng chảy của các con số.") as tracker:
            self.update_subtitle("Biến đổi màu sắc, không gian và chuẩn hóa...")
            
            # Xuất hiện tuần tự (< 1.5s)
            anim_c, r_c = skill_pop_in(color_grp)
            anim_s, r_s = skill_pop_in(space_grp)
            anim_n, r_n = skill_pop_in(norm_grp)
            
            self.play(anim_c, rate_func=r_c, run_time=min(1.0, tracker.duration * 0.3))
            self.update_subtitle("đây chính là bộ ba sức mạnh giúp chúng ta tối ưu hóa dòng chảy của các con số.")
            self.play(anim_s, rate_func=r_s, run_time=min(1.0, tracker.duration * 0.3))
            self.play(anim_n, rate_func=r_n, run_time=min(1.0, tracker.duration * 0.3))

        with self.voiceover(text="Khi dữ liệu được xử lý qua lăng kính của Đại số tuyến tính") as tracker:
            self.update_subtitle("Khi dữ liệu được xử lý qua lăng kính của Đại số tuyến tính...")
            self.play(
                FadeOut(three_powers), FadeIn(prism_grp),
                run_time=min(1.2, tracker.duration * 0.8)
            )
            
        with self.voiceover(text="nó không còn là những pixel rời rạc, mà đã trở thành một cấu trúc logic hoàn hảo.") as tracker:
            self.update_subtitle("nó không còn là những pixel rời rạc...")
            self.play(
                FadeOut(prism_grp), FadeIn(logic_structure),
                run_time=min(1.2, tracker.duration * 0.5)
            )
            self.update_subtitle("mà đã trở thành một cấu trúc logic hoàn hảo")
            self.play(LaggedStartMap(Indicate, all_nodes, lag_ratio=0.1), run_time=min(1.5, tracker.duration * 0.3))

        with self.voiceover(text="Đây chính là bước đệm quyết định, biến những bức ảnh thô thành một nguồn tri thức sẵn sàng để mạng nơ-ron khai phá.") as tracker:
            self.update_subtitle("Đây chính là bước đệm quyết định...")
            
            glow = logic_structure.copy().set_stroke(width=5, opacity=0.5).set_color(SUCCESS)
            self.play(FadeIn(glow, scale=1.1), run_time=min(1.2, tracker.duration * 0.5))
            self.update_subtitle("biến những bức ảnh thô thành một nguồn tri thức sẵn sàng để mạng nơ-ron khai phá.")
            self.play(FadeOut(glow), run_time=min(1.2, tracker.duration * 0.4))
            
        self.finish_scene()
