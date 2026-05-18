import os
import sys
import subprocess
import ctypes
import sys as sys_lib

PROJECT_ROOT = r'C:\Users\doman\Downloads\Project1-main\Roo-Code'

if os.getcwd() != PROJECT_ROOT:
    os.chdir(PROJECT_ROOT)

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

# 2. Import thư viện cốt lõi của Manim
from manim import *

# 3. Import toàn bộ thư viện custom của bạn

from skills.fami_lib import *
from skills.fami_assets_helper import *
from skills.fami_effects import * # Import thêm file này phòng trường hợp các hiệu ứng nằm ở đây
config.tex_template = TexTemplate()
config.tex_template.add_to_preamble(r"\usepackage[utf8]{vietnam}")
config.verbosity = "ERROR"
import warnings
warnings.filterwarnings('ignore')
import sys
import os
from pathlib import Path
from IPython.display import Video, display
from scipy import stats
import math
import numpy as np
from manim import *
import random

# 1. Cấu hình đường dẫn và thông số render
config.media_dir = r"C:\Users\doman\Downloads\Project1-main\Roo-Code\media"
config.pixel_width = 720   # Độ phân giải dọc 720x1280
config.pixel_height = 1280
config.frame_rate = 15
config.disable_caching = True 
config.verbosity = "ERROR" # Tắt các dòng log thừa

# 2. Đảm bảo thư mục tồn tại
os.makedirs(config.media_dir, exist_ok=True)

# 3. Ép môi trường nhận FFmpeg (nếu cần)
ffmpeg_bin = r"C:\ffmpeg\bin"
if ffmpeg_bin not in os.environ["PATH"]:
    os.environ["PATH"] += os.pathsep + ffmpeg_bin
