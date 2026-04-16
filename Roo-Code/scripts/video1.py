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

# ─────────────────────────────────────────────────────────────
# HELPER: Framed bilingual subtitle at fixed position (0, -3.8)
# EN: Arial 20 white  |  VI: Arial 16 yellow
# Khung bo góc, nền tối bán trong suốt
# ─────────────────────────────────────────────────────────────
SUB_CENTER = DOWN * 3.8

def make_subtitle(en_text: str, vi_text: str):
    en = Text(en_text, font="Arial", font_size=20, color=WHITE)
    vi = Text(vi_text, font="Arial", font_size=16, color=YELLOW)
    vi.next_to(en, DOWN, buff=0.10)
    content = VGroup(en, vi)
    content.move_to(SUB_CENTER)

    box = SurroundingRectangle(
        content,
        color=WHITE,
        fill_color=BLACK,
        fill_opacity=0.55,
        buff=0.18,
        corner_radius=0.12,
        stroke_width=1.2,
    )
    box.set_z_index(9)
    content.set_z_index(10)
    return VGroup(box, content)


class mainScene(FaMIBaseScene):

    def show_subtitle(self, en_text: str, vi_text: str):
        """Replace current subtitle instantly (no animation — runs between play() calls)."""
        if hasattr(self, "_cur_sub") and self._cur_sub in self.mobjects:
            self.remove(self._cur_sub)
        sub = make_subtitle(en_text, vi_text)
        self.add(sub)
        self._cur_sub = sub

    def clear_subtitle(self):
        if hasattr(self, "_cur_sub") and self._cur_sub in self.mobjects:
            self.remove(self._cur_sub)

    # ── soft rounded box for formula cards ──────────────────
    @staticmethod
    def soft_box(mob, color=YELLOW):
        return SurroundingRectangle(mob, color=color, buff=0.3, corner_radius=0.2)

    def construct(self):

        # ══════════════════════════════════════════════════════
        # SCENE 1 — Normal distribution is the wrong tool
        # ══════════════════════════════════════════════════════
        title = self.create_title(
            "ƯỚC LƯỢNG ĐỘ BỀN LINH KIỆN PISTON TRONG ĐỘNG CƠ Ô TÔ"
        )

        text_title = Tex(
            r"Phân phối chuẩn có phù hợp để ước lượng \\độ bền linh kiện piston không?",
            font_size=38,
        )
        axes = Axes(
            x_range=[-4, 4, 1], y_range=[0, 0.5, 0.1],
            x_length=8, y_length=3.8,
            axis_config={"include_tip": False},
        )

        def gaussian(x, mu=0, sigma=1):
            return (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(
                -0.5 * ((x - mu) / sigma) ** 2
            )

        graph = axes.plot(lambda x: gaussian(x), color=BLUE).set_fill(opacity=0)
        negative_area = axes.get_area(
            graph, x_range=[-4, 0], color=RED, opacity=0.8
        ).set_stroke(RED, width=2)

        # ── VO 1 ── (~7s)
        with self.voiceover(
            text="Phân phối chuẩn có thực sự phù hợp để ước lượng độ bền linh kiện piston không?"
        ) as tracker:
            self.show_subtitle(
                "Normal dist. right for piston durability?",
                "Phân phối chuẩn có phù hợp bài toán này?",
            )
            self.play(Write(title), run_time=min(1.2, tracker.duration * 0.35))
            self.play(
                Create(axes),
                Write(text_title.next_to(axes, UP)),
                run_time=min(1.5, tracker.duration * 0.45),
            )
            self.play(Create(graph), run_time=min(0.8, tracker.duration * 0.2))

        # ── VO 2 ── (~7s)
        with self.voiceover(
            text="Vấn đề nghiêm trọng: phân phối chuẩn nhận giá trị âm — vô lý với tuổi thọ!"
        ) as tracker:
            self.show_subtitle(
                "Normal accepts negatives — impossible!",
                "Phân phối chuẩn nhận giá trị âm — vô lý!",
            )
            self.play(DrawBorderThenFill(negative_area), run_time=min(1.0, tracker.duration * 0.3))
            math_logic = MathTex(
                "x < 0", "\\Rightarrow", "\\text{Tuổi thọ} < 0", "\\text{ (Vô lý!)}",
                font_size=34,
            ).set_color(YELLOW).next_to(negative_area, DOWN, buff=0.4)
            self.play(
                Write(math_logic[0]),
                Write(math_logic[1]),
                Write(math_logic[2]),
                run_time=min(1.0, tracker.duration * 0.3),
            )
            self.play(Indicate(math_logic[3], color=RED), run_time=min(0.6, tracker.duration * 0.15))
            everything_wrong = VGroup(graph, negative_area, math_logic, axes, text_title)
            cross = Cross(everything_wrong, stroke_width=14).set_color(WHITE)
            self.play(Create(cross), run_time=min(0.8, tracker.duration * 0.2))
            self.play(
                FadeOut(everything_wrong), FadeOut(cross),
                run_time=min(0.6, tracker.duration * 0.15),
            )

        # ══════════════════════════════════════════════════════
        # SCENE 2 — Lightbulb moment: Log-Normal
        # ══════════════════════════════════════════════════════
        head      = Circle(radius=0.55).set_stroke(WHITE, 5)
        body      = Line(head.get_bottom(), head.get_bottom() + 2.2 * DOWN).set_stroke(WHITE, 5)
        left_arm  = Line(body.get_top(), body.get_top() + 1.4 * (DOWN + 0.3 * LEFT)).set_stroke(WHITE, 5)
        right_arm = Line(body.get_top(), body.get_top() + 1.4 * (DOWN + 0.3 * RIGHT)).set_stroke(WHITE, 5)
        left_leg  = Line(body.get_bottom(), body.get_bottom() + 1.4 * (DL * 0.7)).set_stroke(WHITE, 5)
        right_leg = Line(body.get_bottom(), body.get_bottom() + 1.4 * (DR * 0.7)).set_stroke(WHITE, 5)
        student   = VGroup(head, body, left_arm, right_arm, left_leg, right_leg).center().shift(DOWN * 0.8)

        q_group = VGroup(
            Tex("?", font_size=80,  color=RED).shift(LEFT * 1.0),
            Tex("?", font_size=100, color=RED),
            Tex("?", font_size=80,  color=RED).shift(RIGHT * 1.0),
        ).next_to(head, UP, buff=0.6)

        bulb_glass = Circle(radius=0.45, color=YELLOW, fill_opacity=0).set_stroke(YELLOW, 4)
        bulb_base  = Rectangle(height=0.25, width=0.35).next_to(bulb_glass, DOWN, buff=0.05).set_stroke(GRAY, 3)
        lightbulb  = VGroup(bulb_glass, bulb_base)
        lightbulb.move_to(q_group[1].get_center())  # move trước

        # Tính spark_center SAU khi đã move
        spark_center = bulb_glass.get_top() + UP * 0.2
        glow_lines = VGroup(*[
            Line(spark_center + 0.1 * d, spark_center + 0.5 * d).set_stroke(YELLOW, 4)
            for d in [UP, UL, UR, LEFT, RIGHT]
        ])
        # ── VO 3 ── (~5s)
        with self.voiceover(
            text="Người kỹ sư thông minh tìm ra giải pháp: phân phối Log-Chuẩn!"
        ) as tracker:
            self.show_subtitle(
                "Solution: Log-Normal distribution!",
                "Giải pháp: Phân phối Log-Chuẩn!",
            )
            self.play(FadeIn(student, shift=UP), run_time=min(0.7, tracker.duration * 0.25))
            self.play(
                LaggedStart(*[Write(q) for q in q_group], lag_ratio=0.25),
                run_time=min(0.8, tracker.duration * 0.3),
            )
            self.play(
                FadeOut(q_group, scale=0.5),
                FadeIn(bulb_base),
                bulb_glass.animate.set_fill(YELLOW, opacity=0.8),
                run_time=min(0.6, tracker.duration * 0.2),
            )
            self.play(
                Create(glow_lines),
                Indicate(bulb_glass, scale_factor=1.2),
                run_time=min(0.6, tracker.duration * 0.2),
            )

        to_remove = Group(*[m for m in self.mobjects if m != title])
        self.play(FadeOut(to_remove), run_time=0.5)

        log_tex = Tex("Phân phối Log-Chuẩn", color=GREEN, font_size=68).move_to(ORIGIN)

        # ── VO 4 ── (~6s)
        with self.voiceover(
            text="Ba lý do khiến Log-Chuẩn là lựa chọn tối ưu cho bài toán này."
        ) as tracker:
            self.show_subtitle(
                "3 reasons Log-Normal is optimal here.",
                "3 lý do Log-Chuẩn là lựa chọn tối ưu.",
            )
            self.play(Write(log_tex), run_time=min(1.0, tracker.duration * 0.4))
            chot_ha = Tex(r"Tại sao chọn Log-Chuẩn?", color=WHITE, font_size=40)
            chot_ha.next_to(title, DOWN, buff=0.3)
            self.play(Transform(log_tex, chot_ha), run_time=min(1.0, tracker.duration * 0.4))

        # ══════════════════════════════════════════════════════
        # SCENE 3 — 3 reasons
        # ══════════════════════════════════════════════════════
        axes3 = Axes(
            x_range=[0, 10, 2], y_range=[0, 5, 1],
            x_length=8, y_length=3.5,
            axis_config={"include_tip": True, "tip_shape": StealthTip},
        ).shift(DOWN * 1.0)
        x_lab3 = axes3.get_x_axis_label(Tex("Tuổi thọ", font_size=28))
        y_lab3 = axes3.get_y_axis_label(Tex(r"\% Hỏng", font_size=28))
        self.play(Create(axes3), Write(VGroup(x_lab3, y_lab3)), run_time=0.8)

        tex_pos = UP * 1.2

        # ── VO 5 — Reason 1 ── (~6s)
        with self.voiceover(
            text="Một — bản chất: vết nứt mỏi tích lũy theo cấp số nhân."
        ) as tracker:
            self.show_subtitle(
                "Reason 1: fatigue cracks grow exponentially.",
                "Lý do 1: vết nứt tích lũy cấp số nhân.",
            )
            r1 = Tex(r"1. Vết nứt tích lũy theo cấp số nhân", color=YELLOW_E, font_size=32).move_to(tex_pos)
            c1 = axes3.plot(lambda x: 0.1 * np.exp(0.45 * x), x_range=[0.1, 8.5], color=YELLOW_E)
            self.play(Write(r1), Create(c1), run_time=tracker.duration * 0.85)
            self.play(FadeOut(r1), FadeOut(c1), run_time=0.4)

        # ── VO 6 — Reason 2 ── (~6s)
        with self.voiceover(
            text="Hai — logic: tuổi thọ luôn dương, Log-Chuẩn không sinh giá trị âm."
        ) as tracker:
            self.show_subtitle(
                "Reason 2: lifespan always positive (t > 0).",
                "Lý do 2: tuổi thọ luôn dương (t > 0).",
            )
            r2 = Tex(r"2. Tuổi thọ luôn dương ($t > 0$)", color=RED_E, font_size=32).move_to(tex_pos)
            c2 = axes3.plot(
                lambda x: 4 * np.exp(-((x - 4) ** 2) / (2 * 1.2 ** 2)),
                x_range=[0, 10], color=RED_D,
            )
            self.play(Write(r2), Create(c2), run_time=tracker.duration * 0.85)

        # ── VO 7 — Reason 3 ── (~7s)
        with self.voiceover(
            text="Ba — thực tế: đồ thị lệch phải khớp hoàn hảo với dữ liệu piston thật."
        ) as tracker:
            self.show_subtitle(
                "Reason 3: right tail fits real piston data.",
                "Lý do 3: đuôi phải khớp dữ liệu piston.",
            )
            r3 = Tex(r"3. Khớp hoàn hảo dữ liệu Piston", color=ORANGE, font_size=32).move_to(tex_pos)

            def lognorm3(x):
                if x <= 0: return 0
                return (3.8 / (x * 0.7)) * np.exp(-((np.log(x / 1.8)) ** 2) / (2 * 0.7 ** 2))

            c3 = axes3.plot(lognorm3, x_range=[0.1, 10], color=GREEN_D)
            tail = axes3.get_area(c3, x_range=[4.5, 9.5], color=YELLOW, opacity=0.6)
            pin = Tex("Piston siêu bền", color=YELLOW, font_size=26).move_to(axes3.c2p(7.5, 1.1))

            self.play(Transform(r2, r3), Transform(c2, c3), run_time=min(1.4, tracker.duration * 0.4))
            self.play(FadeIn(tail), Write(pin), run_time=min(1.0, tracker.duration * 0.3))
            self.wait(min(1.0, tracker.duration * 0.2))

        # ══════════════════════════════════════════════════════
        # SCENE 4 — Definition: X = e^(μ+σY)
        # ══════════════════════════════════════════════════════
        keep = [title]
        to_rm = [m for m in self.mobjects if m not in keep and "ImageMobject" not in str(type(m))]
        self.play(*[FadeOut(m) for m in to_rm], run_time=0.7)

        intro_lbl = Text("Định nghĩa biến ngẫu nhiên Log-Chuẩn", font_size=22, color=BLUE_B, font="Arial").shift(UP * 1.2)
        def_math  = MathTex(r"X = e^{\mu + \sigma Y}", font_size=50)
        def_box   = self.soft_box(def_math, YELLOW)
        def_grp   = VGroup(intro_lbl, def_math, def_box).move_to(ORIGIN)

        # ── VO 8 ── (~7s)
        with self.voiceover(
            text="Định nghĩa: X bằng e mũ mu cộng sigma Y, với Y là biến chuẩn tắc."
        ) as tracker:
            self.show_subtitle(
                "Definition: X = e^(μ+σY), Y ~ N(0,1).",
                "Định nghĩa: X = e^(μ+σY), Y chuẩn tắc.",
            )
            self.play(Write(intro_lbl), run_time=min(0.8, tracker.duration * 0.25))
            self.play(FadeIn(def_math, scale=1.2), Create(def_box), run_time=min(1.2, tracker.duration * 0.4))

        # ── VO 9 ── (~7s)
        with self.voiceover(
            text="Lấy logarit cả hai vế: ln X bằng Y, đưa bài toán về phân phối chuẩn."
        ) as tracker:
            self.show_subtitle(
                "ln(X) = Y ~ Normal — the core insight.",
                "ln(X) = Y chuẩn — ý tưởng then chốt.",
            )
            self.play(FadeOut(def_grp, shift=UP), run_time=min(0.8, tracker.duration * 0.5))

        # ══════════════════════════════════════════════════════
        # SCENE 5 — Formulas: μ, σ², PDF, CDF
        # ══════════════════════════════════════════════════════
        label_1 = Text("1. Kỳ vọng và Phương sai của ln(X)", font_size=19, color=GREEN_A, font="Arial")
        math_1  = MathTex(
            r"\mu = \ln \frac{\mu_X^2}{\sqrt{\mu^2_X + \sigma^2_X}} \quad;\quad"
            r"\sigma^2 = \ln \!\left(1 + \frac{\sigma^2_X}{\mu^2_X}\right)",
            font_size=30,
        )
        box_1  = self.soft_box(math_1, WHITE)
        item_1 = VGroup(label_1, math_1, box_1)
        label_1.next_to(box_1, UP, buff=0.18)
        item_1.move_to(ORIGIN)

        label_2 = Text("2. Hàm mật độ xác suất (PDF)", font_size=19, color=GREEN_A, font="Arial")
        math_2  = MathTex(
            r"f_X(x) = \frac{1}{x\sigma\sqrt{2\pi}}"
            r"\exp\!\left(-\frac{(\ln x-\mu)^2}{2\sigma^2}\right)",
            font_size=30,
        )
        box_2  = self.soft_box(math_2, GREEN_D)
        item_2 = VGroup(label_2, math_2, box_2)
        label_2.next_to(box_2, UP, buff=0.18)
        item_2.move_to(ORIGIN + DOWN * 0.2)

        label_3 = Text("3. Hàm phân phối tích lũy (CDF)", font_size=19, color=GREEN_A, font="Arial")
        math_3  = MathTex(
            r"P(X \le x) = \Phi\!\left(\frac{\ln x - \mu}{\sigma}\right)",
            font_size=30,
        )
        box_3  = self.soft_box(math_3, BLUE_D)
        item_3 = VGroup(label_3, math_3, box_3)
        label_3.next_to(box_3, UP, buff=0.18)
        item_3.move_to(ORIGIN + DOWN * 1.2)

        # ── VO 10 ── (~6s)
        with self.voiceover(
            text="Công thức kỳ vọng và phương sai mu, sigma bình phương của ln X."
        ) as tracker:
            self.show_subtitle(
                "Formulas: μ and σ² of ln(X).",
                "Công thức: μ và σ² của ln(X).",
            )
            self.play(FadeIn(item_1, shift=DOWN), run_time=min(1.2, tracker.duration * 0.6))

        # ── VO 11 ── (~7s)
        with self.voiceover(
            text="Hàm mật độ PDF và phân phối tích lũy CDF — ngôn ngữ kỹ sư độ bền."
        ) as tracker:
            self.show_subtitle(
                "PDF & CDF — engineer's lifespan language.",
                "PDF & CDF — ngôn ngữ kỹ sư độ bền.",
            )
            self.play(
                item_1.animate.shift(UP * 2.2).scale(0.85),
                FadeIn(item_2, shift=DOWN),
                run_time=min(1.2, tracker.duration * 0.45),
            )
            self.play(
                item_1.animate.shift(UP * 1.8),
                item_2.animate.shift(UP * 1.6).scale(0.85),
                FadeIn(item_3, shift=DOWN),
                run_time=min(1.2, tracker.duration * 0.45),
            )

        # Xóa sạch bộ 3 — liệt kê tường minh
        self.play(FadeOut(item_1), FadeOut(item_2), FadeOut(item_3), run_time=0.8)

        # ══════════════════════════════════════════════════════
        # SCENE 6 — Estimation: Student & Chi-squared
        # ══════════════════════════════════════════════════════
        label_e1 = Text("Ước lượng Kỳ vọng  —  Phân phối Student", font_size=22, color=ORANGE, font="Arial")
        math_e1  = MathTex(
            r"\left(\bar{y} - t_{\alpha/2,n-1}\frac{s_y}{\sqrt{n}}\ ;\ "
            r"\bar{y} + t_{\alpha/2,n-1}\frac{s_y}{\sqrt{n}}\right)",
            font_size=36,
        )
        box_e1  = self.soft_box(math_e1, WHITE)
        item_e1 = VGroup(label_e1, math_e1, box_e1).move_to(ORIGIN)
        label_e1.next_to(box_e1, UP, buff=0.28)

        label_e2 = Text("Ước lượng Phương sai  —  Chi-bình phương", font_size=22, color=ORANGE, font="Arial")
        math_e2  = MathTex(
            r"\left(\frac{(n-1)s_y^2}{\chi^2_{\alpha/2,n-1}}\ ;\ "
            r"\frac{(n-1)s_y^2}{\chi^2_{1-\alpha/2,n-1}}\right)",
            font_size=36,
        )
        box_e2  = self.soft_box(math_e2, ORANGE)
        item_e2 = VGroup(label_e2, math_e2, box_e2)
        label_e2.next_to(box_e2, UP, buff=0.28)

        # ── VO 12 ── (~7s)
        with self.voiceover(
            text="Đặt y i bằng logarit x i để chuẩn hóa dữ liệu, rồi áp dụng thống kê đại cương."
        ) as tracker:
            self.show_subtitle(
                "Set y_i=ln(x_i) → normalize data.",
                "Đặt y_i=ln(x_i) → chuẩn hóa dữ liệu.",
            )
            self.play(
                Write(label_e1), Create(box_e1), Write(math_e1),
                run_time=min(1.4, tracker.duration * 0.55),
            )
            self.play(
                item_e1.animate.shift(UP * 1.8).scale(0.9),
                run_time=min(0.8, tracker.duration * 0.3),
            )

        # Position item_e2 relative to shifted item_e1
        item_e2.next_to(item_e1, DOWN, buff=0.9)

        # ── VO 13 ── (~5s)
        with self.voiceover(
            text="Kỳ vọng dùng phân phối Student; phương sai dùng Chi-bình phương."
        ) as tracker:
            self.show_subtitle(
                "Mean→Student's t; Variance→Chi-squared.",
                "Kỳ vọng→Student; Phương sai→Chi²",
            )
            self.play(
                Write(label_e2), Create(box_e2), Write(math_e2),
                run_time=min(1.2, tracker.duration * 0.6),
            )
            self.play(
                Indicate(math_e1, color=ORANGE),
                Indicate(math_e2, color=ORANGE),
                run_time=min(0.8, tracker.duration * 0.3),
            )

        # ══════════════════════════════════════════════════════
        # SCENE 7 — Final graph: safety lower bound
        # ══════════════════════════════════════════════════════
        with self.voiceover(
            text="Sau khi có đủ công cụ, nhà máy đưa ra quyết định bảo trì cuối cùng."
        ) as tracker:
            self.show_subtitle(
                "With all tools ready — the factory decides.",
                "Đủ công cụ — nhà máy đưa ra quyết định.",
            )
            self.play(FadeOut(*self.mobjects), run_time=min(0.7, tracker.duration * 0.4))

        title2 = self.create_title(
            "ƯỚC LƯỢNG ĐỘ BỀN LINH KIỆN PISTON TRONG ĐỘNG CƠ Ô TÔ"
        )
        self.play(Write(title2), run_time=0.8)

        outro_axes = Axes(
            x_range=[0, 10, 2], y_range=[0, 1.4, 0.4],
            x_length=7.5, y_length=3.0,
            axis_config={"include_tip": True},
        ).move_to(ORIGIN + DOWN * 1.0)

        y_unit = Text("% Hỏng",       font_size=15, font="Arial").next_to(outro_axes.y_axis.get_top(), LEFT,  buff=0.1)
        x_unit = Text("Tuổi thọ (giờ)", font_size=15, font="Arial").next_to(outro_axes.x_axis.get_end(),  DOWN, buff=0.1)

        def final_lognorm(x):
            if x <= 0: return 0
            return (1.6 / (x * 0.6)) * np.exp(-((np.log(x / 2.5)) ** 2) / (2 * 0.6 ** 2))

        curve   = outro_axes.plot(final_lognorm, x_range=[0.1, 9], color=WHITE)
        t_peak  = 1.6
        t_mean  = 3.5
        line_safe  = outro_axes.get_vertical_line(outro_axes.c2p(t_peak, final_lognorm(t_peak)), color=GREEN)
        label_safe = Text("Mốc an toàn (Cận dưới)", font_size=13, color=GREEN, font="Arial").next_to(
            outro_axes.c2p(t_peak, final_lognorm(t_peak)), UP, buff=0.18
        )
        line_mean  = outro_axes.get_vertical_line(outro_axes.c2p(t_mean, final_lognorm(t_mean)), color=RED)
        label_mean = Text("Giá trị trung bình", font_size=13, color=RED, font="Arial").next_to(
            outro_axes.c2p(t_mean, final_lognorm(t_mean)), UP + RIGHT, buff=0.18
        )

        # ── VO 14 ── (~6s)
        with self.voiceover(
            text="Đường cong Log-Chuẩn: xanh là cận dưới an toàn, đỏ là giá trị trung bình."
        ) as tracker:
            self.show_subtitle(
                "Green=lower bound (safe); Red=mean.",
                "Xanh=cận dưới an toàn; Đỏ=trung bình.",
            )
            self.play(
                Create(outro_axes), Write(VGroup(y_unit, x_unit)),
                run_time=min(0.9, tracker.duration * 0.25),
            )
            self.play(Create(curve), run_time=min(1.0, tracker.duration * 0.3))
            self.play(
                Create(line_safe), Write(label_safe),
                Create(line_mean), Write(label_mean),
                run_time=min(0.9, tracker.duration * 0.25),
            )

        risk_area = outro_axes.get_area(curve, x_range=[t_peak, 9], color=RED_E, opacity=0.3)
        safe_text = Text("NGĂN CHẶN HỎNG HÓC SỚM", font_size=28, color=YELLOW, font="Arial").move_to(UP * 2.2)
        safe_box  = SurroundingRectangle(safe_text, color=YELLOW, buff=0.18, corner_radius=0.1)

        # ── VO 15 ── (~8s)
        with self.voiceover(
            text="Kỹ sư luôn chọn cận dưới làm mốc bảo trì — ngăn chặn hỏng hóc trước khi nó xảy ra."
        ) as tracker:
            self.show_subtitle(
                "Lower bound = maintenance threshold.",
                "Cận dưới = mốc bảo trì — ngăn hỏng hóc.",
            )
            self.play(FadeIn(risk_area), run_time=min(0.8, tracker.duration * 0.2))
            self.play(
                Write(safe_text), Create(safe_box),
                run_time=min(1.0, tracker.duration * 0.3),
            )
            self.play(
                Indicate(safe_text, color=YELLOW),
                run_time=min(0.8, tracker.duration * 0.2),
            )
            self.wait(min(2.0, tracker.duration * 0.25))

        self.clear_subtitle()
        self.play(FadeOut(*self.mobjects), run_time=1.0)
        self.wait(0.5)


if __name__ == "__main__":
    scene = mainScene()
    scene.render()