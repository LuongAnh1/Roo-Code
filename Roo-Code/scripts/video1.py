import os
import sys
from pathlib import Path
import warnings

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if os.getcwd() != str(PROJECT_ROOT):
    os.chdir(PROJECT_ROOT)

if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from manim import *
from skills.fami_lib import *
from skills.fami_assets_helper import *
from skills.fami_effects import *

config.tex_template = TexTemplate()
config.tex_template.add_to_preamble(r"\usepackage[utf8]{vietnam}")
config.media_dir = str(PROJECT_ROOT / "media")
config.pixel_width = 720
config.pixel_height = 1280
config.frame_rate = 15
config.disable_caching = True
config.verbosity = "ERROR"

warnings.filterwarnings('ignore')

class mainScene(FaMIBaseScene):
    def construct(self):
        title = self.create_title("ƯỚC LƯỢNG ĐỘ BỀN LINH KIỆN PISTON TRONG ĐỘNG CƠ Ô TÔ")
        self.play(Write(title))

        text_title = Tex(r"Phân phối chuẩn có phù hợp để dùng trong việc \\ước lượng độ bền linh kiện piston không?", font_size=40)
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 0.5, 0.1],
            x_length=8,
            y_length=4,
            axis_config={"include_tip": False}
        )
        self.play(Create(axes))

        def gaussian(x, mu=0, sigma=1):
            return (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)

        graph = axes.plot(lambda x: gaussian(x), color=BLUE).set_fill(opacity=0)
        negative_area = axes.get_area(
            graph, x_range=[-4, 0], color=RED, opacity=0.8
        ).set_stroke(RED, width=2)

        with self.voiceover(text="Làm sao để dự đoán giá một căn nhà khi bạn chỉ biết diện tích của nó?") as tracker:
            self.update_subtitle("Làm sao để dự đoán giá một căn nhà khi bạn chỉ biết diện tích của nó?")
            self.play(Create(graph), run_time=tracker.duration * 0.3)
            self.play(Write(text_title.next_to(axes, UP)), run_time=tracker.duration * 0.3)
            self.play(DrawBorderThenFill(negative_area), run_time=tracker.duration * 0.3)

        math_logic = MathTex(
            "x < 0", "\\Rightarrow", "\\text{Tuổi thọ} < 0", "\\text{ (Vô lý!)}",
            font_size=36
        ).set_color(YELLOW)
        math_logic.next_to(negative_area, DOWN, buff=0.5)

        with self.voiceover(text="Việc một linh kiện có tuổi thọ âm là vô lý, nên phân phối chuẩn không phải là lựa chọn cuối cùng.") as tracker:
            self.update_subtitle("Phân phối chuẩn không phù hợp với tuổi thọ piston")
            self.play(Write(math_logic[0]), run_time=tracker.duration * 0.2)
            self.play(Write(math_logic[1]), Write(math_logic[2]), run_time=tracker.duration * 0.3)
            self.play(Indicate(math_logic[3], color=RED), run_time=tracker.duration * 0.3)
            everything_wrong = VGroup(graph, negative_area, math_logic, axes, text_title)
            cross = Cross(everything_wrong, stroke_width=15).set_color(WHITE)
            self.play(Create(cross), run_time=tracker.duration * 0.2)
            self.play(FadeOut(everything_wrong), FadeOut(cross), run_time=tracker.duration * 0.4)

        head = Circle(radius=0.55).set_stroke(WHITE, 5)
        body = Line(head.get_bottom(), head.get_bottom() + 2.2 * DOWN).set_stroke(WHITE, 5)
        left_arm = Line(body.get_top(), body.get_top() + 1.4 * (DOWN + 0.3 * LEFT)).set_stroke(WHITE, 5)
        right_arm = Line(body.get_top(), body.get_top() + 1.4 * (DOWN + 0.3 * RIGHT)).set_stroke(WHITE, 5)
        left_leg = Line(body.get_bottom(), body.get_bottom() + 1.4 * (DL * 0.7)).set_stroke(WHITE, 5)
        right_leg = Line(body.get_bottom(), body.get_bottom() + 1.4 * (DR * 0.7)).set_stroke(WHITE, 5)

        student = VGroup(head, body, left_arm, right_arm, left_leg, right_leg)
        student.center().shift(DOWN * 0.8)

        q_group = VGroup(
            Tex("?", font_size=80, color=RED).shift(LEFT * 1.0),
            Tex("?", font_size=100, color=RED),
            Tex("?", font_size=80, color=RED).shift(RIGHT * 1.0)
        ).next_to(head, UP, buff=0.6)

        bulb_glass = Circle(radius=0.45, color=YELLOW, fill_opacity=0).set_stroke(YELLOW, 4)
        bulb_base = Rectangle(height=0.25, width=0.35).next_to(bulb_glass, DOWN, buff=0.05).set_stroke(GRAY, 3)
        lightbulb = VGroup(bulb_glass, bulb_base).move_to(q_group[1].get_center())

        self.play(FadeIn(student, shift=UP), run_time=1.0)
        with self.voiceover(text="Người thông minh như bạn đã tìm ra cách khắc phục nhược điểm đó bằng một ý tưởng mới.") as tracker:
            self.update_subtitle("Người thông minh như bạn đã tìm ra cách khắc phục")
            self.play(LaggedStart(*[Write(q) for q in q_group], lag_ratio=0.3), run_time=tracker.duration * 0.8)

        spark_center = bulb_glass.get_top() + UP * 0.2
        glow_lines = VGroup(*[
            Line(spark_center + 0.1 * d, spark_center + 0.5 * d).set_stroke(YELLOW, 4)
            for d in [UP, UL, UR, LEFT, RIGHT]
        ])

        with self.voiceover(text="Và rồi, một giải pháp đã nảy ra...") as tracker:
            self.update_subtitle("Và rồi, một giải pháp đã nảy ra...")
            self.play(
                FadeOut(q_group, scale=0.5),
                FadeIn(bulb_base),
                bulb_glass.animate.set_fill(YELLOW, opacity=0.8),
                run_time=tracker.duration * 0.5
            )
            self.play(Create(glow_lines), Indicate(bulb_glass, scale_factor=1.2), run_time=tracker.duration * 0.3)

        to_remove = Group(*[mob for mob in self.mobjects if mob != title])
        self.play(FadeOut(to_remove), run_time=0.8)

        log_normal_big_tex = Tex("Phân phối Log-Chuẩn", color=GREEN, font_size=72).move_to(ORIGIN)
        with self.voiceover(text="Đó chính là: Phân phối Log-Chuẩn!") as tracker:
            self.update_subtitle("Đó chính là: Phân phối Log-Chuẩn")
            self.play(
                Write(log_normal_big_tex),
                log_normal_big_tex.animate.scale(1.2),
                run_time=tracker.duration * 0.8
            )

        chot_ha_title = Tex(r"Tại sao chọn Log-Chuẩn?", color=WHITE, font_size=40)
        chot_ha_title.next_to(title, DOWN, buff=0.3)

        with self.voiceover(text="Vậy tại sao lại là phân phối log-chuẩn? Hãy xem 3 lý do then chốt.") as tracker:
            self.update_subtitle("Vậy tại sao chọn Log-Chuẩn?")
            self.play(Transform(log_normal_big_tex, chot_ha_title), run_time=tracker.duration * 0.5)

        axes_final = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 5, 1],
            x_length=8,
            y_length=3.5,
            axis_config={"include_tip": True, "tip_shape": StealthTip},
        ).shift(DOWN * 1.0)

        x_lab = axes_final.get_x_axis_label(Tex("Tuổi thọ", font_size=30))
        y_lab = axes_final.get_y_axis_label(Tex(r"\% Hỏng", font_size=30))

        with self.voiceover(text="Ta cần nhìn vào 3 lý do: bản chất, logic và thực tế.") as tracker:
            self.update_subtitle("3 lý do chọn phân phối log-chuẩn")
            self.play(Create(axes_final), Write(VGroup(x_lab, y_lab)), run_time=tracker.duration * 0.5)

        tex_pos = UP * 1.2

        with self.voiceover(text="Một là bản chất: vết nứt mỏi tích lũy theo cấp số nhân.") as tracker:
            self.update_subtitle("1. Bản chất: Vết nứt mỏi tích lũy cấp số nhân")
            tex_reason_1 = Tex(r"1. Vết nứt tích lũy theo cấp số nhân", color=YELLOW_E, font_size=34).move_to(tex_pos)

            def exp_func(x):
                return 0.1 * np.exp(0.45 * x)

            curve_exp = axes_final.plot(exp_func, x_range=[0.1, 8.5], color=YELLOW_E)
            self.play(Write(tex_reason_1), Create(curve_exp), run_time=tracker.duration * 0.5)
            self.play(FadeOut(curve_exp), FadeOut(tex_reason_1), run_time=tracker.duration * 0.3)

        with self.voiceover(text="Hai là logic: tuổi thọ luôn dương, không bao giờ âm.") as tracker:
            self.update_subtitle("2. Logic: Tuổi thọ luôn dương (t > 0)")
            tex_reason_2 = Tex(r"2. Tuổi thọ luôn dương ($t > 0$)", color=RED_E, font_size=34).move_to(tex_pos)

            def normal_func(x):
                return 4 * np.exp(-((x - 4)**2) / (2 * 1.2**2))

            curve_normal_final = axes_final.plot(normal_func, x_range=[0, 10], color=RED_D)
            self.play(Write(tex_reason_2), Create(curve_normal_final), run_time=tracker.duration * 0.6)

        with self.voiceover(text="Ba là thực tế: đồ thị lệch phải phản ánh đúng dữ liệu piston thật.") as tracker:
            self.update_subtitle("3. Thực tế: Đồ thị lệch phải khớp dữ liệu thật")
            tex_reason_3 = Tex(r"3. Khớp hoàn hảo dữ liệu Piston", color=ORANGE, font_size=34).move_to(tex_pos)

            def lognorm_final(x):
                if x <= 0: return 0
                return (3.8 / (x * 0.7)) * np.exp(-((np.log(x/1.8))**2) / (2 * 0.7**2))

            curve_lognorm_final = axes_final.plot(lognorm_final, x_range=[0.1, 10], color=GREEN_D)
            tail_fill_final = axes_final.get_area(curve_lognorm_final, x_range=[4.5, 9.5], color=YELLOW, opacity=0.6)
            piston_ben_text = Tex("Piston siêu bền", color=YELLOW, font_size=28).move_to(axes_final.c2p(7.5, 1.2))

            self.play(
                Transform(tex_reason_2, tex_reason_3),
                Transform(curve_normal_final, curve_lognorm_final),
                run_time=tracker.duration * 0.6
            )
            self.play(FadeIn(tail_fill_final), Write(piston_ben_text), run_time=tracker.duration * 0.3)

        keep_only = [title]
        to_remove = []
        for mob in self.mobjects:
            if mob in keep_only:
                continue
            if "ImageMobject" in str(type(mob)):
                continue
            to_remove.append(mob)

        with self.voiceover(text="Giờ chúng ta dọn cảnh để chuyển sang phần công thức log-chuẩn.") as tracker:
            self.update_subtitle("Chuẩn bị chuyển sang công thức log-chuẩn")
            self.play(*[FadeOut(mob) for mob in to_remove], run_time=tracker.duration * 0.8)

        def get_soft_box(mobject, color=YELLOW):
            return SurroundingRectangle(
                mobject,
                color=color,
                buff=0.3,
                corner_radius=0.2
            )

        intro_label = Text(
            "Định nghĩa biến ngẫu nhiên Log-Chuẩn",
            font_size=24, color=BLUE_B, font="Noto Sans"
        ).shift(UP * 1.2)
        def_math = MathTex(r"X = e^{\mu + \sigma Y}", font_size=48)
        def_box = get_soft_box(def_math, YELLOW)

        definition_group = VGroup(intro_label, def_math, def_box).move_to(ORIGIN)
        with self.voiceover(text="Đồng thời, ta có Y là biến chuẩn tắc; X = e^{mu + sigma Y} là phân phối log-chuẩn.") as tracker:
            self.update_subtitle("Định nghĩa: X = e^{mu + sigma Y}")
            self.play(Write(intro_label), FadeIn(def_math, scale=1.2), Create(def_box), run_time=tracker.duration * 0.7)

        with self.voiceover(text="Khi lấy log, dữ liệu X dương chuyển thành Y chuẩn, và điều này giúp ta dùng phân phối chuẩn cho tính toán.") as tracker:
            self.update_subtitle("Khi lấy log, dữ liệu tuân theo phân phối chuẩn")
            self.play(FadeOut(definition_group, shift=UP), run_time=tracker.duration * 0.6)

        label_1 = Text(
            "1. Kỳ vọng và Phương sai của ln(X)",
            font_size=20, color=GREEN_A, font="Noto Sans"
        )
        math_1 = MathTex(
            r"\mu = \ln \frac{\mu_X^2}{\sqrt{\mu^2_X + \sigma^2_X}} \quad ; \quad \sigma^2 = \ln \left( 1 + \frac{\sigma^2_X}{\mu^2_X} \right)",
            font_size=32
        )
        box_1 = get_soft_box(math_1, WHITE)
        item_1 = VGroup(label_1, math_1, box_1)
        label_1.next_to(box_1, UP, buff=0.2)
        item_1.move_to(ORIGIN)

        label_2 = Text(
            "2. Hàm mật độ xác suất (PDF)",
            font_size=20, color=GREEN_A, font="Noto Sans"
        )
        math_2 = MathTex(
            r"f_X(x) = \frac{1}{x\sigma\sqrt{2\pi}} \exp \left( -\frac{(\ln x - \mu)^2}{2\sigma^2} \right)",
            font_size=32
        )
        box_2 = get_soft_box(math_2, GREEN_D)
        item_2 = VGroup(label_2, math_2, box_2)
        label_2.next_to(box_2, UP, buff=0.2)
        item_2.move_to(ORIGIN + DOWN * 0.2)

        label_3 = Text(
            "3. Hàm phân phối tích lũy (CDF)",
            font_size=20, color=GREEN_A, font="Noto Sans"
        )
        math_3 = MathTex(
            r"P(X \le x) = \Phi \left( \frac{\ln x - \mu}{\sigma} \right)",
            font_size=32
        )
        box_3 = get_soft_box(math_3, BLUE_D)
        item_3 = VGroup(label_3, math_3, box_3)
        label_3.next_to(box_3, UP, buff=0.2)
        item_3.move_to(ORIGIN + DOWN * 1.2)

        with self.voiceover(text="Những ký tự mu, sigma và hàm Phi không chỉ nằm trên giấy mà còn là ngôn ngữ của kỹ sư độ bền.") as tracker:
            self.update_subtitle("Công thức log-chuẩn: mu, sigma, PDF, CDF")
            self.play(FadeIn(item_1, shift=DOWN), run_time=tracker.duration * 0.2)
            self.play(item_1.animate.shift(UP * 2.2).scale(0.85), FadeIn(item_2, shift=DOWN), run_time=tracker.duration * 0.25)
            self.play(item_1.animate.shift(UP * 1.8), item_2.animate.shift(UP * 1.6).scale(0.85), FadeIn(item_3, shift=DOWN), run_time=tracker.duration * 0.3)
            self.play(FadeOut(item_1), FadeOut(item_2), FadeOut(item_3), run_time=tracker.duration * 0.2)

        label_est_1 = Text(
            "Ước lượng Kỳ vọng  —  Phân phối Student",
            font_size=24, color=ORANGE, font="Noto Sans"
        )
        math_est_1 = MathTex(
            r"\left( \bar{y} - t_{\alpha/2,\, n-1} \frac{s_y}{\sqrt{n}} \ ;\ \bar{y} + t_{\alpha/2,\, n-1} \frac{s_y}{\sqrt{n}} \right)",
            font_size=38
        )
        box_est_1 = get_soft_box(math_est_1, WHITE)
        item_est_1 = VGroup(label_est_1, math_est_1, box_est_1).move_to(ORIGIN)
        label_est_1.next_to(box_est_1, UP, buff=0.3)

        label_est_2 = Text(
            "Ước lượng Phương sai  —  Chi-bình phương",
            font_size=24, color=ORANGE, font="Noto Sans"
        )
        math_est_2 = MathTex(
            r"\left( \frac{(n-1)s_y^2}{\chi^2_{\alpha/2,\, n-1}} \ ;\ \frac{(n-1)s_y^2}{\chi^2_{1-\alpha/2,\, n-1}} \right)",
            font_size=38
        )
        box_est_2 = get_soft_box(math_est_2, ORANGE)
        item_est_2 = VGroup(label_est_2, math_est_2, box_est_2).next_to(item_est_1, DOWN, buff=1.0)
        label_est_2.next_to(box_est_2, UP, buff=0.3)

        with self.voiceover(text="Để làm được điều đó, kỹ sư lấy y_i = ln x_i rồi áp dụng Student và Chi-square.") as tracker:
            self.update_subtitle("Để làm được điều đó, lấy logarit dữ liệu")
            self.play(Write(label_est_1), Create(box_est_1), Write(math_est_1), run_time=tracker.duration * 0.35)
            self.play(item_est_1.animate.shift(UP * 1.8).scale(0.9), run_time=tracker.duration * 0.2)
            self.play(Write(label_est_2), Create(box_est_2), Write(math_est_2), run_time=tracker.duration * 0.35)

        title = self.create_title("ƯỚC LƯỢNG ĐỘ BỀN LINH KIỆN PISTON TRONG ĐỘNG CƠ Ô TÔ")
        with self.voiceover(text="Cuối cùng, nhà máy chọn cận dưới của khoảng ước lượng làm mốc bảo dưỡng an toàn nhất.") as tracker:
            self.update_subtitle("Chọn cận dưới để an toàn nhất")
            self.play(FadeOut(*self.mobjects), run_time=tracker.duration * 0.5)
            self.play(Write(title), run_time=tracker.duration * 0.3)

        graph_center = ORIGIN + DOWN * 1.0
        outro_axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 1.4, 0.4],
            x_length=7.5,
            y_length=3.0,
            axis_config={"include_tip": True}
        ).move_to(graph_center)

        y_unit = Text("% Hỏng", font_size=16, font="Arial").next_to(outro_axes.y_axis.get_top(), LEFT, buff=0.1)
        x_unit = Text("Tuổi thọ (giờ)", font_size=16, font="Arial").next_to(outro_axes.x_axis.get_end(), DOWN, buff=0.1)
        axis_labels = VGroup(y_unit, x_unit)

        def final_lognorm(x):
            if x <= 0: return 0
            return (1.6 / (x * 0.6)) * np.exp(-((np.log(x / 2.5))**2) / (2 * 0.6**2))

        curve = outro_axes.plot(final_lognorm, x_range=[0.1, 9], color=WHITE)

        t_peak = 1.6
        t_mean = 3.5
        line_safe = outro_axes.get_vertical_line(outro_axes.c2p(t_peak, final_lognorm(t_peak)), color=GREEN)
        label_safe = Text("Mốc an toàn (Cận dưới)", font_size=14, color=GREEN, font="Arial")\
            .next_to(outro_axes.c2p(t_peak, final_lognorm(t_peak)), UP, buff=0.2)
        line_mean = outro_axes.get_vertical_line(outro_axes.c2p(t_mean, final_lognorm(t_mean)), color=RED)
        label_mean = Text("Giá trị trung bình", font_size=14, color=RED, font="Arial")\
            .next_to(outro_axes.c2p(t_mean, final_lognorm(t_mean)), UP + RIGHT, buff=0.2)

        with self.voiceover(text="Các kỹ sư chọn mốc an toàn và mốc trung bình để so sánh rủi ro và độ bền.") as tracker:
            self.update_subtitle("Mốc an toàn và mốc trung bình")
            self.play(Create(outro_axes), Write(axis_labels), run_time=tracker.duration * 0.35)
            self.play(Create(curve), run_time=tracker.duration * 0.35)
            self.play(Create(line_safe), Write(label_safe), run_time=tracker.duration * 0.15)
            self.play(Create(line_mean), Write(label_mean), run_time=tracker.duration * 0.1)

        risk_area = outro_axes.get_area(curve, x_range=[t_peak, 9], color=RED_E, opacity=0.3)
        safe_text = Text("NGĂN CHẶN HỎNG HÓC SỚM", font_size=30, color=YELLOW, font="Arial").move_to(UP * 2.4)
        safe_box = SurroundingRectangle(safe_text, color=YELLOW, buff=0.2, corner_radius=0.1)

        with self.voiceover(text="Đây là mốc thời gian bảo trì quan trọng, giúp hệ thống vận hành trơn tru nhất.") as tracker:
            self.update_subtitle("NGĂN CHẶN HỎNG HÓC SỚM")
            self.play(FadeIn(risk_area), run_time=tracker.duration * 0.5)
            self.play(Write(safe_text), Create(safe_box), run_time=tracker.duration * 0.3)
            self.play(Indicate(safe_text, color=YELLOW), run_time=tracker.duration * 0.1)

if __name__ == "__main__":
    scene = mainScene()
    scene.render()