# Lưu ý: Đảm bảo FaMIBaseScene đã được định nghĩa trước đó hoặc đổi thành Scene
class mainScene(ThreeDScene, FaMIBaseScene):
    def construct(self):
        title = self.create_title("TÍNH TOÁN SỐ BÀN THẮNG KỲ VỌNG TRONG BÓNG ĐÁ")

        # ==============================================================
        # PHÂN CẢNH 1: GIẢI PHÁP - Giới thiệu xG
        # ==============================================================
        with self.voiceover(
            text="Vậy thì tại sao lại như vậy? Bàn thắng kỳ vọng là gì? "
                 "Hãy cùng tìm hiểu thông qua video này!"
        ) as tracker:
            self.update_subtitle(
                "Vậy tại sao? Bàn thắng kỳ vọng là gì?\n"
                "Why? What is Expected Goals (xG)?"
            )
            self.play(Write(title), run_time=min(1.5, tracker.duration * 0.4))

            xg_query = Text("xG????", font_size=48, color=YELLOW, weight=BOLD)
            xg_query.move_to(ORIGIN)
            self.play(FadeIn(xg_query, scale=1.5), run_time=min(0.8, tracker.duration * 0.2))

        with self.voiceover(
            text="Hãy cùng tìm hiểu thông qua video này!"
        ) as tracker:
            self.update_subtitle(
                "Hãy cùng tìm hiểu!\nLet's find out together!"
            )
            self.play(
                xg_query.animate.next_to(title, DOWN, buff=0.4),
                run_time=min(1.0, tracker.duration * 0.6)
            )

        cat_gif_path = r"C:\Users\doman\Downloads\Project1-main\Roo-Code\assets\cat.mp4.gif"

        if os.path.exists(cat_gif_path):
            cat_meme = ImageMobject(cat_gif_path)
            cat_meme.scale_to_fit_width(7.5).move_to(ORIGIN + DOWN * 0.5)
            self.add_fixed_in_frame_mobjects(cat_meme)

            cat_top = cat_meme.get_top()
            q1 = Text("?", font_size=42, color=RED, weight=BOLD)
            q2 = Text("?", font_size=54, color=RED, weight=BOLD)
            q3 = Text("?", font_size=42, color=RED, weight=BOLD)
            q2.next_to(cat_top, UP, buff=0.4)
            q1.next_to(q2, LEFT, buff=0.5).shift(DOWN * 0.25)
            q3.next_to(q2, RIGHT, buff=0.5).shift(DOWN * 0.25)
            question_marks = VGroup(q1, q2, q3)

            edible_text = Text("Is it edible?", font_size=28, color=WHITE)
            edible_text.next_to(cat_meme.get_bottom(), DOWN, buff=0.3)

            with self.voiceover(
                text="Nghe có vẻ lạ... nhưng đừng lo, chúng ta sẽ giải mã nó ngay bây giờ!"
            ) as tracker:
                self.update_subtitle(
                    "Nghe lạ... nhưng đừng lo!\nSounds strange... but don't worry!"
                )
                self.play(FadeIn(cat_meme, shift=UP * 0.2), run_time=min(0.8, tracker.duration * 0.3))
                self.play(
                    LaggedStart(
                        FadeIn(q1, scale=0.5),
                        FadeIn(q2, scale=0.5),
                        FadeIn(q3, scale=0.5),
                        lag_ratio=0.15
                    ),
                    Write(edible_text),
                    run_time=min(1.2, tracker.duration * 0.5)
                )

            with self.voiceover(
                text="Chúng ta sẽ giải mã xG ngay bây giờ!"
            ) as tracker:
                self.update_subtitle(
                    "Chúng ta sẽ giải mã xG ngay!\nWe'll decode xG right now!"
                )
                self.play(
                    FadeOut(cat_meme),
                    FadeOut(xg_query),
                    FadeOut(question_marks),
                    FadeOut(edible_text),
                    run_time=min(0.8, tracker.duration * 0.6)
                )

        # ==============================================================
        # PHÂN CẢNH 2: THỰC HIỆN BÀI TOÁN
        # Subscene 2.1 - Mô phỏng 1000 cú sút
        # ==============================================================
        goal_width = 5.0
        goal_height = 2.5
        y_ground = 1.5

        post_bottom_left  = np.array([-goal_width/2, y_ground, 0])
        post_bottom_right = np.array([goal_width/2, y_ground, 0])
        goal_top_left     = np.array([-goal_width/2, y_ground + goal_height, 0])
        goal_top_right    = np.array([goal_width/2, y_ground + goal_height, 0])

        left_post  = Line(post_bottom_left, goal_top_left, color=WHITE, stroke_width=4)
        right_post = Line(post_bottom_right, goal_top_right, color=WHITE, stroke_width=4)
        crossbar   = Line(goal_top_left, goal_top_right, color=WHITE, stroke_width=4)
        ground_line = Line(np.array([-3.5, y_ground, 0]), np.array([3.5, y_ground, 0]), color=GRAY_D, stroke_width=2)
        complete_goal = VGroup(ground_line, left_post, right_post, crossbar)

        suppose_text = Text("A player takes 1000 shots", font_size=20, color=WHITE)
        suppose_text.next_to(crossbar, UP, buff=0.95)

        with self.voiceover(
            text="Giả sử có 10000 cú sút ở cùng một vị trí mang về 2700 bàn, "
                 "xác suất thực nghiệm là 0 phẩy 27."
        ) as tracker:
            self.update_subtitle(
                "10.000 cú sút → 2.700 bàn → P = 0.27\n"
                "10,000 shots → 2,700 goals → P = 0.27"
            )
            self.play(Create(complete_goal), Write(suppose_text), run_time=min(1.5, tracker.duration * 0.4))

            player_img_path = r"C:\Users\doman\Downloads\Project1-main\Roo-Code\assets\baycho.png"
            big_player = ImageMobject(player_img_path)
            big_player.set_width(2.5)
            big_player.move_to([0, -2.5, 0])
            self.play(FadeIn(big_player, shift=UP), run_time=min(0.8, tracker.duration * 0.2))

        with self.voiceover(
            text="Hãy xem cầu thủ này sút thử."
        ) as tracker:
            self.update_subtitle(
                "Xem cầu thủ sút thử!\nWatch the player shoot!"
            )
            ball_img_path = r"C:\Users\doman\Downloads\Project1-main\Roo-Code\assets\ball.png"
            shoot_targets = [
                np.array([-1.0, 2.5, 0]),
                np.array([1.5, 3.2, 0]),
                np.array([1.2, 2.0, 0]),
                np.array([-2.8, 1.8, 0]),
            ]
            for target in shoot_targets:
                ball = ImageMobject(ball_img_path)
                ball.set_width(0.3)
                ball.move_to(big_player.get_center() + UP * 0.5)
                self.play(FadeIn(ball, scale=0.5), run_time=0.15)
                self.play(ball.animate.move_to(target).scale(0.7), run_time=0.4, rate_func=linear)
                self.play(FadeOut(ball), run_time=0.1)

        num_dots = 200
        goal_ratio = 0.27
        num_goals = int(num_dots * goal_ratio)
        num_misses = num_dots - num_goals
        all_dots = VGroup()

        for _ in range(num_goals):
            dot = Dot(
                point=[random.uniform(-goal_width/2 + 0.1, goal_width/2 - 0.1),
                       random.uniform(y_ground + 0.1, y_ground + goal_height - 0.1), 0],
                color=GREEN, radius=0.06
            )
            all_dots.add(dot)

        for _ in range(num_misses):
            x_miss = random.choice([
                random.uniform(-3.5, -goal_width/2),
                random.uniform(goal_width/2, 3.5),
                random.uniform(-goal_width/2, goal_width/2)
            ])
            if x_miss >= -goal_width/2 and x_miss <= goal_width/2:
                y_miss = random.uniform(y_ground + goal_height + 0.1, 4.5)
            else:
                y_miss = random.uniform(y_ground, 4.2)
            dot = Dot(point=[x_miss, y_miss, 0], color=RED, radius=0.06)
            all_dots.add(dot)

        all_dots.submobjects = random.sample(all_dots.submobjects, len(all_dots.submobjects))

        ratio_text = MathTex(
            "P_{thuc \\ nghiem} = \\frac{2700}{10000} = 0.27",
            color=YELLOW
        ).scale(0.8)
        ratio_text.next_to(big_player, DOWN, buff=0.3)

        with self.voiceover(
            text="Kết quả thu được: xác suất thực nghiệm là 0 phẩy 27. "
                 "Các chấm xanh là bàn thắng, chấm đỏ là sút trượt."
        ) as tracker:
            self.update_subtitle(
                "Xanh = Bàn thắng | Đỏ = Sút trượt\n"
                "Green = Goal | Red = Miss"
            )
            self.play(
                LaggedStart(
                    *[FadeIn(d) for d in all_dots],
                    lag_ratio=0.008,
                    run_time=min(2.2, tracker.duration * 0.5)
                )
            )
            self.update_subtitle(
                "P_thực nghiệm = 2700/10000 = 0.27\n"
                "Empirical P = 2700/10000 = 0.27"
            )
            self.play(Write(ratio_text), run_time=min(1.0, tracker.duration * 0.25))

        # ==============================================================
        # Subscene 2.2 - Vector đặc trưng X
        # ==============================================================
        vector_x = MathTex(
            "X = \\begin{bmatrix} x_1 \\\\ x_2 \\\\ x_3 \\\\ \\vdots \\\\ x_n \\end{bmatrix}",
            color=BLUE
        ).scale(0.9).shift(LEFT * 1.5 + UP * 0.5)

        label_x1 = Text("x_1: Distance", font_size=18, color=WHITE)
        label_x2 = Text("x_2: Shot Angle", font_size=18, color=WHITE)
        label_x3 = Text("x_3: Shot Type", font_size=18, color=WHITE)
        label_dots = Text("...", font_size=18, color=WHITE)

        labels_group = VGroup(label_x1, label_x2, label_x3, label_dots).arrange(
            DOWN, aligned_edge=LEFT, buff=0.4
        ).next_to(vector_x, RIGHT, buff=0.4)

        arrows = VGroup(*[
            Arrow(
                start=vector_x.get_right(),
                end=np.array([1.5, -2.5, 0]) + LEFT * 1.2,
                buff=0.15, stroke_width=2, color=GRAY_A
            ) for _ in range(2)
        ])

        with self.voiceover(
            text="Nhưng trên sân cỏ, mọi pha bóng đều khác biệt! "
                 "Ta gom các yếu tố thành một vector đặc trưng X: "
                 "x1 khoảng cách, x2 loại cú sút, x3 góc sút, vân vân."
        ) as tracker:
            self.update_subtitle(
                "Mỗi pha bóng đều khác nhau!\n"
                "Every shot is different!"
            )
            self.play(
                FadeOut(complete_goal),
                FadeOut(suppose_text),
                FadeOut(all_dots),
                FadeOut(ratio_text),
                run_time=min(1.2, tracker.duration * 0.2)
            )
            self.play(
                big_player.animate.move_to([1.5, -2.5, 0]),
                run_time=min(1.2, tracker.duration * 0.2)
            )
            self.update_subtitle(
                "Vector đặc trưng X: x₁ khoảng cách, x₂ góc sút...\n"
                "Feature vector X: x₁ distance, x₂ angle..."
            )
            self.play(Write(vector_x), run_time=min(1.2, tracker.duration * 0.2))
            self.play(Write(label_x1), run_time=min(0.6, tracker.duration * 0.05))
            self.play(Write(label_x2), run_time=min(0.6, tracker.duration * 0.05))
            self.play(Write(label_x3), run_time=min(0.6, tracker.duration * 0.05))
            self.play(Write(label_dots), run_time=min(0.4, tracker.duration * 0.05))
            self.play(Create(arrows), run_time=min(1.2, tracker.duration * 0.15))

        # ==============================================================
        # Subscene 2.3 - Hình học: khoảng cách d và góc theta
        # ==============================================================
        goal_center_point = np.array([0, y_ground, 0])

        post_bottom_left  = np.array([-goal_width/2, y_ground, 0])
        post_bottom_right = np.array([goal_width/2, y_ground, 0])
        goal_top_left     = np.array([-goal_width/2, y_ground + goal_height, 0])
        goal_top_right    = np.array([goal_width/2, y_ground + goal_height, 0])

        left_post  = Line(post_bottom_left, goal_top_left, color=WHITE, stroke_width=4)
        right_post = Line(post_bottom_right, goal_top_right, color=WHITE, stroke_width=4)
        crossbar   = Line(goal_top_left, goal_top_right, color=WHITE, stroke_width=4)
        ground_line = Line(np.array([-3.5, y_ground, 0]), np.array([3.5, y_ground, 0]), color=WHITE, stroke_width=2)
        complete_goal = VGroup(ground_line, left_post, right_post, crossbar)

        with self.voiceover(
            text="Về hình học, ta dùng tọa độ tính khoảng cách d và góc nhìn khung thành theta. "
                 "Khoảng cách càng nhỏ, góc càng lớn thì xác suất ghi bàn càng cao."
        ) as tracker:
            self.update_subtitle(
                "d nhỏ + θ lớn → Xác suất cao hơn\n"
                "Smaller d + Larger θ → Higher probability"
            )
            self.play(
                FadeOut(vector_x),
                FadeOut(label_x1), FadeOut(label_x2), FadeOut(label_x3), FadeOut(label_dots),
                FadeOut(arrows),
                FadeOut(big_player),
                run_time=min(1.0, tracker.duration * 0.15)
            )
            self.play(Create(complete_goal), run_time=min(1.2, tracker.duration * 0.15))

            axes = Axes(
                x_range=[-3, 3, 1], y_range=[0, 5, 1],
                x_length=5.5, y_length=4.0,
                axis_config={"color": GRAY, "include_numbers": False}
            ).shift(UP * 1.5)

            self.update_subtitle(
                "Khoảng cách d được tính bằng công thức Euclid\n"
                "Distance d is calculated using Euclidean formula"
            )
            self.play(
                ReplacementTransform(complete_goal, axes.x_axis),
                Create(axes.y_axis),
                run_time=min(1.5, tracker.duration * 0.2)
            )

            pt_any = axes.c2p(1.5, 3.5, 0)
            pt_on_ox = axes.c2p(0.5, 0, 0)
            dot_p = Dot(pt_any, color=YELLOW, radius=0.08)
            lbl_p = MathTex("P(x, y)", font_size=20, color=YELLOW).next_to(pt_any, UR, buff=0.1)
            dist_line_axes = Line(pt_any, pt_on_ox, color=BLUE, stroke_width=3)
            lbl_d_axes = MathTex("d", color=BLUE).scale(0.8).next_to(dist_line_axes.get_center(), RIGHT, buff=0.1)
            formula_d = MathTex(
                "d = \\sqrt{(x_2-x_1)^2 + (y_2-y_1)^2}", color=YELLOW
            ).scale(0.8).next_to(axes, DOWN, buff=0.4)

            self.play(FadeIn(dot_p, lbl_p), run_time=min(0.5, tracker.duration * 0.05))
            self.play(Create(dist_line_axes), Write(lbl_d_axes), run_time=min(1.0, tracker.duration * 0.1))
            self.play(Write(formula_d), run_time=min(1.0, tracker.duration * 0.1))

        rebuild_goal = VGroup(
            Line(np.array([-3.5, y_ground, 0]), np.array([3.5, y_ground, 0]), color=WHITE, stroke_width=2),
            Line(post_bottom_left, goal_top_left, color=WHITE, stroke_width=4),
            Line(post_bottom_right, goal_top_right, color=WHITE, stroke_width=4),
            Line(goal_top_left, goal_top_right, color=WHITE, stroke_width=4)
        )

        with self.voiceover(
            text="Ta cũng tính góc nhìn theta giữa cầu thủ và hai cột dọc khung thành."
        ) as tracker:
            self.update_subtitle(
                "Góc θ: góc nhìn từ vị trí sút đến khung thành\n"
                "θ: the viewing angle from shot position to goal"
            )
            self.play(
                FadeOut(dot_p), FadeOut(lbl_p),
                FadeOut(dist_line_axes), FadeOut(lbl_d_axes),
                FadeOut(formula_d),
                FadeOut(axes.y_axis),
                ReplacementTransform(axes.x_axis, rebuild_goal),
                run_time=min(1.5, tracker.duration * 0.4)
            )

            onana_img_path = r"C:\Users\doman\Downloads\Project1-main\Roo-Code\assets\onana.png"
            onana = ImageMobject(onana_img_path)
            onana.set_width(1.5)
            onana.move_to([0, y_ground + 0.8, 0])

            player_img_path = r"C:\Users\doman\Downloads\Project1-main\Roo-Code\assets\baycho.png"
            player_kick = ImageMobject(player_img_path)
            player_kick.set_width(2.5)
            player_kick.move_to([0, -2.5, 0])

            ball_img_path = r"C:\Users\doman\Downloads\Project1-main\Roo-Code\assets\ball.png"
            ball = ImageMobject(ball_img_path)
            ball.set_width(0.3)
            ball.move_to(player_kick.get_center() + UP * 0.5 + RIGHT * 0.2)

            self.play(
                FadeIn(onana, shift=DOWN),
                FadeIn(player_kick, shift=UP),
                FadeIn(ball),
                run_time=min(1.2, tracker.duration * 0.3)
            )

        with self.voiceover(
            text="Nhìn xem, góc sút theta được biểu diễn bằng cung tròn xanh lá."
        ) as tracker:
            self.update_subtitle(
                "Cung xanh = Góc sút θ\nGreen arc = Shooting angle θ"
            )
            shot_target = np.array([goal_width/2 - 0.4, y_ground + 0.6, 0])
            self.play(
                ball.animate.move_to(shot_target).scale(0.8),
                onana.animate.shift(RIGHT * 0.6 + DOWN * 0.2),
                run_time=min(0.5, tracker.duration * 0.2)
            )

            real_line_d = Line(player_kick.get_center(), goal_center_point, color=BLUE, stroke_width=3)
            real_lbl_d = MathTex("d", color=BLUE).scale(0.9).next_to(real_line_d.get_center(), LEFT, buff=0.15)
            self.play(Create(real_line_d), Write(real_lbl_d), run_time=min(1.0, tracker.duration * 0.3))

            p_center = player_kick.get_center()
            ray_to_right_post = Line(p_center, post_bottom_right, color=GRAY_B, stroke_width=2)
            ray_to_left_post  = Line(p_center, post_bottom_left, color=GRAY_B, stroke_width=2)
            theta_arc = ArcBetweenPoints(
                start=p_center + 0.6 * normalize(post_bottom_right - p_center),
                end=p_center + 0.6 * normalize(post_bottom_left - p_center),
                stroke_width=2.5, color=GREEN
            )
            real_lbl_theta = MathTex("\\theta", color=GREEN).scale(0.9).next_to(theta_arc, UP, buff=0.1)

            self.play(Create(ray_to_right_post), Create(ray_to_left_post), run_time=min(0.8, tracker.duration * 0.2))
            self.play(Create(theta_arc), Write(real_lbl_theta), run_time=min(0.8, tracker.duration * 0.2))

        # ==============================================================
        # Subscene 2.4 - Logistic Regression
        # ==============================================================
        with self.voiceover(
            text="Kết quả mà ta mong muốn là 0 hoặc 1, "
                 "vì vậy ta phải dùng Hồi quy Logistic thay vì tuyến tính."
        ) as tracker:
            self.update_subtitle(
                "Output: 0 (No Goal) hoặc 1 (Goal)\n"
                "Output: 0 (No Goal) or 1 (Goal)"
            )
            self.play(
                FadeOut(rebuild_goal),
                FadeOut(onana),
                FadeOut(player_kick),
                FadeOut(ball),
                FadeOut(real_line_d), FadeOut(real_lbl_d),
                FadeOut(ray_to_right_post), FadeOut(ray_to_left_post),
                FadeOut(theta_arc), FadeOut(real_lbl_theta),
                run_time=min(1.0, tracker.duration * 0.2)
            )

            output_title = Text("Target output:", font_size=36, color=YELLOW).move_to([0, 2.5, 0])
            goal_text = Text("1: GOAL", font_size=30, color=GREEN).move_to([0, 1.3, 0])
            nogoal_text = Text("0: NO GOAL", font_size=30, color=RED).move_to([0, 0.3, 0])

            self.update_subtitle(
                "1 = Ghi bàn | 0 = Không ghi bàn\n"
                "1 = Goal | 0 = No Goal"
            )
            self.play(Write(output_title), run_time=min(0.8, tracker.duration * 0.2))
            self.play(FadeIn(goal_text, shift=UP), run_time=min(0.8, tracker.duration * 0.2))
            self.play(FadeIn(nogoal_text, shift=UP), run_time=min(0.8, tracker.duration * 0.2))

        output_group = VGroup(output_title, goal_text, nogoal_text)

        with self.voiceover(
            text="Hồi quy tuyến tính không phù hợp vì kết quả có thể vượt quá 0 và 1. "
                 "Ta cần Logistic Regression!"
        ) as tracker:
            self.update_subtitle(
                "Hồi quy tuyến tính → Sai! Dùng Logistic!\n"
                "Linear Regression → Wrong! Use Logistic!"
            )
            self.play(FadeOut(output_group), run_time=min(0.8, tracker.duration * 0.15))

            linear_text = Text("Linear Regression", font_size=36, color=WHITE).move_to([0, 1.5, 0])
            linear_cross = Line(
                start=linear_text.get_corner(DL) + LEFT * 0.1,
                end=linear_text.get_corner(UR) + RIGHT * 0.1,
                color=RED, stroke_width=4
            )
            self.play(Write(linear_text), run_time=min(1.0, tracker.duration * 0.2))
            self.play(Create(linear_cross), run_time=min(0.6, tracker.duration * 0.15))

            angry_meme_path = r"C:\Users\doman\Downloads\Project1-main\Roo-Code\assets\angry.png"
            angry_meme = ImageMobject(angry_meme_path)
            angry_meme.set_width(5.0)
            angry_meme.move_to([0, -1.5, 0])
            self.play(FadeIn(angry_meme, scale=0.8), run_time=min(0.8, tracker.duration * 0.2))

        with self.voiceover(
            text="Logistic Regression mới là lựa chọn đúng đắn!"
        ) as tracker:
            self.update_subtitle(
                "Logistic Regression ✓\nLogistic Regression ✓"
            )
            self.play(
                FadeOut(linear_text), FadeOut(linear_cross), FadeOut(angry_meme),
                run_time=min(0.8, tracker.duration * 0.3)
            )

            logistic_text = Text("Logistic Regression", font_size=36, color=GREEN).move_to([0, 1.5, 0])
            thumbsup_meme_path = r"C:\Users\doman\Downloads\Project1-main\Roo-Code\assets\pngwing.com.png"
            thumbsup_meme = ImageMobject(thumbsup_meme_path)
            thumbsup_meme.set_width(5.0)
            thumbsup_meme.move_to([0, -1.5, 0])

            self.play(Write(logistic_text), run_time=min(1.0, tracker.duration * 0.3))
            self.play(FadeIn(thumbsup_meme, shift=UP), run_time=min(0.8, tracker.duration * 0.3))

        with self.voiceover(
            text="Ta cùng tìm hiểu công thức, đầu tiên là giá trị tuyến tính z."
        ) as tracker:
            self.update_subtitle(
                "Bước 1: Phần tuyến tính z\nStep 1: Linear part z"
            )
            self.play(
                FadeOut(thumbsup_meme, shift=DOWN),
                logistic_text.animate.next_to(title, DOWN, buff=0.3).scale(0.8),
                run_time=min(1.0, tracker.duration * 0.4)
            )

            step1_title = Text("1. Linear part", font_size=28, color=YELLOW)
            step1_title.move_to(ORIGIN)
            self.play(Write(step1_title), run_time=min(1.0, tracker.duration * 0.3))
            self.play(step1_title.animate.next_to(logistic_text, DOWN, buff=0.4), run_time=min(0.8, tracker.duration * 0.2))

        with self.voiceover(
            text="z bằng b0 cộng b1 x1 cộng b2 x2 cộng các hệ số khác. "
                 "Mỗi x là một yếu tố: khoảng cách, góc sút, loại cú sút."
        ) as tracker:
            self.update_subtitle(
                "z = b₀ + b₁x₁ + b₂x₂ + ... + bₙxₙ\n"
                "z = b₀ + b₁x₁ + b₂x₂ + ... + bₙxₙ"
            )
            z_formula = MathTex(
                "z", "=", "b_0", "+", "b_1x_1", "+", "b_2x_2", "+", "b_3x_3", "+", "\\cdots", "+", "b_nx_n",
                font_size=42, color=YELLOW
            )
            z_formula.next_to(step1_title, DOWN, buff=0.4)
            self.play(FadeIn(z_formula, shift=UP), run_time=min(1.0, tracker.duration * 0.3))

            factor_x1 = MathTex("x_1:", "\\text{ Distance}", font_size=32, color=GRAY_A)
            factor_x1.next_to(z_formula, DOWN, buff=0.4, aligned_edge=LEFT).shift(RIGHT * 0.5)
            factor_x2 = MathTex("x_2:", "\\text{ Shot angle}", font_size=32, color=GRAY_A)
            factor_x2.next_to(factor_x1, DOWN, buff=0.25, aligned_edge=LEFT)
            factor_x3 = MathTex("x_3:", "\\text{ Shot type}", font_size=32, color=GRAY_A)
            factor_x3.next_to(factor_x2, DOWN, buff=0.25, aligned_edge=LEFT)
            factor_dots = MathTex("\\dots", font_size=32, color=GRAY_A)
            factor_dots.next_to(factor_x3, DOWN, buff=0.2, aligned_edge=LEFT).shift(RIGHT * 0.2)

            self.update_subtitle(
                "x₁: Khoảng cách | x₂: Góc sút | x₃: Loại cú sút\n"
                "x₁: Distance | x₂: Shot Angle | x₃: Shot Type"
            )
            self.play(
                FadeIn(factor_x1, shift=RIGHT),
                FadeIn(factor_x2, shift=RIGHT),
                FadeIn(factor_x3, shift=RIGHT),
                FadeIn(factor_dots, shift=RIGHT),
                run_time=min(1.2, tracker.duration * 0.4)
            )

        with self.voiceover(
            text="Ta đưa z vào hàm mũ để chuẩn bị cho bước tiếp theo."
        ) as tracker:
            self.update_subtitle(
                "Bước 2: Hàm mũ e^(-z)\nStep 2: Exponential e^(-z)"
            )
            self.play(
                FadeOut(factor_x1), FadeOut(factor_x2), FadeOut(factor_x3), FadeOut(factor_dots),
                run_time=min(0.6, tracker.duration * 0.3)
            )

            step2_title = Text("2. Non-linear exponential", font_size=28, color=BLUE)
            step2_title.move_to(ORIGIN)
            self.play(Write(step2_title), run_time=min(1.0, tracker.duration * 0.3))
            self.play(step2_title.animate.next_to(z_formula, DOWN, buff=0.5), run_time=min(0.8, tracker.duration * 0.3))

            exp_part = MathTex("e^{-", "z", "}", font_size=52, color=BLUE)
            exp_part.next_to(step2_title, DOWN, buff=0.4)
            self.play(
                ReplacementTransform(z_formula[0].copy(), exp_part[1]),
                Write(exp_part[0]), Write(exp_part[2]),
                run_time=min(1.2, tracker.duration * 0.3)
            )

        with self.voiceover(
            text="Ta đưa z vào hàm sigmoid để ép kết quả về khoảng từ 0 đến 1, "
                 "đó chính là xác suất ghi bàn."
        ) as tracker:
            self.update_subtitle(
                "Bước 3: Nén về xác suất (0, 1)\nStep 3: Probability compression (0, 1)"
            )
            step3_title = Text("3. Probability compression", font_size=28, color=GREEN)
            step3_title.move_to(DOWN * 2.0)
            self.play(Write(step3_title), run_time=min(1.0, tracker.duration * 0.3))
            self.play(step3_title.animate.next_to(exp_part, DOWN, buff=0.5), run_time=min(0.8, tracker.duration * 0.3))

        with self.voiceover(
            text="Có đủ công cụ rồi! Đây là công thức Logistic Regression hoàn chỉnh: "
                 "P bằng 1 chia cho 1 cộng e mũ trừ z."
        ) as tracker:
            self.update_subtitle(
                "P(y=1) = 1 / (1 + e^{-z})\n"
                "P(y=1) = 1 / (1 + e^{-z})"
            )
            self.play(
                FadeOut(step1_title), FadeOut(step2_title), FadeOut(step3_title),
                run_time=min(0.8, tracker.duration * 0.15)
            )
            self.play(z_formula.animate.shift(UP * 0.5), run_time=min(0.5, tracker.duration * 0.1))

            p_formula = MathTex(
                "P(y=1)", "=", "{ 1", "\\over", "1 + ", "e^{-z}", "}",
                font_size=54
            ).move_to(DOWN * 0.5)
            p_formula.set_color_by_tex("e^{-z}", BLUE)
            p_formula.set_color_by_tex("P(y=1)", GREEN)

            self.play(
                ReplacementTransform(exp_part, p_formula[5]),
                Write(p_formula[0:2]),
                Write(p_formula[4]),
                Write(p_formula[2]),
                Create(p_formula[3]),
                run_time=min(2.0, tracker.duration * 0.5)
            )

            final_box = SurroundingRectangle(p_formula, color=GREEN, buff=0.3, stroke_width=3)
            self.play(Create(final_box), run_time=min(0.8, tracker.duration * 0.15))

        # ==============================================================
        # Subscene 2.5 - Đồ thị Sigmoid 2D
        # ==============================================================
        with self.voiceover(
            text="Hãy thử minh họa đồ thị hồi quy logistics bằng hình ảnh. "
                 "Trục tung là kết quả ghi bàn, trục hoành là khoảng cách. "
                 "Đồ thị có hình dạng sigmoid đi xuống."
        ) as tracker:
            self.update_subtitle(
                "Trục Y: Goal/No Goal | Trục X: Khoảng cách\n"
                "Y-axis: Goal/No Goal | X-axis: Distance"
            )
            self.play(
                FadeOut(p_formula), FadeOut(final_box), FadeOut(z_formula),
                run_time=min(0.8, tracker.duration * 0.15)
            )

            axes = Axes(
                x_range=[0, 7, 1], y_range=[-0.1, 1.2, 0.5],
                x_length=5.8, y_length=6.0,
                axis_config={"color": GRAY, "include_ticks": True},
                tips=False
            ).shift(DOWN * 0.3)

            x_label = Text("Distance", font_size=20, color=WHITE).next_to(axes.x_axis.get_end(), DOWN, buff=0.2).shift(LEFT * 0.5)
            y_label = Text("Result", font_size=20, color=WHITE).next_to(axes.y_axis, UP, buff=0.2)
            lbl_y1 = MathTex("1 \\text{ (Goal)}", font_size=20, color=GREEN).next_to(axes.c2p(0, 1, 0), LEFT, buff=0.15)
            lbl_y0 = MathTex("0 \\text{ (No Goal)}", font_size=20, color=RED).next_to(axes.c2p(0, 0, 0), LEFT, buff=0.15)

            self.play(
                Create(axes),
                Write(x_label), Write(y_label),
                Write(lbl_y1), Write(lbl_y0),
                run_time=min(1.2, tracker.duration * 0.2)
            )

            y1_line = DashedLine(start=axes.c2p(0, 1, 0), end=axes.c2p(6.5, 1, 0), color=GREEN_B, stroke_width=2)
            self.play(Create(y1_line), run_time=min(0.8, tracker.duration * 0.1))

            goals_coords   = [(0.8,1),(2.6,1),(0.3,1),(1.5,1),(5.0,1),(0.6,1),(3.5,1),(1.1,1),(2.0,1)]
            nogoals_coords = [(4.2,0),(0.8,0),(5.8,0),(2.8,0),(4.8,0),(1.8,0),(6.2,0),(3.6,0),(5.3,0)]

            goal_dots   = VGroup(*[Dot(axes.c2p(x, y, 0), color=GREEN,  radius=0.08) for x, y in goals_coords])
            nogoal_dots = VGroup(*[Dot(axes.c2p(x, y, 0), color=RED,    radius=0.08) for x, y in nogoals_coords])

            self.update_subtitle(
                "Gần gôn → Nhiều bàn hơn\nClose to goal → More goals"
            )
            self.play(
                LaggedStart(*[FadeIn(dot, scale=0.3) for dot in goal_dots],   lag_ratio=0.25),
                LaggedStart(*[FadeIn(dot, scale=0.3) for dot in nogoal_dots], lag_ratio=0.25),
                run_time=min(3.0, tracker.duration * 0.4)
            )

        with self.voiceover(
            text="Đường sigmoid khớp dần với dữ liệu, cho thấy khoảng cách càng gần thì xác suất càng cao."
        ) as tracker:
            self.update_subtitle(
                "Đường Sigmoid khớp với dữ liệu\nSigmoid curve fits the data"
            )
            k_tracker  = ValueTracker(-2.5)
            x0_tracker = ValueTracker(1.0)

            sigmoid_curve = always_redraw(lambda: axes.plot(
                lambda x: 1 / (1 + np.exp(k_tracker.get_value() * (x - x0_tracker.get_value()))),
                x_range=[0, 6.2], color=YELLOW, stroke_width=4
            ))

            self.play(Create(sigmoid_curve), run_time=min(1.0, tracker.duration * 0.15))
            self.play(k_tracker.animate.set_value(3.0), x0_tracker.animate.set_value(5.0),
                      run_time=min(1.2, tracker.duration * 0.2), rate_func=linear)
            self.play(k_tracker.animate.set_value(0.5), x0_tracker.animate.set_value(1.5),
                      run_time=min(1.0, tracker.duration * 0.15), rate_func=linear)
            self.play(k_tracker.animate.set_value(1.5), x0_tracker.animate.set_value(3.0),
                      run_time=min(1.5, tracker.duration * 0.2), rate_func=smooth)

            all_coords = goals_coords + nogoals_coords
            projection_lines = VGroup()
            for x, y in all_coords:
                start_pt  = axes.c2p(x, y, 0)
                y_sigmoid = 1 / (1 + np.exp(1.5 * (x - 3.0)))
                end_pt    = axes.c2p(x, y_sigmoid, 0)
                line = DashedLine(start=start_pt, end=end_pt, color=YELLOW_A, stroke_width=1.5)
                projection_lines.add(line)

            self.update_subtitle(
                "Đường dứt nét: sai số giữa thực tế và mô hình\n"
                "Dashed lines: error between actual and model"
            )
            self.play(Create(projection_lines), run_time=min(1.8, tracker.duration * 0.3))

        # ==============================================================
        # Subscene 2.6 - Không gian 3D
        # ==============================================================
        with self.voiceover(
            text="Giờ ta thêm yếu tố góc sút vào, ta sẽ thu được một mặt cong trong không gian ba chiều. "
                 "Góc sút càng rộng thì tỉ lệ thành bàn sẽ càng cao hơn."
        ) as tracker:
            self.update_subtitle(
                "Thêm góc sút → Mặt cong 3D\nAdd shot angle → 3D curved surface"
            )
            self.play(
                FadeOut(projection_lines), FadeOut(sigmoid_curve),
                FadeOut(y1_line),
                FadeOut(x_label), FadeOut(y_label),
                FadeOut(lbl_y1), FadeOut(lbl_y0),
                FadeOut(goal_dots), FadeOut(nogoal_dots),
                FadeOut(axes),
                run_time=min(0.8, tracker.duration * 0.1)
            )

            self.add_fixed_in_frame_mobjects(title, logistic_text)
            self.move_camera(phi=70 * DEGREES, theta=-60 * DEGREES, run_time=min(1.5, tracker.duration * 0.2))

            axes_3d = ThreeDAxes(
                x_range=[0, 7, 1], y_range=[0, 90, 15], z_range=[0, 1.2, 0.5],
                x_length=4.0, y_length=4.0, z_length=3.0,
                axis_config={"color": GRAY, "stroke_width": 2,
                             "include_numbers": False, "include_ticks": False}
            ).move_to(ORIGIN + DOWN * 0.5)

            x_lbl_3d = Text("Distance (X)", font_size=14, color=WHITE)
            y_lbl_3d = Text("Shot Angle (Y)", font_size=14, color=WHITE)
            z_lbl_3d = Text("Result (Z)", font_size=14, color=WHITE)
            x_lbl_3d.next_to(axes_3d.x_axis.get_end(), RIGHT, buff=0.15)
            y_lbl_3d.next_to(axes_3d.y_axis.get_end(), OUT + UP, buff=0.1)
            z_lbl_3d.next_to(axes_3d.z_axis.get_end(), UP, buff=0.1)

            self.play(Create(axes_3d), Write(x_lbl_3d), Write(y_lbl_3d), Write(z_lbl_3d),
                      run_time=min(1.5, tracker.duration * 0.2))

            prediction_surface = Surface(
                lambda u, v: axes_3d.c2p(
                    u, v, 1 / (1 + np.exp(1.5 * (u - 3.0) - 0.05 * (v - 45)))
                ),
                u_range=[0, 6.5], v_range=[0, 90], resolution=(20, 20),
            )
            prediction_surface.set_style(
                fill_opacity=0.35, fill_color=BLUE_C,
                stroke_color=TEAL_D, stroke_width=0.6
            )

            goals_3d   = [(0.8,75,1),(2.6,45,1),(0.3,80,1),(1.5,60,1),(5.0,30,1)]
            nogoals_3d = [(4.2,15,0),(0.8,25,0),(5.8,10,0),(2.8,35,0),(4.8,15,0)]

            goal_dots_3d = VGroup(*[
                Dot3D(point=axes_3d.c2p(x, y, z), color=GREEN, radius=0.09)
                for x, y, z in goals_3d
            ])
            nogoal_dots_3d = VGroup(*[
                Dot3D(point=axes_3d.c2p(x, y, z), color=RED, radius=0.09)
                for x, y, z in nogoals_3d
            ])

            self.update_subtitle(
                "Mặt cong Sigmoid 3D: khoảng cách + góc sút\n"
                "3D Sigmoid surface: distance + shot angle"
            )
            self.play(Create(prediction_surface), run_time=min(2.0, tracker.duration * 0.25))
            self.play(FadeIn(goal_dots_3d), FadeIn(nogoal_dots_3d), run_time=min(1.0, tracker.duration * 0.1))

        with self.voiceover(
            text="Ta xoay camera để quan sát mặt cong từ nhiều góc độ khác nhau."
        ) as tracker:
            self.update_subtitle(
                "Quan sát mặt cong từ nhiều góc\nViewing the surface from multiple angles"
            )
            self.add_fixed_in_frame_mobjects(self.logo)
            self.move_camera(phi=55*DEGREES, theta=20*DEGREES, run_time=min(2.5, tracker.duration*0.3), rate_func=smooth)
            self.move_camera(phi=25*DEGREES, theta=20*DEGREES, run_time=min(2.5, tracker.duration*0.3), rate_func=smooth)
            self.move_camera(phi=75*DEGREES, theta=80*DEGREES, run_time=min(2.5, tracker.duration*0.25), rate_func=smooth)
            self.move_camera(phi=70*DEGREES, theta=-60*DEGREES, run_time=min(2.5, tracker.duration*0.1), rate_func=smooth)

        # ==============================================================
        # Subscene 2.7 - Chiến thuật HLV
        # ==============================================================
        with self.voiceover(
            text="Đó là lí do ngày nay, các đội bóng được dẫn dắt bởi Pep hay Enrique "
                 "thường cố gắng đưa quả bóng tới gần gôn hết mức có thể rồi mới kết liễu."
        ) as tracker:
            self.update_subtitle(
                "Tránh sút xa! Đưa bóng gần gôn rồi mới dứt điểm\n"
                "Avoid long shots! Get the ball close before finishing"
            )
            self.play(
                FadeOut(axes_3d),
                FadeOut(x_lbl_3d), FadeOut(y_lbl_3d), FadeOut(z_lbl_3d),
                FadeOut(prediction_surface),
                FadeOut(goal_dots_3d), FadeOut(nogoal_dots_3d),
                FadeOut(logistic_text),
                run_time=min(1.0, tracker.duration * 0.15)
            )
            self.move_camera(phi=0*DEGREES, theta=-90*DEGREES, run_time=0.1)

            strategy_text = Text("Avoid long shots as much as possible", font_size=36, color=YELLOW)
            strategy_text.next_to(title, DOWN, buff=0.4)
            self.play(Write(strategy_text), run_time=min(1.2, tracker.duration * 0.2))

            pep_path = r"C:\Users\doman\Downloads\Project1-main\Roo-Code\assets\pep.png"
            if os.path.exists(pep_path):
                pep_img = ImageMobject(pep_path).scale_to_fit_width(6.0).move_to(UP * 0.2)
                self.update_subtitle(
                    "Pep Guardiola: Tiki-taka → Gần gôn → Dứt điểm\n"
                    "Pep Guardiola: Tiki-taka → Close range → Finish"
                )
                self.play(FadeIn(pep_img, shift=UP * 0.3), run_time=min(1.0, tracker.duration * 0.2))

        with self.voiceover(
            text="Luis Enrique cũng áp dụng triết lý tương tự với đội tuyển Pháp."
        ) as tracker:
            self.update_subtitle(
                "Luis Enrique: Triết lý kiểm soát bóng & xâm nhập vòng cấm\n"
                "Luis Enrique: Ball control & penalty box invasion philosophy"
            )
            enrique_path = r"C:\Users\doman\Downloads\Project1-main\Roo-Code\assets\enrique.png"
            if os.path.exists(pep_path):
                self.play(FadeOut(pep_img, shift=DOWN * 0.3), run_time=min(0.8, tracker.duration * 0.2))
            if os.path.exists(enrique_path):
                enrique_img = ImageMobject(enrique_path).scale_to_fit_width(3.5).move_to(UP * 0.2)
                self.play(FadeIn(enrique_img, shift=UP * 0.3), run_time=min(1.0, tracker.duration * 0.3))

        # ==============================================================
        # Subscene 2.8 - Các yếu tố không thể đo lường & Phương pháp khác
        # ==============================================================
        with self.voiceover(
            text="Trên thực tế, mô hình không bao giờ chính xác 100% "
                 "vì có những biến số không thể đo lường như tâm lý cầu thủ hay độ xoáy của cỏ."
        ) as tracker:
            self.update_subtitle(
                "Mô hình không hoàn hảo: tâm lý, điều kiện sân...\n"
                "Model isn't perfect: psychology, pitch conditions..."
            )
            self.play(FadeOut(strategy_text), run_time=min(0.5, tracker.duration * 0.1))
            if os.path.exists(enrique_path):
                self.play(FadeOut(enrique_img), run_time=min(0.5, tracker.duration * 0.1))

            reason_txt = Text("Some reasons may affect the xG", font_size=28, color=YELLOW_B)
            reason_txt.next_to(title, DOWN, buff=0.4)
            self.play(Write(reason_txt), run_time=min(1.0, tracker.duration * 0.2))

            messi_path = r"C:\Users\doman\Downloads\Project1-main\Roo-Code\assets\messi.png"
            if os.path.exists(messi_path):
                messi_img = ImageMobject(messi_path).scale_to_fit_width(5.0).move_to(UP * 0.3)
                self.add_fixed_in_frame_mobjects(messi_img)
                messi_txt = Text("Bro sent the ball to the universe", font_size=20, color=GRAY_A)
                messi_txt.next_to(messi_img, DOWN, buff=0.3)
                self.update_subtitle(
                    "Messi: Sút ra ngoài vũ trụ 🌌\nMessi: Sent the ball to the universe 🌌"
                )
                self.play(FadeIn(messi_img, shift=UP * 0.2), Write(messi_txt), run_time=min(1.0, tracker.duration * 0.2))

        with self.voiceover(
            text="Còn Ronaldo thì... trượt chân."
        ) as tracker:
            self.update_subtitle(
                "Ronaldo: Trượt chân 😅\nRonaldo: Bro slipped 😅"
            )
            if os.path.exists(messi_path):
                self.play(FadeOut(messi_img), FadeOut(messi_txt), run_time=min(0.6, tracker.duration * 0.3))

            ronaldo_path = r"C:\Users\doman\Downloads\Project1-main\Roo-Code\assets\crbuoi-Photoroom.png"
            if os.path.exists(ronaldo_path):
                ronaldo_img = ImageMobject(ronaldo_path).scale_to_fit_width(5.0).move_to(UP * 0.3)
                self.add_fixed_in_frame_mobjects(ronaldo_img)
                ronaldo_txt = Text("Bro slipped", font_size=18, color=GRAY_A)
                ronaldo_txt.next_to(ronaldo_img, DOWN, buff=0.3)
                self.play(FadeIn(ronaldo_img, shift=UP * 0.2), Write(ronaldo_txt), run_time=min(1.0, tracker.duration * 0.4))

        with self.voiceover(
            text="Nên để xử lý số lượng biến khổng lồ, các phân tích viên sẽ dùng các công cụ "
                 "như phương pháp phân tích thành phần chính, hay bản đồ nhiệt, vân vân."
        ) as tracker:
            self.update_subtitle(
                "Công cụ xử lý: PCA, Heatmap...\n"
                "Analysis tools: PCA, Heatmap..."
            )
            if os.path.exists(ronaldo_path):
                self.play(FadeOut(ronaldo_img), FadeOut(ronaldo_txt), FadeOut(reason_txt),
                          run_time=min(0.8, tracker.duration * 0.1))

            other_methods_title = Text("Other methods", font_size=32, color=BLUE_B, weight=BOLD)
            other_methods_title.next_to(title, DOWN, buff=0.4)
            pca_title = Text("1. Principal Component Analysis (PCA)", font_size=24, color=WHITE)
            pca_title.next_to(other_methods_title, DOWN, buff=0.3)

            self.play(Write(other_methods_title), run_time=min(0.8, tracker.duration * 0.1))
            self.play(Write(pca_title), run_time=min(0.8, tracker.duration * 0.1))

            pca_img_path = r"C:\Users\doman\Downloads\Project1-main\Roo-Code\assets\1QinDfRawRskupf4mU5bYSA.webp"
            if os.path.exists(pca_img_path):
                pca_img = ImageMobject(pca_img_path).scale_to_fit_width(6.0).next_to(pca_title, DOWN, buff=0.4)
                self.add_fixed_in_frame_mobjects(pca_img)
                self.update_subtitle(
                    "PCA: Giảm chiều dữ liệu\nPCA: Dimensionality reduction"
                )
                self.play(FadeIn(pca_img, shift=UP * 0.2), run_time=min(1.0, tracker.duration * 0.15))
                self.play(FadeOut(pca_img), run_time=min(0.6, tracker.duration * 0.1))

            heatmap_title = Text("2. Heatmap", font_size=24, color=WHITE)
            heatmap_title.next_to(pca_title, DOWN, buff=0.3)
            self.play(Write(heatmap_title), run_time=min(0.8, tracker.duration * 0.1))

            # Heatmap construction
            heatmap_pitch_group = VGroup()
            pitch_border  = Rectangle(width=6.0, height=5.5, stroke_color=GRAY, stroke_width=1.5)
            penalty_box   = Rectangle(width=4.0, height=2.2, stroke_color=GRAY, stroke_width=1.2)
            penalty_box.align_to(pitch_border, UP)
            goal_post     = Rectangle(width=1.0, height=0.25, stroke_color=GRAY, stroke_width=1.2)
            goal_post.next_to(pitch_border, UP, buff=0)
            penalty_arc   = Arc(radius=0.7, start_angle=0*DEGREES, angle=-180*DEGREES,
                                stroke_color=GRAY, stroke_width=1.2)
            penalty_arc.move_to(penalty_box.get_bottom() + DOWN * 0.02)
            pitch_lines   = VGroup(pitch_border, penalty_box, goal_post, penalty_arc)

            DARK_BROWN = "#1C1410"
            MED_BROWN  = "#402414"
            ORANGE_HOT = "#C87424"

            heatmap_data = [
                [("1%",DARK_BROWN),("5%",MED_BROWN), ("3%",MED_BROWN), ("1%",DARK_BROWN)],
                [("4%",MED_BROWN), ("9%",ORANGE_HOT),("14%",ORANGE_HOT),("3%",MED_BROWN)],
                [("5%",MED_BROWN), ("7%",ORANGE_HOT),("11%",ORANGE_HOT),("3%",MED_BROWN)],
                [("6%",MED_BROWN), ("4%",MED_BROWN), ("6%",MED_BROWN), ("4%",MED_BROWN)],
                [("1%",DARK_BROWN),("4%",DARK_BROWN),("3%",DARK_BROWN),("2%",DARK_BROWN)],
                [("1%",DARK_BROWN),("1%",DARK_BROWN),("2%",DARK_BROWN),("1%",DARK_BROWN)],
            ]
            heatmap_grid = VGroup()
            box_width, box_height = 1.45, 0.72
            for r_idx, row in enumerate(heatmap_data):
                for c_idx, (pct_str, bg_color) in enumerate(row):
                    box = Rectangle(
                        width=box_width, height=box_height,
                        fill_color=bg_color, fill_opacity=0.80,
                        stroke_color=GRAY, stroke_width=0.4
                    )
                    box.move_to(RIGHT*(c_idx-1.5)*box_width + DOWN*(r_idx-1.0)*box_height)
                    text = Text(pct_str, font="Courier New", font_size=16, color=WHITE)
                    text.move_to(box.get_center())
                    heatmap_grid.add(VGroup(box, text))

            heatmap_grid.move_to(pitch_border.get_center() + UP * 0.5)
            heatmap_pitch_group.add(pitch_lines, heatmap_grid)
            heatmap_pitch_group.next_to(heatmap_title, DOWN, buff=0.6)
            self.add_fixed_in_frame_mobjects(heatmap_pitch_group)

            self.update_subtitle(
                "Heatmap: Vùng nóng trong vòng cấm địa (%)\n"
                "Heatmap: Hot zones inside the penalty area (%)"
            )
            self.play(FadeIn(heatmap_pitch_group, shift=UP * 0.3), run_time=min(1.5, tracker.duration * 0.2))
            self.play(FadeOut(heatmap_pitch_group), run_time=min(0.8, tracker.duration * 0.1))

            etc_text = Text("etc.", font_size=24, color=WHITE, font="Segoe UI", slant=ITALIC)
            etc_text.next_to(heatmap_title, DOWN, buff=0.4)
            self.play(FadeIn(etc_text, shift=DOWN * 0.1), run_time=min(0.5, tracker.duration * 0.05))

        with self.voiceover(
            text="Và còn nhiều phương pháp khác nữa!"
        ) as tracker:
            self.update_subtitle(
                "Và còn nhiều phương pháp khác...\nAnd many more methods..."
            )
            self.play(
                FadeOut(other_methods_title), FadeOut(pca_title),
                FadeOut(heatmap_title), FadeOut(etc_text),
                run_time=min(0.8, tracker.duration * 0.5)
            )

        # ==============================================================
        # PHÂN CẢNH 3: TỔNG KẾT KIẾN THỨC
        # Subscene 3.1 - Ý nghĩa thống kê: Overperforming
        # ==============================================================
        with self.voiceover(
            text="Ta có thể thấy ý nghĩa thống kê của xG rất rõ ràng: "
                 "Nếu cầu thủ ghi 25 bàn nhưng xG chỉ 18, anh ta có kỹ năng dứt điểm tốt hơn trung bình."
        ) as tracker:
            self.update_subtitle(
                "25 Bàn vs xG 18 → Dứt điểm xuất sắc!\n"
                "25 Goals vs xG 18 → Elite finishing!"
            )
            sig_subtitle = Text("Statistical Significance: Goals vs xG", font_size=28, color=BLUE)
            sig_subtitle.next_to(title, DOWN, buff=0.3)
            self.add_fixed_in_frame_mobjects(sig_subtitle)
            self.play(FadeIn(sig_subtitle, shift=UP * 0.2), run_time=min(0.8, tracker.duration * 0.1))

            chart_data  = {"Goals": 25, "xG": 18}
            bar_colors  = [BLUE_C, RED_C]
            finishing_chart = BarChart(
                values=[chart_data["Goals"], chart_data["xG"]],
                bar_names=["Goals", "xG"],
                y_range=[0, 30, 5], y_length=4.5, x_length=6.0,
                axis_config={"include_numbers": True}, bar_colors=bar_colors,
            ).scale_to_fit_width(6.5).move_to(DOWN * 0.8)

            goals_label = DecimalNumber(chart_data["Goals"], num_decimal_places=0, color=WHITE, font_size=24)
            xg_label    = DecimalNumber(chart_data["xG"],    num_decimal_places=0, color=WHITE, font_size=24)
            goals_label.next_to(finishing_chart.bars[0], UP, buff=0.2)
            xg_label.next_to(finishing_chart.bars[1],    UP, buff=0.2)
            chart_labels = VGroup(goals_label, xg_label)

            self.play(
                FadeIn(finishing_chart.axes),
                GrowFromEdge(finishing_chart.bars, DOWN),
                FadeIn(chart_labels, shift=UP * 0.2),
                run_time=min(2.0, tracker.duration * 0.3)
            )

            diff_line = DashedLine(goals_label.get_center(), xg_label.get_center(), color=YELLOW_C, stroke_width=2)
            diff_text = Text("+7 Goals", font_size=20, color=YELLOW_C)
            diff_text.next_to(diff_line, DOWN, buff=0.1)
            diff_visual = VGroup(diff_line, diff_text)
            self.update_subtitle(
                "+7 Bàn vượt kỳ vọng → Overperforming!\n"
                "+7 Goals above expectation → Overperforming!"
            )
            self.play(Create(diff_line), FadeIn(diff_text), run_time=min(1.0, tracker.duration * 0.15))

        # Subscene 3.2 - Underperforming
        with self.voiceover(
            text="Ngược lại, nếu ghi ít hơn xG thì cầu thủ đang kém may mắn hoặc dứt điểm kém."
        ) as tracker:
            self.update_subtitle(
                "Goals < xG → Kém may mắn hoặc dứt điểm kém\n"
                "Goals < xG → Bad luck or poor finishing"
            )
            self.play(FadeOut(diff_visual), run_time=min(0.5, tracker.duration * 0.15))

            new_goals_val, new_xg_val = 12, 18
            self.play(
                finishing_chart.animate.change_bar_values([new_goals_val, new_xg_val]),
                FadeOut(chart_labels),
                run_time=min(2.0, tracker.duration * 0.35), rate_func=linear
            )

            goals_label_new = DecimalNumber(new_goals_val, num_decimal_places=0, color=WHITE, font_size=24)
            xg_label_new    = DecimalNumber(new_xg_val,    num_decimal_places=0, color=WHITE, font_size=24)
            goals_label_new.next_to(finishing_chart.bars[0], UP, buff=0.2)
            xg_label_new.next_to(finishing_chart.bars[1],    UP, buff=0.2)
            chart_labels_new = VGroup(goals_label_new, xg_label_new)
            self.play(FadeIn(chart_labels_new, shift=UP * 0.1), run_time=min(0.5, tracker.duration * 0.1))

            diff_line_new = DashedLine(goals_label_new.get_center(), xg_label_new.get_center(), color=RED_A, stroke_width=2)
            diff_text_new = Text("-6 Goals", font_size=20, color=RED_A)
            diff_text_new.next_to(diff_line_new, UP, buff=0.1)
            diff_visual_new = VGroup(diff_line_new, diff_text_new)
            self.add_fixed_in_frame_mobjects(diff_visual_new)

            self.update_subtitle(
                "-6 Bàn dưới kỳ vọng → Underperforming!\n"
                "-6 Goals below expectation → Underperforming!"
            )
            self.play(Create(diff_line_new), FadeIn(diff_text_new, scale=0.8), run_time=min(0.8, tracker.duration * 0.15))

        # Subscene 3.3 - Hạn chế: Khác biệt mô hình AI
        with self.voiceover(
            text="Tất nhiên xG cũng có hạn chế vì chưa đo được hoàn toàn áp lực tâm lý "
                 "và mỗi hãng như Opta hay StatsBomb lại có một model riêng."
        ) as tracker:
            self.update_subtitle(
                "Hạn chế: Mỗi hãng có model xG khác nhau\n"
                "Limit: Each provider has a different xG model"
            )
            self.play(
                FadeOut(sig_subtitle), FadeOut(finishing_chart),
                FadeOut(chart_labels_new), FadeOut(diff_visual_new),
                run_time=min(0.8, tracker.duration * 0.1)
            )

            model_subtitle = Text("Limit: Difference in AI Models", font_size=28, color=GREEN)
            model_subtitle.next_to(title, DOWN, buff=0.3)
            self.add_fixed_in_frame_mobjects(model_subtitle)
            self.play(FadeIn(model_subtitle, shift=UP * 0.2), run_time=min(0.8, tracker.duration * 0.1))

            opta_label    = Text("Opta Model", font_size=24, color=BLUE_B)
            opta_box      = RoundedRectangle(corner_radius=0.3, width=3.5, height=1.0, color=BLUE_B, stroke_width=2)
            opta_group    = VGroup(opta_box, opta_label).move_to(LEFT * 2.2 + DOWN * 1.0)

            statsbomb_label = Text("StatsBomb Model", font_size=22, color=ORANGE)
            statsbomb_box   = RoundedRectangle(corner_radius=0.3, width=3.5, height=1.0, color=ORANGE, stroke_width=2)
            statsbomb_group = VGroup(statsbomb_box, statsbomb_label).move_to(RIGHT * 2.2 + DOWN * 1.0)

            opta_val  = Text("xG: 0.23", font_size=22, color=WHITE).next_to(opta_box,      DOWN, buff=0.3)
            stats_val = Text("xG: 0.19", font_size=22, color=WHITE).next_to(statsbomb_box, DOWN, buff=0.3)

            comparison_group = VGroup(opta_group, statsbomb_group, opta_val, stats_val)
            comparison_group.scale_to_fit_width(6.8)

            self.update_subtitle(
                "Opta: xG = 0.23 | StatsBomb: xG = 0.19\n"
                "Opta: xG = 0.23 | StatsBomb: xG = 0.19"
            )
            self.play(FadeIn(opta_group, shift=RIGHT * 0.2), Write(opta_val), run_time=min(1.0, tracker.duration * 0.2))
            self.play(FadeIn(statsbomb_group, shift=LEFT * 0.2), Write(stats_val), run_time=min(1.0, tracker.duration * 0.2))

        with self.voiceover(
            text="Cùng một pha bóng, hai mô hình cho ra kết quả khác nhau. "
                 "Đó là sự tương đối của dữ liệu trong bóng đá hiện đại."
        ) as tracker:
            self.update_subtitle(
                "Cùng 1 cú sút → 2 giá trị xG khác nhau!\n"
                "Same shot → 2 different xG values!"
            )
            self.play(
                FadeOut(model_subtitle),
                FadeOut(comparison_group),
                FadeOut(title),
                run_time=min(1.0, tracker.duration * 0.5)
            )


######################
scene = mainScene()
scene.render()
video_file = Path(config.media_dir) / "videos" / "1280p15" / "mainScene.mp4"
if video_file.exists():
    display(Video(str(video_file), embed=True, width=300))
else:
    found = list(Path(config.media_dir).glob("**/mainScene.mp4"))
    if found:
        display(Video(str(found[0]), embed=True, width=300))
    else:
        print("Render xong nhưng không tìm thấy file mp4 để hiển thị.")
