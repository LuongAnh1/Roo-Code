import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from skills.fami_lib import *

class Scene8_Norm_Images(FaMIBaseScene):
    def construct(self):
        # 1. TIÊU ĐỀ
        title = self.create_title("4 BIẾN THỂ CỦA NORMALIZATION", "BATCH - LAYER - INSTANCE - GROUP")
        
        # 2. KHỞI TẠO 4 ẢNH
        norm_names = ["batch", "layer", "instance", "group"]
        display_names = ["Batch Norm", "Layer Norm", "Instance Norm", "Group Norm"]
        
        # Dùng Group() thay vì VGroup()
        cards = Group()
        
        for i, name in enumerate(norm_names):
            # Ảnh là ImageMobject
            img = ImageMobject(f"assets/CV/{name}.png").scale_to_fit_width(2.0)
            # Text là VMobject (có thể dùng VGroup hoặc Group đều được, nhưng dùng Group cho đồng bộ)
            lbl = Text(display_names[i], font="Segoe UI", font_size=24, weight=BOLD, color=FAMI_CYAN)
            
            # GỘP ẢNH VÀ CHỮ: Phải dùng Group() vì ảnh là ImageMobject
            card_unit = Group(img, lbl).arrange(DOWN, buff=0.3)
            cards.add(card_unit)
        
        # Sắp xếp lưới cho Group
        cards.arrange_in_grid(rows=2, cols=2, buff=0.8).move_to(ORIGIN).shift(DOWN * 0.2)
        

        # ==========================================
        # 🎬 ĐỒNG BỘ VOICEOVER
        # ==========================================

        with self.voiceover(text="Tại đây, tùy vào cách ta gom nhóm dữ liệu để tính toán, sẽ có 4 biến thể phổ biến là: Batch Norm, Layer Norm, Instance Norm và Group Norm.") as tracker:
            self.update_subtitle("4 biến thể: Batch, Layer, Instance và Group Norm.")
            
            self.play(FadeIn(title), run_time=0.5)
            
            # Hiện lần lượt 4 ảnh với hiệu ứng pop-up nhẹ nhàng
            for i in range(len(cards)):
                self.play(FadeIn(cards[i], scale=0.8), run_time=0.4)
                # Indicate để người xem biết mình đang nói đến cái nào
                self.play(Indicate(cards[i], color=ACCENT), run_time=0.3)
            
            self.wait(tracker.get_remaining_duration())

        # ==========================================
        # 🎬 ĐOẠN 2: ĐỒ THỊ BẢN CHẤT CỦA NORMALIZATION
        # ==========================================

        with self.voiceover(text="Dù cách triển khai khác nhau, nhưng mục tiêu cuối cùng của các lớp này vẫn là duy trì sự ổn định cho toàn bộ hệ thống, giúp AI học nhanh hơn, chính xác hơn và không bao giờ bị loạn giữa biển số liệu khổng lồ!") as tracker:
            self.update_subtitle("Mục tiêu: Duy trì sự ổn định, giúp AI học nhanh và không bị 'loạn'.")
            
            # 1. Dọn dẹp 4 khối Card ở đoạn trước
            self.play(FadeOut(cards), run_time=0.5)

            # 2. XÂY DỰNG HỆ TRỤC TỌA ĐỘ (Bên phải màn hình)
            # Trục Y là Input (Dữ liệu đầu vào), Trục X là Output (Giá trị Gradient/Activation)
            axes = Axes(
                x_range=[0, 1.0, 0.2], y_range=[-6, 6, 2],
                x_length=4, y_length=6,
                axis_config={"color": GRAY, "stroke_width": 1, "include_numbers": False}
            ).to_edge(RIGHT, buff=1.0).shift(UP*0.5)

            # Hàm Sigmoid và Đạo hàm (Gradient)
            def sigmoid(x): return 1 / (1 + np.exp(-x))
            def gradient(x): return sigmoid(x) * (1 - sigmoid(x))

            # Vẽ đường cong (Dùng parametric để vẽ hàm x=f(y))
            curve_sig = axes.plot_parametric_curve(lambda t: np.array([sigmoid(t), t, 0]), t_range=[-6, 6], color=BLUE, stroke_width=3)
            curve_grad = axes.plot_parametric_curve(lambda t: np.array([gradient(t), t, 0]), t_range=[-6, 6], color=RED, stroke_width=3)
            curve_grad = DashedVMobject(curve_grad, num_dashes=30) # Đường đứt nét màu đỏ

            graph_lbl = Text("Sigmoid Activation and Gradient", font="Segoe UI", font_size=20, color=GRAY_A).next_to(axes, UP)

            self.play(
                Create(axes), Create(curve_sig), Create(curve_grad), Write(graph_lbl),
                run_time=min(1.5, tracker.duration * 0.3)
            )

            # 3. VẼ HIỆU ỨNG GOM DỮ LIỆU (FUNNEL)
            # Các điểm phân tán (Bên trái)
            input_y_vals = np.linspace(-5.5, 5.5, 15)
            # Các điểm đã chuẩn hóa (Gom lại ở giữa)
            norm_y_vals = np.linspace(-1.5, 1.5, 15)

            funnel_lines = VGroup()
            input_dots = VGroup()
            norm_dots = VGroup()

            start_x = LEFT * 4 # Vị trí cột mốc bên trái

            for y_in, y_norm in zip(input_y_vals, norm_y_vals):
                p_start = start_x + UP * (y_in * 0.5 + 0.5) # Scale Y cho vừa màn hình
                p_end = axes.c2p(0, y_norm) # Nằm ngay trên trục Y của đồ thị
                
                # Điểm ảnh
                input_dots.add(Dot(p_start, color=WHITE, radius=0.06))
                norm_dots.add(Dot(p_end, color=BLUE, radius=0.06))
                
                # Vẽ đường cong Bezier tạo hình cái phễu (Funnel) mượt mà
                line = CubicBezier(p_start, p_start + RIGHT*2, p_end + LEFT*2, p_end, color=BLUE, stroke_width=1.5, stroke_opacity=0.6)
                funnel_lines.add(line)

            input_lbl = Text("Activation Inputs", font="Segoe UI", font_size=20, color=GRAY_A).next_to(input_dots, UP, buff=0.3).shift(RIGHT * 0.7)
            norm_lbl = Text("Normalization", font="Segoe UI", font_size=20, color=WHITE).move_to(LEFT * 1 + UP * 2.5)

            # Xuất hiện dữ liệu thô
            self.play(FadeIn(input_dots), Write(input_lbl), run_time=min(0.8, tracker.duration * 0.2))
            
            # ANIMATION ĐẮT GIÁ: Gom dữ liệu
            self.play(
                Create(funnel_lines), FadeIn(norm_dots), Write(norm_lbl),
                run_time=min(1.5, tracker.duration * 0.3)
            )

            # 4. KẾT LUẬN & HIGHLIGHT
            # Khoanh tròn đỏ vùng dữ liệu được gom
            circle_highlight = Ellipse(width=0.6, height=2.0, color=RED, stroke_width=3).move_to(axes.c2p(0, 0))
            
            # Hộp Text giải thích
            box = RoundedRectangle(width=8.5, height=1.0, corner_radius=0.1, color=ACCENT, fill_color=BLACK, fill_opacity=1).move_to(DOWN * 3.5)
            explanation = Text("Normalization layer giúp tập trung dữ liệu vào khu vực có gradient lớn hơn", font="Segoe UI", font_size=18, color=ACCENT, weight=BOLD)
            explanation.scale_to_fit_width(8.0).move_to(box)
            info_box = VGroup(box, explanation)
            
            # Mũi tên chỉ từ Text box lên vòng tròn đỏ
            arrow_up = Arrow(box.get_top(), circle_highlight.get_bottom(), color=FAMI_CYAN, buff=0.1)

            self.play(
                Create(circle_highlight),
                FadeIn(info_box, shift=UP*0.2),
                GrowArrow(arrow_up),
                run_time=min(1.0, tracker.duration * 0.2)
            )
            
            self.wait(tracker.get_remaining_duration())

        self.finish_scene()
