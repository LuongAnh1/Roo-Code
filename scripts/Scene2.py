import sys
import os
# [QUY TẮC 1: HACK PATH]
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from skills.fami_lib import *

class Scene2_HoanThien_Final(FaMIBaseScene):
    def construct(self):
        # ==========================================
        # 🎨 KHỞI TẠO ASSETS (PRE-LOADING)
        # ==========================================
        GAP = 1.0
        title = self.create_title("BẢN CHẤT CỦA ẢNH", "LÀ MA TRẬN SỐ")

        # --- PHẦN 1: ẢNH & KHỐI 3D ---
        cat_img = ImageMobject("assets/cat.jpg").scale_to_fit_height(4).move_to(ORIGIN)
        matrix_data = [["120", "45", "200"], ["200", "80", "150"], ["10", "150", "90"]]
        matrix_2d = Matrix(matrix_data, left_bracket="[", right_bracket="]").set_color(WHITE)

        def create_layer(color):
            grid = VGroup(*[Square(side_length=0.8, stroke_width=3, color=color, fill_opacity=0.3, fill_color=color) for _ in range(9)]).arrange_in_grid(rows=3, cols=3, buff=0)
            nums = VGroup(*[Text(str(np.random.randint(10, 99)), font_size=20, color=WHITE, weight=BOLD).move_to(c) for c in grid])
            return VGroup(grid, nums)

        l_b, l_g, l_r = create_layer(BLUE), create_layer(GREEN), create_layer(RED)
        for l in [l_b, l_g, l_r]:
            l.rotate(45*DEGREES, axis=OUT).rotate(60*DEGREES, axis=RIGHT).set_shear_factor(0.2)
        l_g.shift(UP*GAP*0.5 + RIGHT*GAP*0.5)
        l_r.shift(UP*GAP + RIGHT*GAP)
        volume_block = VGroup(l_b, l_g, l_r).move_to(ORIGIN)

        # --- PHẦN 2: DSTT.PNG ---
        la_img = ImageMobject("assets/dstt.png").scale_to_fit_height(4)
        la_label = Text("ĐẠI SỐ TUYẾN TÍNH", font="Segoe UI", font_size=32, weight=BOLD, color=FAMI_CYAN)
        la_group = Group(la_img, la_label).arrange(DOWN, buff=0.4).move_to(ORIGIN)

         # --- PHẦN 3: CỔNG AI ---
        def create_gate(number, text_label, icon_mobject, box_color):
            box = RoundedRectangle(width=2.2, height=3.5, corner_radius=0.2, color=box_color, fill_opacity=0.05)
            num = Text(str(number), font="Segoe UI", font_size=45, weight=BOLD, color=box_color).move_to(box).shift(UP * 1.2)
            label = Text(text_label, font="Segoe UI", font_size=20, weight=BOLD).move_to(box).shift(DOWN * 1.2)
            icon_mobject.scale_to_fit_width(1.0).move_to(box)
            return VGroup(box, num, icon_mobject, label)

        icon_color = VGroup(
            Circle(radius=0.3, color=RED, fill_opacity=0.8).shift(LEFT*0.2 + UP*0.2),
            Circle(radius=0.3, color=GREEN, fill_opacity=0.8).shift(RIGHT*0.2 + UP*0.2),
            Circle(radius=0.3, color=BLUE, fill_opacity=0.8).shift(DOWN*0.2)
        )
        icon_pos = VGroup(
            Arrow(ORIGIN, UP*0.6, buff=0, color=WHITE),
            Arrow(ORIGIN, DOWN*0.6, buff=0, color=WHITE),
            Arrow(ORIGIN, LEFT*0.6, buff=0, color=WHITE),
            Arrow(ORIGIN, RIGHT*0.6, buff=0, color=WHITE)
        )
        icon_norm = FunctionGraph(lambda x: 0.8 * np.exp(-x**2), x_range=[-2, 2], color=ACCENT)

        g1 = create_gate(1, "GIÁ TRỊ", icon_color, FAMI_CYAN)
        g2 = create_gate(2, "VỊ TRÍ", icon_pos, FAMI_CYAN)
        g3 = create_gate(3, "CHUẨN HÓA", icon_norm, FAMI_CYAN)
        gates = VGroup(g1, g2, g3).arrange(RIGHT, buff=0.5).move_to(ORIGIN).shift(DOWN * 0.8)

        ai_brain = VGroup(
            Circle(radius=0.8, color=ACCENT, stroke_width=4),
            Text("AI", font="Segoe UI", font_size=40, weight=BOLD, color=ACCENT)
        ).to_edge(RIGHT, buff=0.5).set_y(3.5) 

        # ==========================================
        # 🎬 ĐỒNG BỘ VOICEOVER & PHỤ ĐỀ CHI TIẾT
        # ==========================================

        # --- KHỐI 1: ẢNH -> MA TRẬN (~4.5s) ---
        with self.voiceover(text="Trong thị giác máy tính, bức ảnh không phải là hình ảnh, nó là Ma trận.") as tracker:
            self.update_subtitle("Trong thị giác máy tính...")
            self.play(Write(title), FadeIn(cat_img, scale=0.6), run_time=tracker.duration * 0.3)
            
            self.update_subtitle("bức ảnh không phải là hình ảnh...")
            self.play(FadeOut(cat_img, scale=1.2), FadeIn(matrix_2d, scale=0.8), run_time=tracker.duration * 0.3)
            
            self.update_subtitle("nó là Ma trận.")
            self.play(ReplacementTransform(matrix_2d, l_b), FadeIn(l_g), FadeIn(l_r), run_time=tracker.duration * 0.3, rate_func=rate_functions.ease_out_back)

        # --- KHỐI 2: ĐẠI SỐ TUYẾN TÍNH (~6.5s) ---
        with self.voiceover(text="Và để AI có thể nhìn và hiểu một bức ảnh, đại số tuyến tính là công cụ không thể thiếu để dọn dẹp dữ liệu") as tracker:
            self.update_subtitle("Và để AI có thể nhìn và hiểu một bức ảnh...")
            new_title = self.create_title("3 THAO TÁC CỐT LÕI", "DỌN DẸP DỮ LIỆU ẢNH")
            self.play(Transform(title, new_title), volume_block.animate.scale(0.3).to_edge(LEFT, buff=0.5).set_y(3.5), run_time=1.5)
            self.wait(tracker.duration * 0.2)
            
            self.update_subtitle("đại số tuyến tính là công cụ không thể thiếu...")
            self.play(FadeIn(la_group, shift=UP*0.2), run_time=2.0)
            self.wait(tracker.duration * 0.4 - 2.0) # Chờ nhịp đọc
            
            self.update_subtitle("để dọn dẹp dữ liệu...")
            # Khoảng nghỉ nhẹ cho lời thoại cuối
            self.wait(tracker.duration * 0.1)

        # Xóa DSTT trước khi sang phần Gate
        self.play(FadeOut(la_group, scale=1.2), run_time=0.6)

        # --- KHỐI 3: 3 THAO TÁC (~5.0s) ---
        with self.voiceover(text="Ở đây ta tìm hiểu 3 thao tác cốt lõi: Biến đổi giá trị, Biến đổi vị trí và Chuẩn hóa.") as tracker:
            self.update_subtitle("Ở đây ta tìm hiểu 3 thao tác cốt lõi:")
            self.wait(tracker.duration * 0.4) # Chờ nhịp đọc
            
            self.update_subtitle("Biến đổi giá trị,")
            self.play(FadeIn(g1, scale=0.8), run_time=tracker.duration * 0.2)
            
            self.update_subtitle("Biến đổi vị trí")
            self.play(FadeIn(g2, scale=0.8), run_time=tracker.duration * 0.2)
            
            self.update_subtitle("và Chuẩn hóa.")
            self.play(FadeIn(g3, scale=0.8), run_time=tracker.duration * 0.2)

        # --- KHỐI 4: KẾT THÚC (~4.5s) ---
        with self.voiceover(text="Từ đây, ta mới có nền tảng để tiến vào các mạng Nơ-ron phức tạp.") as tracker:
            self.update_subtitle("Từ đây, ta mới có nền tảng...")
            self.play(FadeIn(ai_brain, scale=0.5), run_time=tracker.duration * 0.4)
            
            self.update_subtitle("để tiến vào các mạng Nơ-ron phức tạp.")
            self.play(volume_block.animate.move_to(ai_brain).scale(0.1).set_opacity(0), run_time=tracker.duration * 0.4)
            self.play(Indicate(ai_brain[0], color=SUCCESS), run_time=tracker.duration * 0.1)

        self.finish_scene()