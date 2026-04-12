import os
import sys
import subprocess
import ctypes
import math
from scipy import stats
from manim import *

PROJECT_ROOT = '/Users/doanvinhnhan/Roo-Code'

if os.getcwd() != PROJECT_ROOT:
    os.chdir(PROJECT_ROOT)

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from skills.fami_lib import *
from skills.fami_assets_helper import *
from skills.fami_effects import *
from skills.bit import BitSequence
from skills.broadcasting import Broadcasting
from skills.receiving import Receiving

config.tex_template = TexTemplate()
config.tex_template.add_to_preamble(r"\usepackage[utf8]{vietnam}")
config.tex_template.add_to_preamble(r"\usepackage{enumitem}")
config.tex_template.add_to_preamble(r"\usepackage{xcolor}")

class VideoHai(FaMIBaseScene, ThreeDScene):
    def construct(self):

        # 1. Setup + subscene 1
        with self.voiceover(text="Hãy nhìn vào dữ liệu lịch sử. Trục ngang là diện tích, trục dọc là giá nhà.") as tracker:
            self.update_subtitle("Hãy nhìn vào dữ liệu lịch sử.")
            title = self.create_title("DỰ ĐOÁN GIÁ NHÀ", "VỚI HỒI QUY TUYẾN TÍNH")
            self.add_fixed_in_frame_mobjects(title)
            
            grid = NumberPlane(
                x_range=[-8, 8, 1],
                y_range=[-4.5, 4.5, 1],
                background_line_style={
                    "stroke_color": TEAL,
                    "stroke_width": 2,
                    "stroke_opacity": 0.3
                },
                axis_config={
                    "stroke_width":0,
                    "include_tip":False,
                }
            )
            self.add(grid)

            axes = Axes(
                x_range=[0, 7, 1],
                y_range=[0, 6, 1],
                x_length=7, 
                y_length=5,  
                axis_config={"color": WHITE, "include_tip": True}
            )
            x_lab = Tex(r"Diện tích $(m^2)$", font_size=24) 
            y_lab = Tex(r"Giá nhà (Tỷ VNĐ)", font_size=24)
            labels = axes.get_axis_labels(x_label=x_lab, y_label=y_lab)
            x_values = {1: "10", 2: "20", 3: "30", 4: "40", 5: "50", 6: "60"}
            y_values = {1: "1", 2: "2", 3: "3", 4: "4", 5: "5"}
            axes.add_coordinates(x_values, y_values, font_size=24)
            
            self.play(Create(VGroup(axes, labels)), run_time=min(1.5, tracker.duration * 0.4))
            self.update_subtitle("Trục ngang là diện tích, trục dọc là giá nhà.")
            
        with self.voiceover(text="Mỗi dấu chấm ở đây là một căn nhà đã bán. Ta thấy một xu hướng: nhà càng rộng, giá càng cao.") as tracker:
            self.update_subtitle("Mỗi dấu chấm ở đây là một căn nhà đã bán.")
            text_0 = Tex(r"Bộ dữ liệu $(x_1,y_1), (x_2,y_2),\ldots,(x_n,y_n)$",font_size=30, color=BLUE).next_to(axes, UP*2.5)
            data = [(0.7375779026859406, 0.8762267637664103), (5.747548588441712, 4.470908396065174),
                    (1.155975564712503, 1.0863555316951816), (1.2659318698118998, 1.3058256123881307),
                    (4.432632627033911, 3.51281133247901), (4.154338949723417, 2.6230666476296376),
                    (5.590417955792432, 4.8), (1.9505209425364165, 1.4092493007500466),
                    (4.900527795835633, 3.6812504026237454), (2.963677054148505, 2.004136458825997),
                    (6.305782616222107, 3.377038984240996), (1.7691945699926697, 1.526166647053821),
                    (2.161768915232135, 2.02665845571968), (2.454434460755312, 2.2937663196194915),
                    (2.7788757139884477, 2.502423415838253), (5.006739293383402, 3.884868105526015),
                    (1.7858983674125484, 1.071733716382127), (0.686144734570977, 0.6021182934828442),
                    (4.499323766266825, 2.0195648824446675), (1.9232486582239645, 1.518412321111875),
                    (1.430899463271513, 1.0362479585811923), (1.8702420317026573, 1.5868088254157144),
                    (1.2110966513723391, 1.3279319837943429), (4.092423159175475, 3.191393132313477),
                    (3.8153251755350084, 2.5850336014460344), (6.324118406620103, 4.8),
                    (5.43167102428402, 2.2821358752216336), (4.037083821378183, 3.613846596804576),
                    (4.329836852240367, 2.926019130957031), (4.398204874387136, 2.2286319509480785)]
            dots = VGroup(*[Dot(point=axes.c2p(x, y), color=BLUE, radius=0.1) for x, y in data])
            self.play(FadeIn(text_0), LaggedStartMap(Create, dots, lag_ratio=0.1), run_time=tracker.duration * 0.45)
            self.update_subtitle("Ta thấy một xu hướng: nhà càng rộng, giá càng cao.")

        # Subscene 3
        slope_tracker = ValueTracker(0.2)
        intercept_tracker = ValueTracker(1.0)
        regression_line = always_redraw(lambda: 
            Line(
                axes.c2p(0, intercept_tracker.get_value()),
                axes.c2p(7, slope_tracker.get_value() * 7 + intercept_tracker.get_value()),
                color=YELLOW
            )
        )
        line_label = Tex("Đường dự đoán", font_size=20, color=YELLOW)
        line_label.add_updater(lambda m: 
            m.next_to(
                axes.c2p(7, slope_tracker.get_value() * 7 + intercept_tracker.get_value()), 
                UP, 
                buff=0.1
            )
        )

        with self.voiceover(text="Nhưng làm sao để tạo ra một công thức chung? Giải pháp là vẽ một đường thẳng đi xuyên qua đám mây dữ liệu này. Nó được gọi là Đường Hồi quy tuyến tính.") as tracker:
            self.update_subtitle("Nhưng làm sao để tạo ra một công thức chung?")
            self.play(Create(regression_line), Write(line_label), run_time=tracker.duration * 0.25)
            self.update_subtitle("Giải pháp là vẽ một đường thẳng đi xuyên qua đám mây dữ liệu này.")
            self.play(
                slope_tracker.animate.set_value(0.85),
                intercept_tracker.animate.set_value(0),
                run_time=tracker.duration * 0.3
            )
            self.update_subtitle("Nó được gọi là Đường Hồi quy tuyến tính.")
            self.play(
                slope_tracker.animate.set_value(0.4),
                intercept_tracker.animate.set_value(0.5),
                run_time=tracker.duration * 0.25
            )

        with self.voiceover(text="Để hiểu rõ hơn, chúng ta hãy cùng nhau xây dựng mô hình dự đoán từ dữ liệu này.") as tracker:
            self.update_subtitle("Để hiểu rõ hơn, chúng ta hãy cùng nhau...")
            self.play(FadeOut(text_0), run_time=tracker.duration * 0.3)
            self.update_subtitle("xây dựng mô hình dự đoán từ dữ liệu này.")
            self.play(VGroup(axes,labels, dots).animate.shift(UP*3).scale(0.5), run_time=tracker.duration * 0.4)

        # Subscene 4
        text_X = Tex(r"Gọi $X$ là diện tích $(m^2)$, $Y$ là giá nhà (Tỷ VNĐ).", substrings_to_isolate=[r"$X$", r"diện tích", r"$Y$", r"giá nhà"], font_size=30)
        text_X.set_color_by_tex(r"$X$", BLUE); text_X.set_color_by_tex(r"diện tích", BLUE)
        text_X.set_color_by_tex(r"$Y$", RED); text_X.set_color_by_tex(r"giá nhà", RED)

        text_1 = Tex(r"Ta giả định rằng giữa $X$, $Y$ có mối quan hệ tuyến tính", substrings_to_isolate=[r"$X$", r"$Y$"], font_size=30)
        text_1.set_color_by_tex(r"$X$", BLUE); text_1.set_color_by_tex(r"$Y$", RED)

        text_2 = MathTex(r"Y \approx \beta_0 + \beta_1 \times X + \epsilon", substrings_to_isolate=[r"Y", r"\beta_0", r"\beta_1", r"X"], font_size=30)
        text_2.set_color_by_tex(r"Y", RED); text_2.set_color_by_tex(r"\beta_0", GREEN)
        text_2.set_color_by_tex(r"\beta_1", YELLOW); text_2.set_color_by_tex(r"X", BLUE)

        text_3 = Tex(r"Tương ứng với", font_size=30)

        text_4 = MathTex(r"\text{Giá nhà} \approx \beta_0 + \beta_1 \times \text{Diện tích} + \epsilon", substrings_to_isolate=[r"\text{Giá nhà}", r"\beta_0", r"\beta_1", r"\text{Diện tích}"], font_size=30)
        text_4.set_color_by_tex(r"\text{Giá nhà}", RED); text_4.set_color_by_tex(r"\beta_0", GREEN)
        text_4.set_color_by_tex(r"\beta_1", YELLOW); text_4.set_color_by_tex(r"\text{Diện tích}", BLUE)

        text_5 = Tex(r"Nhiệm vụ của ta là ước lượng các tham số $\hat{\beta_0}$, $\hat{\beta_1}$ để có", substrings_to_isolate=[r"$\hat{\beta_0}$", r"$\hat{\beta_1}$"], font_size=30)
        text_5.set_color_by_tex(r"$\hat{\beta_0}$", GREEN); text_5.set_color_by_tex(r"$\hat{\beta_1}$", YELLOW)

        text_6 = Tex(r"thể dự đoán giá nhà với một giá trị cụ thể của diện tích", substrings_to_isolate=[r"giá nhà", r"diện tích"], font_size=30)
        text_6.set_color_by_tex(r"giá nhà", RED); text_6.set_color_by_tex(r"diện tích", BLUE)

        text_7 = MathTex(r"\hat{y} = \hat{\beta_0} + \hat{\beta_1} x.", substrings_to_isolate=[r"\hat{y}", r"\hat{\beta_0}", r"\hat{\beta_1}", r"x"], font_size=30)
        text_7.set_color_by_tex(r"\hat{y}", ORANGE); text_7.set_color_by_tex(r"\hat{\beta_0}", GREEN)
        text_7.set_color_by_tex(r"\hat{\beta_1}", YELLOW); text_7.set_color_by_tex(r"x", BLUE)

        paragraph = VGroup(text_X,text_1,text_2,text_3,text_4,text_5,text_6,text_7).arrange(DOWN, aligned_edge=LEFT).shift(DOWN*1)
        text_2.set_x(0); text_4.set_x(0); text_7.set_x(0)

        with self.voiceover(text="Gọi X là diện tích theo mét vuông, Y là giá nhà tính bằng Tỷ Việt Nam Đồng.") as tracker:
            self.update_subtitle("Gọi X là diện tích theo mét vuông, Y là giá nhà tính bằng Tỷ Việt Nam Đồng.")
            self.play(Write(text_X), run_time=min(1.5, tracker.duration * 0.8))

        with self.voiceover(text="Ta giả định rằng giữa X, Y có mối quan hệ tuyến tính. Giá nhà xấp xỉ beta 0 cộng beta 1 nhân với diện tích cộng với sai số epsilon.") as tracker:
            self.update_subtitle("Ta giả định rằng giữa X, Y có mối quan hệ tuyến tính.")
            self.play(Write(text_1), run_time=tracker.duration * 0.4)
            self.play(Write(text_2), run_time=tracker.duration * 0.3)
            self.play(Write(text_3), Write(text_4), run_time=tracker.duration * 0.3)

        with self.voiceover(text="Nhiệm vụ của ta là ước lượng các tham số beta 0, beta 1 để có thể dự đoán giá nhà với một diện tích cụ thể.") as tracker:
            self.update_subtitle("Nhiệm vụ của ta là ước lượng các tham số hồi quy để có thể dự đoán giá nhà với một diện tích cụ thể.")
            self.play(Write(text_5), Write(text_6), run_time=min(2, tracker.duration * 0.8))

        self.play(Write(text_7), run_time=1.5)

        self.play(FadeOut(paragraph))
        self.play(VGroup(axes,labels, dots).animate.shift(DOWN*1).scale(2))

        # Subscene 5
        text_t0 = Tex(r"Đặt $\hat{y_i} = \hat{\beta_0} + \hat{\beta_1} x_i$ ",font_size=30)
        text_t1 = Tex(r"$e = y_i-\hat{y}_i$ được gọi là phần dư",font_size=30)
        text_t2 = MathTex(r"\text{MSE} = \dfrac{1}{n}( e_1^2+e_2^2+\ldots+e_n^2)",font_size=30)
        text_t3 = MathTex(r"\hat{\beta_1} = \dfrac{\sum_{i=1}^{n}(x_i - \overline{x_i})(y_i-\overline{y})}{\sum_{i=1}^{n}(x_i-\overline{x})^2} ",font_size=30)
        text_t4 = MathTex(r"\hat{\beta_0} = \overline{y}-\hat{\beta_1}\overline{x}",font_size=30)
        formula_group_1 = VGroup(text_t0, text_t1).arrange(DOWN).shift(DOWN*2)

        y_hat_dots = VGroup(*[Dot(point=axes.c2p(x, slope_tracker.get_value() * x + intercept_tracker.get_value()), color=ORANGE, radius=0.07) for x, y in data])
        def update_y_hat_dots(mob):
            m = slope_tracker.get_value()
            b = intercept_tracker.get_value()
            for i, (x, _) in enumerate(data):
                mob[i].move_to(axes.c2p(x, m * x + b))
        y_hat_dots.add_updater(update_y_hat_dots)

        with self.voiceover(text="Mục tiêu là làm sao cho tổng khoảng cách từ các điểm thực tế đến đường thẳng dự đoán là nhỏ nhất.") as tracker:
            self.update_subtitle("Mục tiêu là làm sao cho tổng khoảng cách từ các điểm thực tế")
            self.play(Write(text_t0), run_time=tracker.duration * 0.3)
            self.update_subtitle("đến đường thẳng dự đoán này là nhỏ nhất.")
            self.play(FadeIn(y_hat_dots, lag_ratio=0.1), run_time=tracker.duration * 0.4)

        residuals = VGroup(*[Line(axes.c2p(x, y), axes.c2p(x, slope_tracker.get_value() * x + intercept_tracker.get_value()), stroke_width=3.5, color=RED, stroke_opacity=1) for x, y in data])
        def update_residuals(mob):
            m = slope_tracker.get_value()
            b = intercept_tracker.get_value()
            for i, (x, y) in enumerate(data):
                mob[i].put_start_and_end_on(axes.c2p(x, y), axes.c2p(x, m * x + b))
        residuals.add_updater(update_residuals)

        with self.voiceover(text="Khoảng chênh lệch giữa thực tế và dự đoán được gọi là một phần dư.") as tracker:
            self.update_subtitle("Khoảng chênh lệch giữa thực tế và dự đoán được gọi là một phần dư.")
            self.play(Write(text_t1), Create(residuals, lag_ratio=0.1), run_time=tracker.duration * 0.7)

        with self.voiceover(text="Có một vài cách để ước lượng các tham số, thường gặp nhất là phương pháp bình phương tối thiểu. Chính là cực tiểu hóa giá trị MSE: trung bình của bình phương phần dư.") as tracker:
            self.update_subtitle("Có một vài cách để ước lượng các tham số,")
            self.play(FadeOut(formula_group_1), run_time=tracker.duration * 0.3)
            
            formula_group_2 = VGroup(text_t2, text_t3, text_t4).arrange(DOWN).move_to(formula_group_1).shift(DOWN)
            self.update_subtitle("thường gặp nhất là phương pháp bình phương tối thiểu. Chính là cực tiểu hóa giá trị MSE")
            self.play(Write(text_t2), run_time=tracker.duration * 0.4)

        with self.voiceover(text="Bằng một vài phương pháp giải tích, ta tìm ra được chuỗi công thức để đồ thị có MSE đạt cực tiểu.") as tracker:
            self.update_subtitle("Bằng một vài phương pháp giải tích, ta tìm ra được chuỗi công thức")
            self.play(Write(VGroup(text_t3, text_t4)), run_time=tracker.duration * 0.4)
            self.update_subtitle("để đồ thị có MSE đạt cực tiểu.")

        def get_current_mse():
            m = slope_tracker.get_value()
            b = intercept_tracker.get_value()
            total_error = sum([(y - (m * x + b))**2 for x, y in data])
            return total_error / len(data)

        mse_formula = Tex(r"$\text{MSE} = \frac{1}{n} \sum (y_i - \hat{y}_i)^2 = $", font_size=30, color=WHITE).move_to(text_t2)
        mse_value = DecimalNumber(get_current_mse(), num_decimal_places=3, include_sign=False, color=RED, font_size=36).next_to(mse_formula, RIGHT)
        mse_value.add_updater(lambda d: d.set_value(get_current_mse()))
        mse_value.add_updater(lambda d: d.next_to(mse_formula, RIGHT))

        with self.voiceover(text="Chúng ta có thể quan sát giá trị MSE thay đổi khi đường thẳng dự đoán di chuyển.") as tracker:
            self.update_subtitle("Chúng ta có thể quan sát giá trị MSE thay đổi")
            self.play(Transform(text_t2, mse_formula), run_time=tracker.duration * 0.3)
            self.update_subtitle("khi đường thẳng dự đoán di chuyển.")
            self.play(FadeIn(mse_value), run_time=tracker.duration * 0.4)

        with self.voiceover(text="Và đây là vị trí tối ưu khi thay các tham số vào công thức giải tích, đường hồi quy cuối cùng giảm thiểu tối đa MSE.") as tracker:
            self.update_subtitle("Và đây là vị trí tối ưu khi thay các tham số vào công thức giải tích,")
            self.play(slope_tracker.animate.set_value(0.6059), intercept_tracker.animate.set_value(0.4019), run_time=tracker.duration * 0.4)
            self.update_subtitle("đường hồi quy cuối cùng giảm thiểu tối đa MSE.")

        value_0 = MathTex(r"= 0.6059", font_size=36).next_to(text_t3, RIGHT)
        value_1 = MathTex(r"= 0.4019", font_size=36).next_to(text_t4, RIGHT)
        self.play(FadeIn(VGroup(value_0, value_1)))

        # Remove MSE to show predictions
        with self.voiceover(text="Dựa vào kết quả này, chúng ta có thể dễ dàng ước tính giá nhà cho một diện tích mới.") as tracker:
            self.update_subtitle("Dựa vào kết quả này, chúng ta có thể dễ dàng ước tính giá nhà cho một diện tích mới.")
            self.play(FadeOut(VGroup(mse_formula, mse_value, value_0, value_1, text_t2, text_t3, text_t4)), run_time=tracker.duration * 0.7)

        d_text_0 = Tex(r"$\bullet\, \text{Diện tích} = 10 (m^2) \rightarrow \text{Giá nhà} \approx 1.0070 \text{(Tỷ VNĐ)}$", font_size=30)
        d_text_1 = Tex(r"$\bullet\, \text{Diện tích} = 20 (m^2) \rightarrow \text{Giá nhà} \approx 1.6137 \text{(Tỷ VNĐ)}$", font_size=30)
        d_text_2 = Tex(r"$\bullet\, \text{Diện tích} = 40 (m^2) \rightarrow \text{Giá nhà} \approx 2.8255 \text{(Tỷ VNĐ)}$", font_size=30)
        d_text_3 = Tex(r"$\bullet\, \text{Diện tích} = 60 (m^2) \rightarrow \text{Giá nhà} \approx 4.0373 \text{(Tỷ VNĐ)}$", font_size=30)
        predictions = VGroup(d_text_0, d_text_1, d_text_2, d_text_3).arrange(DOWN, aligned_edge=LEFT).shift(DOWN*1).move_to(mse_formula)

        with self.voiceover(text="Với 10, 20 hoặc thậm chí 60 mét vuông, các dự đoán đều được tính toán một cách hệ thống.") as tracker:
            self.update_subtitle("Với 10, 20 hoặc thậm chí 60 mét vuông,")
            self.play(LaggedStart(Write(d_text_0), Write(d_text_1), lag_ratio=0.5), run_time=tracker.duration * 0.4)
            self.update_subtitle("các dự đoán đều được tính toán một cách hệ thống.")
            self.play(LaggedStart(Write(d_text_2), Write(d_text_3), lag_ratio=0.5), run_time=tracker.duration * 0.4)

        # Subscene: Conversion to 3D and Vector Matrix forms
        with self.voiceover(text="Nhưng khoan đã, thực tế không chỉ có diện tích!") as tracker:
            self.update_subtitle("Nhưng khoan đã, thực tế không chỉ có diện tích!")
            line_label.clear_updaters()
            y_hat_dots.clear_updaters()
            residuals.clear_updaters()
            self.play(FadeOut(predictions), FadeOut(VGroup(axes, labels, y_hat_dots, residuals, regression_line, dots)), run_time=tracker.duration * 0.7)

        # Setup 3D Scene Elements
        self.add_fixed_in_frame_mobjects(self.logo, self.subtitle_obj)
        axes3d = ThreeDAxes(
            x_range=[-1, 7, 1],
            y_range=[-1, 6, 1],
            z_range=[-1, 6, 1],
            x_length=6,
            y_length=5,
            z_length=4
        )
        self.move_camera(phi=75 * DEGREES, theta=45 * DEGREES, run_time=0.1) # Set initial 3D orientation internally. Wait, self is inherited from ThreeDScene, so it works.

        with self.voiceover(text="Nếu ta thêm số phòng ngủ để đánh giá, không gian 2D lúc này sẽ trở thành 3D.") as tracker:
            self.update_subtitle("Nếu ta thêm số phòng ngủ để đánh giá,")
            self.play(Create(axes3d), run_time=min(1.5, tracker.duration * 0.4))
            self.update_subtitle("không gian 2D lúc này sẽ trở thành 3D.")
            
        with self.voiceover(text="Trong không gian 3 chiều, các điểm dữ liệu lơ lửng khắp nơi trong trục không gian.") as tracker:
            self.update_subtitle("Trong không gian 3 chiều,")
            n_dots = 20
            dots_3d = VGroup()
            for i in range(n_dots):
                x_v = np.random.uniform(1, 6)
                y_v = np.random.uniform(1, 5)
                # random point following z approx x + 0.5y
                z_v = 0.5 * x_v + 0.4 * y_v + np.random.uniform(-0.5, 0.5) 
                # Color gradient logically based on Z height
                color = interpolate_color(BLUE, RED, z_v / 5.0)
                dot3d = Sphere(center=axes3d.c2p(x_v, y_v, z_v), radius=0.1, resolution=(6, 6)).set_color(color)
                dots_3d.add(dot3d)
            self.play(LaggedStartMap(FadeIn, dots_3d, lag_ratio=0.1), run_time=tracker.duration * 0.4)
            self.update_subtitle("các điểm dữ liệu lơ lửng khắp nơi trong không gian.")

        with self.voiceover(text="Lúc này, đường thẳng hồi quy tuyến tính biến thành một 'mặt phẳng' dự đoán.") as tracker:
            self.update_subtitle("Lúc này, đường thẳng hồi quy tuyến tính biến thành")
            
            plane = Surface(
                lambda u, v: axes3d.c2p(u, v, 0.5 * u + 0.4 * v),
                u_range=[0, 7],
                v_range=[0, 6],
                checkerboard_colors=[FAMI_CYAN, FAMI_BLUE],
                fill_opacity=0.6,
                resolution=(2, 2)
            )
            plane_label = Tex("Mặt phẳng dự đoán", font_size=35, color=YELLOW).move_to(axes3d.c2p(3.5, 3, 0.5 * 3.5 + 0.4 * 3 + 1.5))
            self.add_fixed_orientation_mobjects(plane_label)
            self.add_fixed_orientation_mobjects(line_label)
            self.play(Create(plane), Transform(line_label, plane_label), run_time=tracker.duration * 0.4)
            self.update_subtitle("một 'mặt phẳng' dự đoán.")
            self.move_camera(theta=-45 * DEGREES, run_time=tracker.duration * 0.3)

        with self.voiceover(text="Đó chính là Hồi quy tuyến tính đa biến!") as tracker:
            self.update_subtitle("Đó chính là Hồi quy tuyến tính đa biến!")
            title_3d = Tex("Hồi quy tuyến tính đa biến").shift(UP*4)
            self.add_fixed_in_frame_mobjects(title_3d) # Keep text 2D on top of 3D scene
            self.play(Write(title_3d), run_time=tracker.duration * 0.7)

        with self.voiceover(text="Để tính toán cho Hồi quy đa biến, ta cần chuyển dạng phương trình đại số Y đại lượng thành dạng Phương trình Vector ma trận.") as tracker:
            self.update_subtitle("Để tính toán cho Hồi quy đa biến, ta cần chuyển dạng")
            self.move_camera(phi=60*DEGREES, theta=0*DEGREES, run_time=tracker.duration * 0.4)
            self.update_subtitle("phương trình đại số Y đại lượng thành dạng Phương trình Vector ma trận.")

        with self.voiceover(text="Công thức lúc này chuyển sang phương trình Vector ma trận.") as tracker:
            self.update_subtitle("Công thức lúc này chuyển sang phương trình Vector ma trận.")
            vector_eq = MathTex(
                r"\hat{y} = \begin{bmatrix} 1 & x_1 & x_2 & \cdots & x_p \end{bmatrix} \cdot \begin{bmatrix} \hat{\beta_0} \\ \hat{\beta_1}\\ \hat{\beta_2} \\ \vdots \\ \hat{\beta_p} \end{bmatrix} + \epsilon", 
                font_size=32, color=YELLOW
            ).shift(DOWN*2)
            self.add_fixed_in_frame_mobjects(vector_eq)
            self.play(Write(vector_eq), run_time=tracker.duration * 0.5)
            self.move_camera(theta=45*DEGREES, phi=75*DEGREES, run_time=tracker.duration * 0.4)

        with self.voiceover(text="Nhờ dạng Vector, thuật toán có thể xử lý hàng nghìn biến số thay vì chỉ 1 hay 2 biến. Thật tuyệt vời phải không toán học?") as tracker:
            self.update_subtitle("Nhờ dạng Vector, thuật toán có thể xử lý hàng nghìn biến số thay vì 1 hay 2.")
            self.play(vector_eq.animate.scale(1.2), run_time=tracker.duration * 0.4)
            self.update_subtitle("Thật tuyệt vời phải không toán học?")
            self.move_camera(theta=90*DEGREES, run_time=tracker.duration * 0.4)
            
        self.finish_scene()
