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
# HELPER: Bilingual subtitle  (English on top, Vietnamese below)
# EN: Arial 22 white  |  VI: Arial 18 yellow
# ─────────────────────────────────────────────────────────────
def make_subtitle(en_text: str, vi_text: str):
    en = Text(en_text, font="Arial", font_size=22, color=WHITE)
    vi = Text(vi_text, font="Arial", font_size=18, color=YELLOW)
    vi.next_to(en, DOWN, buff=0.12)
    group = VGroup(en, vi)
    group.to_edge(DOWN, buff=0.28)
    return group


class mainScene(FaMIBaseScene):
    # ── override update_subtitle to handle bilingual pairs ──
    def show_subtitle(self, en_text: str, vi_text: str):
        """Fade old subtitle out, fade new bilingual subtitle in."""
        if hasattr(self, "_current_subtitle") and self._current_subtitle in self.mobjects:
            self.remove(self._current_subtitle)
        sub = make_subtitle(en_text, vi_text)
        sub.set_z_index(10)
        self.add(sub)
        self._current_subtitle = sub

    def construct(self):
        # ══════════════════════════════════════════════════════
        # SCENE 1 — Intro: Normal distribution is insufficient
        # ══════════════════════════════════════════════════════
        title = self.create_title("ƯỚC LƯỢNG ĐỘ BỀN LINH KIỆN PISTON TRONG ĐỘNG CƠ Ô TÔ")

        text_title = Tex(
            r"Phân phối chuẩn có phù hợp để dùng trong việc \\ước lượng độ bền linh kiện piston không?",
            font_size=40
        )
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 0.5, 0.1],
            x_length=8,
            y_length=4,
            axis_config={"include_tip": False}
        )

        def gaussian(x, mu=0, sigma=1):
            return (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)

        graph = axes.plot(lambda x: gaussian(x), color=BLUE).set_fill(opacity=0)
        negative_area = axes.get_area(
            graph, x_range=[-4, 0], color=RED, opacity=0.8
        ).set_stroke(RED, width=2)

        # ── Voiceover 1 ──
        with self.voiceover(
            text="Ước lượng độ bền linh kiện piston trong động cơ ô tô là bài toán cực kỳ quan trọng. "
                 "Nhưng liệu phân phối chuẩn có đủ sức đáp ứng nhu cầu của các kỹ sư không?"
        ) as tracker:
            self.show_subtitle(
                "Estimating piston component durability is critical.",
                "Ước lượng độ bền linh kiện piston rất quan trọng."
            )
            self.play(Write(title), run_time=min(1.5, tracker.duration * 0.35))
            self.show_subtitle(
                "But is the normal distribution enough for engineers?",
                "Liệu phân phối chuẩn có đủ cho các kỹ sư không?"
            )
            self.play(Create(axes), run_time=min(1.5, tracker.duration * 0.35))

        # ── Voiceover 2 ──
        with self.voiceover(
            text="Phân phối chuẩn nhận cả giá trị âm — điều hoàn toàn vô lý với tuổi thọ linh kiện. "
                 "Một linh kiện không thể có tuổi thọ âm!"
        ) as tracker:
            self.show_subtitle(
                "Normal distribution accepts negative values — impossible for lifespan!",
                "Phân phối chuẩn nhận giá trị âm — điều vô lý với tuổi thọ linh kiện!"
            )
            self.play(Create(graph), run_time=min(1.2, tracker.duration * 0.3))
            self.play(Write(text_title.next_to(axes, UP)), run_time=min(1.2, tracker.duration * 0.25))
            self.play(DrawBorderThenFill(negative_area), run_time=min(1.2, tracker.duration * 0.25))

        math_logic = MathTex(
            "x < 0", "\\Rightarrow", "\\text{Tuổi thọ} < 0", "\\text{ (Vô lý!)}",
            font_size=36
        ).set_color(YELLOW)
        math_logic.next_to(negative_area, DOWN, buff=0.5)

        # ── Voiceover 3 ──
        with self.voiceover(
            text="Nhìn vào vùng đỏ này — đó là xác suất tuổi thọ âm theo phân phối chuẩn. "
                 "Hoàn toàn vô nghĩa về mặt vật lý. Phân phối chuẩn không phải lựa chọn cuối cùng."
        ) as tracker:
            self.show_subtitle(
                "The red zone: probability of negative lifespan — physically meaningless.",
                "Vùng đỏ: xác suất tuổi thọ âm — hoàn toàn vô nghĩa vật lý."
            )
            self.play(Write(math_logic[0]), run_time=min(0.8, tracker.duration * 0.15))
            self.play(Write(math_logic[1]), Write(math_logic[2]), run_time=min(1.0, tracker.duration * 0.2))
            self.show_subtitle(
                "Normal distribution is NOT the right choice for this problem.",
                "Phân phối chuẩn KHÔNG phải lựa chọn phù hợp cho bài toán này."
            )
            self.play(Indicate(math_logic[3], color=RED), run_time=min(0.8, tracker.duration * 0.15))
            everything_wrong = VGroup(graph, negative_area, math_logic, axes, text_title)
            cross = Cross(everything_wrong, stroke_width=15).set_color(WHITE)
            self.play(Create(cross), run_time=min(1.0, tracker.duration * 0.2))
            self.play(FadeOut(everything_wrong), FadeOut(cross), run_time=min(1.0, tracker.duration * 0.15))

        # ══════════════════════════════════════════════════════
        # SCENE 2 — Smart solution: Log-normal distribution
        # ══════════════════════════════════════════════════════
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

        # ── Voiceover 4 ──
        with self.voiceover(
            text="Nhưng người thông minh như bạn không dừng lại ở đó. "
                 "Bạn đặt câu hỏi: có cách nào khắc phục nhược điểm này không?"
        ) as tracker:
            self.show_subtitle(
                "But a smart engineer like you doesn't stop there.",
                "Nhưng người thông minh như bạn không dừng lại ở đó."
            )
            self.play(FadeIn(student, shift=UP), run_time=min(1.0, tracker.duration * 0.3))
            self.show_subtitle(
                "You ask: is there a way to fix this flaw?",
                "Bạn đặt câu hỏi: có cách nào khắc phục nhược điểm này không?"
            )
            self.play(LaggedStart(*[Write(q) for q in q_group], lag_ratio=0.3), run_time=min(1.5, tracker.duration * 0.5))

        spark_center = bulb_glass.get_top() + UP * 0.2
        glow_lines = VGroup(*[
            Line(spark_center + 0.1 * d, spark_center + 0.5 * d).set_stroke(YELLOW, 4)
            for d in [UP, UL, UR, LEFT, RIGHT]
        ])

        # ── Voiceover 5 ──
        with self.voiceover(
            text="Và rồi, một giải pháp chói sáng đã bùng lên — phân phối log-chuẩn!"
        ) as tracker:
            self.show_subtitle(
                "And then — a brilliant solution lights up!",
                "Và rồi — một giải pháp chói sáng bùng lên!"
            )
            self.play(
                FadeOut(q_group, scale=0.5),
                FadeIn(bulb_base),
                bulb_glass.animate.set_fill(YELLOW, opacity=0.8),
                run_time=min(1.0, tracker.duration * 0.4)
            )
            self.play(
                Create(glow_lines),
                Indicate(bulb_glass, scale_factor=1.2),
                run_time=min(1.0, tracker.duration * 0.35)
            )

        to_remove = Group(*[mob for mob in self.mobjects if mob != title])
        self.play(FadeOut(to_remove), run_time=0.6)

        log_normal_big_tex = Tex("Phân phối Log-Chuẩn", color=GREEN, font_size=72).move_to(ORIGIN)

        # ── Voiceover 6 ──
        with self.voiceover(
            text="Đó chính là: Phân phối Log-Chuẩn! "
                 "Công cụ mà các kỹ sư độ bền tin dùng để đọc vị tuổi thọ linh kiện."
        ) as tracker:
            self.show_subtitle(
                "The Log-Normal Distribution — the engineer's tool for predicting lifespan.",
                "Phân phối Log-Chuẩn — công cụ kỹ sư độ bền tin dùng."
            )
            self.play(
                Write(log_normal_big_tex),
                log_normal_big_tex.animate.scale(1.2),
                run_time=min(1.5, tracker.duration * 0.6)
            )

        # ══════════════════════════════════════════════════════
        # SCENE 3 — Why Log-Normal? 3 reasons
        # ══════════════════════════════════════════════════════
        chot_ha_title = Tex(r"Tại sao chọn Log-Chuẩn?", color=WHITE, font_size=40)
        chot_ha_title.next_to(title, DOWN, buff=0.3)

        # ── Voiceover 7 ──
        with self.voiceover(
            text="Vậy tại sao lại là phân phối log-chuẩn? Hãy cùng xem xét ba lý do then chốt."
        ) as tracker:
            self.show_subtitle(
                "Why Log-Normal? Let's explore 3 key reasons.",
                "Tại sao Log-Chuẩn? Hãy xem 3 lý do then chốt."
            )
            self.play(
                Transform(log_normal_big_tex, chot_ha_title),
                run_time=min(1.2, tracker.duration * 0.5)
            )

        axes_final = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 5, 1],
            x_length=8,
            y_length=3.5,
            axis_config={"include_tip": True, "tip_shape": StealthTip},
        ).shift(DOWN * 1.0)

        x_lab = axes_final.get_x_axis_label(Tex("Tuổi thọ", font_size=30))
        y_lab = axes_final.get_y_axis_label(Tex(r"\% Hỏng", font_size=30))

        with self.voiceover(
            text="Đây là hệ trục biểu diễn tỉ lệ hỏng hóc theo tuổi thọ linh kiện."
        ) as tracker:
            self.show_subtitle(
                "This axis shows failure rate vs. component lifespan.",
                "Hệ trục biểu diễn tỉ lệ hỏng hóc theo tuổi thọ linh kiện."
            )
            self.play(
                Create(axes_final),
                Write(VGroup(x_lab, y_lab)),
                run_time=min(1.5, tracker.duration * 0.6)
            )

        tex_pos = UP * 1.2

        # ── Voiceover 8 — Reason 1 ──
        with self.voiceover(
            text="Lý do thứ nhất — bản chất vật lý: vết nứt mỏi trong piston tích lũy theo cấp số nhân, "
                 "không phải tuyến tính. Log-chuẩn mô tả chính xác cơ chế này."
        ) as tracker:
            self.show_subtitle(
                "Reason 1 — Physics: fatigue cracks accumulate exponentially.",
                "Lý do 1 — Bản chất: vết nứt tích lũy theo cấp số nhân."
            )
            tex_reason_1 = Tex(
                r"1. Vết nứt tích lũy theo cấp số nhân",
                color=YELLOW_E, font_size=34
            ).move_to(tex_pos)

            def exp_func(x):
                return 0.1 * np.exp(0.45 * x)

            curve_exp = axes_final.plot(exp_func, x_range=[0.1, 8.5], color=YELLOW_E)
            self.play(Write(tex_reason_1), run_time=min(1.0, tracker.duration * 0.25))
            self.show_subtitle(
                "Log-Normal accurately captures this exponential growth mechanism.",
                "Log-Chuẩn mô tả chính xác cơ chế tăng trưởng cấp số nhân này."
            )
            self.play(Create(curve_exp), run_time=min(1.5, tracker.duration * 0.35))
            self.play(FadeOut(curve_exp), FadeOut(tex_reason_1), run_time=min(0.8, tracker.duration * 0.2))

        # ── Voiceover 9 — Reason 2 ──
        with self.voiceover(
            text="Lý do thứ hai — logic toán học: tuổi thọ linh kiện luôn phải dương, tức t lớn hơn không. "
                 "Phân phối log-chuẩn đảm bảo điều này tuyệt đối, không bao giờ sinh ra giá trị âm."
        ) as tracker:
            self.show_subtitle(
                "Reason 2 — Logic: lifespan must always be positive (t > 0).",
                "Lý do 2 — Logic: tuổi thọ luôn dương (t > 0)."
            )
            tex_reason_2 = Tex(
                r"2. Tuổi thọ luôn dương ($t > 0$)",
                color=RED_E, font_size=34
            ).move_to(tex_pos)

            def normal_func(x):
                return 4 * np.exp(-((x - 4)**2) / (2 * 1.2**2))

            curve_normal_final = axes_final.plot(normal_func, x_range=[0, 10], color=RED_D)
            self.play(Write(tex_reason_2), run_time=min(1.0, tracker.duration * 0.25))
            self.show_subtitle(
                "Log-Normal guarantees no negative values — ever.",
                "Log-Chuẩn đảm bảo không bao giờ sinh ra giá trị âm."
            )
            self.play(Create(curve_normal_final), run_time=min(1.5, tracker.duration * 0.35))

        # ── Voiceover 10 — Reason 3 ──
        with self.voiceover(
            text="Lý do thứ ba — thực tế: dữ liệu piston thực luôn có đuôi dài về phía phải. "
                 "Đó là những chiếc piston đặc biệt bền hơn số đông. Log-chuẩn khớp hoàn hảo với hình dạng này."
        ) as tracker:
            self.show_subtitle(
                "Reason 3 — Reality: real piston data has a right-skewed tail.",
                "Lý do 3 — Thực tế: dữ liệu piston thực có đuôi lệch phải."
            )
            tex_reason_3 = Tex(
                r"3. Khớp hoàn hảo dữ liệu Piston",
                color=ORANGE, font_size=34
            ).move_to(tex_pos)

            def lognorm_final(x):
                if x <= 0: return 0
                return (3.8 / (x * 0.7)) * np.exp(-((np.log(x / 1.8))**2) / (2 * 0.7**2))

            curve_lognorm_final = axes_final.plot(lognorm_final, x_range=[0.1, 10], color=GREEN_D)
            tail_fill_final = axes_final.get_area(
                curve_lognorm_final, x_range=[4.5, 9.5], color=YELLOW, opacity=0.6
            )
            piston_ben_text = Tex(
                "Piston siêu bền", color=YELLOW, font_size=28
            ).move_to(axes_final.c2p(7.5, 1.2))

            self.play(
                Transform(tex_reason_2, tex_reason_3),
                Transform(curve_normal_final, curve_lognorm_final),
                run_time=min(1.5, tracker.duration * 0.35)
            )
            self.show_subtitle(
                "The right tail represents exceptionally durable pistons.",
                "Đuôi phải: những chiếc piston có độ bền vượt trội."
            )
            self.play(FadeIn(tail_fill_final), Write(piston_ben_text), run_time=min(1.2, tracker.duration * 0.3))

        # ══════════════════════════════════════════════════════
        # SCENE 4 — Definition of Log-Normal
        # ══════════════════════════════════════════════════════
        keep_only = [title]
        to_remove = []
        for mob in self.mobjects:
            if mob in keep_only:
                continue
            if "ImageMobject" in str(type(mob)):
                continue
            to_remove.append(mob)

        with self.voiceover(
            text="Giờ hãy làm rõ định nghĩa chính xác của phân phối log-chuẩn."
        ) as tracker:
            self.show_subtitle(
                "Now let's clarify the exact definition of the Log-Normal distribution.",
                "Hãy làm rõ định nghĩa chính xác của phân phối log-chuẩn."
            )
            self.play(*[FadeOut(mob) for mob in to_remove], run_time=min(0.8, tracker.duration * 0.6))

        def get_soft_box(mobject, color=YELLOW):
            return SurroundingRectangle(mobject, color=color, buff=0.3, corner_radius=0.2)

        intro_label = Text(
            "Định nghĩa biến ngẫu nhiên Log-Chuẩn",
            font_size=24, color=BLUE_B, font="Noto Sans"
        ).shift(UP * 1.2)
        def_math = MathTex(r"X = e^{\mu + \sigma Y}", font_size=48)
        def_box = get_soft_box(def_math, YELLOW)
        definition_group = VGroup(intro_label, def_math, def_box).move_to(ORIGIN)

        # ── Voiceover 11 ──
        with self.voiceover(
            text="Cho Y là biến ngẫu nhiên chuẩn tắc, mu và sigma là hai số thực với sigma lớn hơn không. "
                 "Khi đó, biến ngẫu nhiên X bằng e mũ mu cộng sigma nhân Y tuân theo phân phối log-chuẩn."
        ) as tracker:
            self.show_subtitle(
                "Let Y ~ N(0,1). Then X = e^(μ + σY) follows a Log-Normal distribution.",
                "Cho Y chuẩn tắc, khi đó X = e^{μ + σY} tuân theo phân phối log-chuẩn."
            )
            self.play(Write(intro_label), run_time=min(1.0, tracker.duration * 0.2))
            self.play(FadeIn(def_math, scale=1.2), Create(def_box), run_time=min(1.5, tracker.duration * 0.4))

        # ── Voiceover 12 ──
        with self.voiceover(
            text="Ý tưởng cốt lõi rất thanh lịch: khi lấy logarit của X, ta thu được Y tuân theo phân phối chuẩn. "
                 "Tức là, log-chuẩn chính là logarit của biến ngẫu nhiên tuân theo phân phối chuẩn."
        ) as tracker:
            self.show_subtitle(
                "Core idea: taking ln(X) gives Y ~ Normal. Log-Normal = log of a Normal variable.",
                "Ý tưởng cốt lõi: ln(X) = Y tuân theo chuẩn. Log-Chuẩn = logarit của biến chuẩn."
            )
            self.play(FadeOut(definition_group, shift=UP), run_time=min(1.0, tracker.duration * 0.5))

        # ══════════════════════════════════════════════════════
        # SCENE 5 — Formulas: μ, σ², PDF, CDF
        # ══════════════════════════════════════════════════════
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

        # ── Voiceover 13 ──
        with self.voiceover(
            text="Từ định nghĩa đó, ta suy ra các công thức quan trọng. "
                 "Đầu tiên là mu và sigma bình phương — kỳ vọng và phương sai của logarit dữ liệu."
        ) as tracker:
            self.show_subtitle(
                "From the definition, we derive key formulas. First: μ and σ² of ln(X).",
                "Từ định nghĩa, ta suy ra công thức quan trọng. Trước tiên: μ và σ² của ln(X)."
            )
            self.play(FadeIn(item_1, shift=DOWN), run_time=min(1.5, tracker.duration * 0.5))

        # ── Voiceover 14 ──
        with self.voiceover(
            text="Tiếp theo là hàm mật độ xác suất PDF — cho biết xác suất linh kiện hỏng tại từng thời điểm."
        ) as tracker:
            self.show_subtitle(
                "Next: the PDF — probability of failure at each time point.",
                "Tiếp theo: hàm PDF — xác suất hỏng tại từng thời điểm."
            )
            self.play(
                item_1.animate.shift(UP * 2.2).scale(0.85),
                FadeIn(item_2, shift=DOWN),
                run_time=min(1.5, tracker.duration * 0.55)
            )

        # ── Voiceover 15 ──
        with self.voiceover(
            text="Và hàm phân phối tích lũy CDF — xác suất linh kiện hỏng trước thời điểm x. "
                 "Những ký tự mu, sigma và hàm Phi này chính là ngôn ngữ của kỹ sư độ bền trong công nghiệp."
        ) as tracker:
            self.show_subtitle(
                "The CDF: P(X ≤ x) — probability of failure before time x.",
                "Hàm CDF: P(X ≤ x) — xác suất hỏng trước thời điểm x."
            )
            self.play(
                item_1.animate.shift(UP * 1.8),
                item_2.animate.shift(UP * 1.6).scale(0.85),
                FadeIn(item_3, shift=DOWN),
                run_time=min(1.5, tracker.duration * 0.35)
            )
            self.show_subtitle(
                "μ, σ and Φ are the language engineers use to predict component lifespan.",
                "μ, σ và hàm Φ — ngôn ngữ kỹ sư dùng để đọc vị tuổi thọ linh kiện."
            )
            self.play(FadeOut(item_1), FadeOut(item_2), FadeOut(item_3), run_time=min(0.8, tracker.duration * 0.2))

        # ══════════════════════════════════════════════════════
        # SCENE 6 — Estimation formulas: Student & Chi-square
        # ══════════════════════════════════════════════════════
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

        # ── Voiceover 16 ──
        with self.voiceover(
            text="Tại phòng lab, các kỹ sư lấy n piston đem thử nghiệm phá hủy. "
                 "Kết quả đạt đỉnh ở một khoảng nhất định, nhưng luôn có những piston đặc biệt bền hơn hay kém hơn số đông — "
                 "tạo nên phần đuôi lệch phải đặc trưng."
        ) as tracker:
            self.show_subtitle(
                "In the lab: n pistons undergo destructive testing.",
                "Tại phòng lab: n piston được thử nghiệm phá hủy."
            )
            self.play(
                Write(label_est_1),
                Create(box_est_1),
                Write(math_est_1),
                run_time=min(1.5, tracker.duration * 0.35)
            )
            self.show_subtitle(
                "Results peak at a range, but outliers create the right-skewed tail.",
                "Kết quả có đỉnh xác định, nhưng luôn có piston bền hơn — tạo đuôi lệch phải."
            )
            self.play(
                item_est_1.animate.shift(UP * 1.8).scale(0.9),
                run_time=min(1.0, tracker.duration * 0.25)
            )

        # ── Voiceover 17 ──
        with self.voiceover(
            text="Nhà máy không thể xác định một thời điểm hỏng cụ thể — họ cần khoảng ước lượng. "
                 "Bằng cách đặt y i bằng logarit x i, dữ liệu chuyển về dạng chuẩn và ta áp dụng được thống kê đại cương."
        ) as tracker:
            self.show_subtitle(
                "The factory needs a confidence interval, not a single point estimate.",
                "Nhà máy cần khoảng ước lượng, không phải một điểm cụ thể."
            )
            self.play(
                Write(label_est_2),
                Create(box_est_2),
                Write(math_est_2),
                run_time=min(1.5, tracker.duration * 0.35)
            )
            self.show_subtitle(
                "Set y_i = ln(x_i) → data becomes Normal → apply classical statistics.",
                "Đặt y_i = ln(x_i) → dữ liệu chuẩn hóa → áp dụng thống kê đại cương."
            )

        # ── Voiceover 18 ──
        with self.voiceover(
            text="Để ước lượng độ bền trung bình, kỹ sư dùng phân phối Student với n trừ một bậc tự do. "
                 "Để kiểm soát độ đồng đều lô hàng, họ dùng phân phối Chi-bình phương cho phương sai."
        ) as tracker:
            self.show_subtitle(
                "Mean lifespan → Student's t-distribution (n−1 degrees of freedom).",
                "Độ bền trung bình → phân phối Student (n−1 bậc tự do)."
            )
            self.play(Indicate(math_est_1, color=ORANGE), run_time=min(1.0, tracker.duration * 0.3))
            self.show_subtitle(
                "Variance consistency → Chi-squared distribution.",
                "Độ đồng đều lô hàng → phân phối Chi-bình phương."
            )
            self.play(Indicate(math_est_2, color=ORANGE), run_time=min(1.0, tracker.duration * 0.3))

        # ══════════════════════════════════════════════════════
        # SCENE 7 — Final graph: safety benchmark
        # ══════════════════════════════════════════════════════
        title = self.create_title("ƯỚC LƯỢNG ĐỘ BỀN LINH KIỆN PISTON TRONG ĐỘNG CƠ Ô TÔ")
        with self.voiceover(
            text="Sau khi có đầy đủ công cụ, nhà máy đưa ra quyết định thực tế cuối cùng."
        ) as tracker:
            self.show_subtitle(
                "With all tools ready, the factory makes its final practical decision.",
                "Đã có đủ công cụ, nhà máy đưa ra quyết định thực tế cuối cùng."
            )
            self.play(FadeOut(*self.mobjects), run_time=min(0.8, tracker.duration * 0.4))
            self.play(Write(title), run_time=min(1.2, tracker.duration * 0.4))

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
        line_safe = outro_axes.get_vertical_line(
            outro_axes.c2p(t_peak, final_lognorm(t_peak)), color=GREEN
        )
        label_safe = Text(
            "Mốc an toàn (Cận dưới)", font_size=14, color=GREEN, font="Arial"
        ).next_to(outro_axes.c2p(t_peak, final_lognorm(t_peak)), UP, buff=0.2)
        line_mean = outro_axes.get_vertical_line(
            outro_axes.c2p(t_mean, final_lognorm(t_mean)), color=RED
        )
        label_mean = Text(
            "Giá trị trung bình", font_size=14, color=RED, font="Arial"
        ).next_to(outro_axes.c2p(t_mean, final_lognorm(t_mean)), UP + RIGHT, buff=0.2)

        # ── Voiceover 19 ──
        with self.voiceover(
            text="Đây là đường cong log-chuẩn ước lượng cho lô piston. "
                 "Đường xanh là cận dưới — mốc an toàn. Đường đỏ là giá trị trung bình."
        ) as tracker:
            self.show_subtitle(
                "The Log-Normal curve for the piston batch.",
                "Đường cong log-chuẩn ước lượng cho lô piston."
            )
            self.play(Create(outro_axes), Write(axis_labels), run_time=min(1.2, tracker.duration * 0.3))
            self.play(Create(curve), run_time=min(1.2, tracker.duration * 0.3))
            self.show_subtitle(
                "Green line = lower bound (safety benchmark). Red = mean estimate.",
                "Đường xanh = cận dưới (mốc an toàn). Đường đỏ = giá trị trung bình."
            )
            self.play(Create(line_safe), Write(label_safe), run_time=min(0.8, tracker.duration * 0.1))
            self.play(Create(line_mean), Write(label_mean), run_time=min(0.8, tracker.duration * 0.1))

        risk_area = outro_axes.get_area(curve, x_range=[t_peak, 9], color=RED_E, opacity=0.3)
        safe_text = Text(
            "NGĂN CHẶN HỎNG HÓC SỚM", font_size=30, color=YELLOW, font="Arial"
        ).move_to(UP * 2.4)
        safe_box = SurroundingRectangle(safe_text, color=YELLOW, buff=0.2, corner_radius=0.1)

        # ── Voiceover 20 ──
        with self.voiceover(
            text="Thay vì chọn giá trị trung bình đầy rủi ro, các kỹ sư luôn lấy cận dưới làm mốc bảo dưỡng. "
                 "Đây là thời điểm an toàn nhất để bảo trì — ngăn chặn mọi hỏng hóc trước khi nó kịp xảy ra."
        ) as tracker:
            self.show_subtitle(
                "Engineers choose the lower bound — not the mean — as maintenance threshold.",
                "Kỹ sư chọn cận dưới — không phải trung bình — làm mốc bảo trì."
            )
            self.play(FadeIn(risk_area), run_time=min(1.0, tracker.duration * 0.25))
            self.show_subtitle(
                "This is the safest moment to act — preventing failure before it happens.",
                "Đây là thời điểm an toàn nhất — ngăn chặn hỏng hóc trước khi nó xảy ra."
            )
            self.play(Write(safe_text), Create(safe_box), run_time=min(1.2, tracker.duration * 0.3))
            self.play(Indicate(safe_text, color=YELLOW), run_time=min(0.8, tracker.duration * 0.2))


if __name__ == "__main__":
    scene = mainScene()
    scene.render()