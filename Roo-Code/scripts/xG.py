from manim_voiceover.services.gtts import GTTSService
from manim import *
from manim_voiceover import VoiceoverScene
from pathlib import Path
import random
import os
from datetime import datetime

# Cấu hình rendering
config.pixel_height = 1280
config.pixel_width = 720
config.frame_rate = 15
config.quality = "low_quality"
config.media_dir = "./videos"

# Định nghĩa màu tùy chỉnh
ACCENT = "#1f77b4"
FAMI_BLUE = "#0066cc"
FAMI_CYAN = "#00ccff"
FAMI_SUB = "#ffaa00"

PROJECT_ROOT = Path(__file__).parent.parent.parent
ASSETS_DIR = PROJECT_ROOT / "Roo-Code" / "assets"

def normalize(vec):
    """Chuẩn hóa vector"""
    norm = np.linalg.norm(vec)
    return vec / norm if norm > 0 else vec

class FaMIBaseScene(VoiceoverScene, ThreeDScene):
    """Scene cơ bản cho video"""
    def setup(self):
        super().setup()
        self.logo = None
    
    def create_title(self, text):
        """Tạo tiêu đề"""
        return Title(text)
    
    def update_subtitle(self, text):
        """Placeholder for subtitle update - manim-voiceover handles this automatically"""
        pass

class mainScene(FaMIBaseScene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_speech_service(GTTSService())

    def construct(self):
        title = self.create_title("EXPECTED GOALS (xG) IN FOOTBALL")
        
        # PHÂN CẢNH: Giải pháp 
        # Tạo dòng chữ thắc mắc "xG????"
        xg_query = Text("xG????", font_size=48, color=YELLOW, weight=BOLD)
        xg_query.move_to(ORIGIN) 

        with self.voiceover(text="Why is it so? What are expected goals? Let us explore together through this video!") as tracker:
            # Hiệu ứng hiện chữ tại tâm màn hình
            self.play(Write(title), run_time=min(1.2, tracker.duration * 0.25))
            self.play(FadeIn(xg_query, scale=1.5), run_time=min(0.8, tracker.duration * 0.2))

            # Hiệu ứng trượt lên trên (Slide Up) bám dưới title
            self.play(
                xg_query.animate.next_to(title, DOWN, buff=0.4),
                run_time=min(1.0, tracker.duration * 0.25),
                rate_func=smooth 
            )

        # Chèn trực tiếp file ảnh GIF gốc vào hệ thống
        cat_gif_path = r"C:\Users\doman\Downloads\Project1-main\Roo-Code\assets\cat.mp4.gif"

        if os.path.exists(cat_gif_path):
            # Sử dụng ImageMobject để đọc file gif dưới dạng ảnh tĩnh
            cat_meme = ImageMobject(cat_gif_path)
            
            # Cân chỉnh kích thước và vị trí trung tâm phía dưới dòng chữ
            cat_meme.scale_to_fit_width(7.5).move_to(ORIGIN + DOWN * 0.5)
            
            # QUAN TRỌNG TRONG 3DSCENE: Khóa cứng ảnh vào màn hình phẳng overlay
            self.add_fixed_in_frame_mobjects(cat_meme)

            with self.voiceover(text="This is the question that many football fans ask themselves.") as tracker:
                self.update_subtitle("Đây là câu hỏi mà nhiều fan bóng đá tự hỏi mình.\n(This is the question that many football fans ask themselves.)")
                # Xuất hiện chú mèo mượt mà từ dưới lên một chút
                self.play(FadeIn(cat_meme, shift=UP * 0.2), run_time=min(0.8, tracker.duration * 0.3))
                
                # Tạo 3 dấu hỏi màu đỏ độc lập
                q1 = Text("?", font_size=42, color=RED, weight=BOLD)
                q2 = Text("?", font_size=54, color=RED, weight=BOLD)
                q3 = Text("?", font_size=42, color=RED, weight=BOLD)
                
                # Xếp chúng thành hình vòng cung trên đỉnh đầu của cat_meme
                cat_top = cat_meme.get_top()
                
                q2.next_to(cat_top, UP, buff=0.4)
                q1.next_to(q2, LEFT, buff=0.5).shift(DOWN * 0.25)
                q3.next_to(q2, RIGHT, buff=0.5).shift(DOWN * 0.25)
                
                # Gom 3 dấu hỏi thành nhóm
                question_marks = VGroup(q1, q2, q3)
                
                # Tạo dòng chữ "Is it edible?" nằm ngay dưới meme con mèo
                edible_text = Text("Is it edible?", font_size=28, color=WHITE)
                edible_text.next_to(cat_meme.get_bottom(), DOWN, buff=0.3)
                
                # Chạy hiệu ứng xuất hiện
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

            # Kết thúc: Xóa sạch toàn bộ các object cùng một lúc
            self.play(
                FadeOut(cat_meme),
                FadeOut(xg_query),
                FadeOut(question_marks),
                FadeOut(edible_text),
                run_time=0.8
            )

        # PHÂN CẢNH: Thực hiện bài toán
        # Subscene 1: Mô phỏng 1000 cú sút của cầu thủ
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

        with self.voiceover(text="Suppose a player takes 10,000 shots from the same position, resulting in 2,700 goals. The empirical probability is 0.27.") as tracker:
            self.update_subtitle("Giả sử có 10000 cú sút ở cùng một vị trí mang về 2700 bàn, xác suất thực nghiệm là 0,27.\n(Suppose a player takes 10,000 shots from the same position, resulting in 2,700 goals. The empirical probability is 0.27.)")
            self.play(Create(complete_goal), Write(suppose_text), run_time=min(1.5, tracker.duration * 0.3))

            player_img_path = r"C:\Users\doman\Downloads\Project1-main\Roo-Code\assets\baycho.png"
            big_player = ImageMobject(player_img_path)
            big_player.set_width(2.5) 
            big_player.move_to([0, -2.5, 0]) 
            
            self.play(FadeIn(big_player, shift=UP), run_time=min(0.8, tracker.duration * 0.2))

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
                self.play(
                    ball.animate.move_to(target).scale(0.7), 
                    run_time=0.4, 
                    rate_func=linear
                )
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

        with self.voiceover(text="But on the field, every football play is different. We combine various factors into feature vectors.") as tracker:
            self.update_subtitle("Nhưng trên sân cỏ, mọi pha bóng đều khác biệt! Ta gom các yếu tố thành một vector đặc trưng X.\n(But on the field, every football play is different. We combine various factors into feature vectors.)")
            self.play(
                LaggedStart(
                    *[FadeIn(d) for d in all_dots],
                    lag_ratio=0.008,
                    run_time=min(2.2, tracker.duration * 0.6)
                )
            )

        ratio_text = MathTex(
            "P_{empirical} = \\frac{2700}{10000} = 0.27", 
            color=YELLOW
        ).scale(0.8)
        ratio_text.next_to(big_player, DOWN, buff=0.3)
        
        with self.voiceover(text="For example, x1 represents distance, x2 represents shot type, x3 represents shooting angle, and so on.") as tracker:
            self.update_subtitle("Ví dụ: x1: khoảng cách, x2: loại cú sút, x3: góc sút, vân vân.\n(For example, x1 represents distance, x2 represents shot type, x3 represents shooting angle, and so on.)")
            self.play(Write(ratio_text), run_time=min(1.5, tracker.duration * 0.3))

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
                buff=0.15, 
                stroke_width=2, 
                color=GRAY_A
            ) for _ in range(2)
        ])

        self.play(
            FadeOut(complete_goal),
            FadeOut(suppose_text),
            FadeOut(all_dots),
            FadeOut(ratio_text),
            run_time=1.2
        )

        with self.voiceover(text="In geometry, we calculate distance d and viewing angle theta to the goal.") as tracker:
            self.update_subtitle("Về hình học, ta dùng tọa độ tính khoảng cách d và góc nhìn khung thành theta.\n(In geometry, we calculate distance d and viewing angle theta to the goal.)")
            self.play(
                big_player.animate.move_to([1.5, -2.5, 0]),
                run_time=min(1.2, tracker.duration * 0.3),
                rate_func=smooth
            )
            self.play(
                Write(vector_x),
                run_time=min(1.2, tracker.duration * 0.3)
            )
            self.play(Write(label_x1), run_time=min(0.6, tracker.duration * 0.15))
            self.play(Write(label_x2), run_time=min(0.6, tracker.duration * 0.15))
            self.play(Write(label_x3), run_time=min(0.6, tracker.duration * 0.15))
            self.play(Write(label_dots), run_time=min(0.4, tracker.duration * 0.1))
            self.play(
                Create(arrows),
                run_time=min(1.2, tracker.duration * 0.2)
            )

        # Subscene 2: Chuyển đổi từ mô phỏng sút bóng sang biểu diễn hình học thực địa
        self.play(
            FadeOut(vector_x),
            FadeOut(label_x1), FadeOut(label_x2), FadeOut(label_x3), FadeOut(label_dots),
            FadeOut(arrows),
            FadeOut(big_player),
            run_time=1
        )

        goal_width = 5.0
        goal_height = 2.5
        y_ground = 1.5 

        post_bottom_left  = np.array([-goal_width/2, y_ground, 0])
        post_bottom_right = np.array([goal_width/2, y_ground, 0])
        goal_top_left     = np.array([-goal_width/2, y_ground + goal_height, 0])
        goal_top_right    = np.array([goal_width/2, y_ground + goal_height, 0])
        goal_center_point = np.array([0, y_ground, 0])

        left_post  = Line(post_bottom_left, goal_top_left, color=WHITE, stroke_width=4)
        right_post = Line(post_bottom_right, goal_top_right, color=WHITE, stroke_width=4)
        crossbar   = Line(goal_top_left, goal_top_right, color=WHITE, stroke_width=4)
        ground_line = Line(np.array([-3.5, y_ground, 0]), np.array([3.5, y_ground, 0]), color=WHITE, stroke_width=2)
        
        complete_goal = VGroup(ground_line, left_post, right_post, crossbar)

        with self.voiceover(text="The closer the distance and the wider the angle, the higher the probability of scoring.") as tracker:
            self.update_subtitle("Khoảng cách càng nhỏ, góc càng lớn thì xác suất ghi bàn càng cao.\n(The closer the distance and the wider the angle, the higher the probability of scoring.)")
            self.play(Create(complete_goal), run_time=min(1.2, tracker.duration * 0.3))

        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[0, 5, 1],
            x_length=5.5,
            y_length=4.0,
            axis_config={"color": GRAY, "include_numbers": False}
        ).shift(UP * 1.5)

        with self.voiceover(text="We need logistic regression instead of linear regression for binary output.") as tracker:
            self.update_subtitle("Kết quả mà ta mong muốn là 0 hoặc 1, ta phải dùng Hồi quy Logistic thay vì tuyến tính.\n(We need logistic regression instead of linear regression for binary output.)")
            self.play(
                ReplacementTransform(complete_goal, axes.x_axis),
                Create(axes.y_axis),
                run_time=min(1.5, tracker.duration * 0.4)
            )

        pt_any = axes.c2p(1.5, 3.5, 0)
        pt_on_ox = axes.c2p(0.5, 0, 0)

        dot_p = Dot(pt_any, color=YELLOW, radius=0.08)
        lbl_p = MathTex("P(x, y)", font_size=20, color=YELLOW).next_to(pt_any, UR, buff=0.1)
        
        dist_line_axes = Line(pt_any, pt_on_ox, color=BLUE, stroke_width=3)
        lbl_d_axes = MathTex("d", color=BLUE).scale(0.8).next_to(dist_line_axes.get_center(), RIGHT, buff=0.1)

        self.play(FadeIn(dot_p, lbl_p), run_time=0.5)
        self.play(Create(dist_line_axes), Write(lbl_d_axes), run_time=1)

        formula_d = MathTex(
            "d = \\sqrt{(x_2-x_1)^2 + (y_2-y_1)^2}",
            color=YELLOW
        ).scale(0.8).next_to(axes, DOWN, buff=0.4)

        with self.voiceover(text="Let us understand the formula displayed on the screen. First, the linear value z.") as tracker:
            self.update_subtitle("Ta cùng tìm hiểu công thức hiển thị trên màn hình. Đầu tiên là giá trị tuyến tính z.\n(Let us understand the formula displayed on the screen. First, the linear value z.)")
            self.play(Write(formula_d), run_time=min(1.5, tracker.duration * 0.4))

        rebuild_goal = VGroup(
            Line(np.array([-3.5, y_ground, 0]), np.array([3.5, y_ground, 0]), color=WHITE, stroke_width=2),
            Line(post_bottom_left, goal_top_left, color=WHITE, stroke_width=4),
            Line(post_bottom_right, goal_top_right, color=WHITE, stroke_width=4),
            Line(goal_top_left, goal_top_right, color=WHITE, stroke_width=4)
        )

        self.play(
            FadeOut(dot_p), FadeOut(lbl_p),
            FadeOut(dist_line_axes), FadeOut(lbl_d_axes),
            FadeOut(formula_d),
            FadeOut(axes.y_axis),
            ReplacementTransform(axes.x_axis, rebuild_goal),
            run_time=1.5
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

        with self.voiceover(text="When the shot distance is closer and the angle is wider, the scoring probability increases.") as tracker:
            self.update_subtitle("Khoảng cách cầu sút gần hơn và góc sút rộng hơn, xác suất ghi bàn tăng lên.\n(When the shot distance is closer and the angle is wider, the scoring probability increases.)")
            self.play(
                FadeIn(onana, shift=DOWN),
                FadeIn(player_kick, shift=UP),
                FadeIn(ball),
                run_time=min(1.2, tracker.duration * 0.3)
            )

        shot_target = np.array([goal_width/2 - 0.4, y_ground + 0.6, 0]) 

        with self.voiceover(text="The ball flies into the goal, and the goalkeeper tries to save but misses.") as tracker:
            self.update_subtitle("Quả bóng bay vào lưới, thủ môn cố gắng cứu nhưng hụt.\n(The ball flies into the goal, and the goalkeeper tries to save but misses.)")
            self.play(
                ball.animate.move_to(shot_target).scale(0.8),
                onana.animate.shift(RIGHT * 0.6 + DOWN * 0.2), 
                run_time=min(0.5, tracker.duration * 0.25),
                rate_func=linear
            )

        real_line_d = Line(player_kick.get_center(), goal_center_point, color=BLUE, stroke_width=3)
        real_lbl_d = MathTex("d", color=BLUE).scale(0.9).next_to(real_line_d.get_center(), LEFT, buff=0.15)

        self.play(Create(real_line_d), Write(real_lbl_d), run_time=1)

        p_center = player_kick.get_center()
        
        ray_to_right_post = Line(p_center, post_bottom_right, color=GRAY_B, stroke_width=2)
        ray_to_left_post = Line(p_center, post_bottom_left, color=GRAY_B, stroke_width=2)

        theta_arc = ArcBetweenPoints(
            start=p_center + 0.6 * normalize(post_bottom_right - p_center),
            end=p_center + 0.6 * normalize(post_bottom_left - p_center),
            stroke_width=2.5,
            color=GREEN
        )
        
        real_lbl_theta = MathTex("\\theta", color=GREEN).scale(0.9).next_to(theta_arc, UP, buff=0.1)

        with self.voiceover(text="We connect the shooting position to both goal posts and measure the angle theta between them.") as tracker:
            self.update_subtitle("Ta nối từ vị trí sút tới cả hai cột dọc và đo góc theta giữa chúng.\n(We connect the shooting position to both goal posts and measure the angle theta between them.)")
            self.play(
                Create(ray_to_right_post),
                Create(ray_to_left_post),
                run_time=min(0.8, tracker.duration * 0.3)
            )
            
            self.play(
                Create(theta_arc),
                Write(real_lbl_theta),
                run_time=min(0.8, tracker.duration * 0.3)
            )

        # Subscene 3: Chuyển đổi từ biểu diễn hình học thực địa sang mô hình hồi quy logistic
        self.play(
            FadeOut(rebuild_goal),
            FadeOut(onana),
            FadeOut(player_kick),
            FadeOut(ball),
            FadeOut(real_line_d), FadeOut(real_lbl_d),
            FadeOut(ray_to_right_post), FadeOut(ray_to_left_post),
            FadeOut(theta_arc), FadeOut(real_lbl_theta),
            run_time=1
        )

        output_title = Text("Target output:", font_size=36, color=YELLOW).move_to([0, 2.5, 0])
        goal_text = Text("1: GOAL", font_size=30, color=GREEN).move_to([0, 1.3, 0])
        nogoal_text = Text("0: NO GOAL", font_size=30, color=RED).move_to([0, 0.3, 0])
        
        output_group = VGroup(output_title, goal_text, nogoal_text)

        with self.voiceover(text="Our goal is to predict binary output: 1 for goal, 0 for no goal.") as tracker:
            self.update_subtitle("Mục tiêu của chúng ta là dự đoán đầu ra nhị phân: 1 cho ghi bàn, 0 cho không ghi bàn.\n(Our goal is to predict binary output: 1 for goal, 0 for no goal.)")
            self.play(Write(output_title), run_time=min(0.8, tracker.duration * 0.25))
            
            self.play(FadeIn(goal_text, shift=UP), run_time=min(0.8, tracker.duration * 0.25))
            
            self.play(FadeIn(nogoal_text, shift=UP), run_time=min(0.8, tracker.duration * 0.25))

        self.play(FadeOut(output_group), run_time=0.8)

        linear_text = Text("Linear Regression", font_size=36, color=WHITE).move_to([0, 1.5, 0])
        
        linear_cross = Line(
            start=linear_text.get_corner(DL) + LEFT * 0.1, 
            end=linear_text.get_corner(UR) + RIGHT * 0.1, 
            color=RED, 
            stroke_width=4
        )

        with self.voiceover(text="But linear regression produces values outside the 0-1 range, which is invalid for probability.") as tracker:
            self.update_subtitle("Nhưng hồi quy tuyến tính tạo ra các giá trị ngoài khoảng 0-1, không hợp lệ cho xác suất.\n(But linear regression produces values outside the 0-1 range, which is invalid for probability.)")
            self.play(Write(linear_text), run_time=min(1, tracker.duration * 0.3))
            self.play(Create(linear_cross), run_time=min(0.6, tracker.duration * 0.2))

        angry_meme_path = r"C:\Users\doman\Downloads\Project1-main\Roo-Code\assets\angry.png"
        angry_meme = ImageMobject(angry_meme_path)
        angry_meme.set_width(5.0)
        angry_meme.move_to([0, -1.5, 0])

        self.play(FadeIn(angry_meme, scale=0.8), run_time=0.8)

        self.play(
            FadeOut(linear_text),
            FadeOut(linear_cross),
            FadeOut(angry_meme),
            run_time=0.8
        )

        logistic_text = Text("Logistic Regression", font_size=36, color=GREEN).move_to([0, 1.5, 0])
        
        thumbsup_meme_path = r"C:\Users\doman\Downloads\Project1-main\Roo-Code\assets\pngwing.com.png"
        thumbsup_meme = ImageMobject(thumbsup_meme_path)
        thumbsup_meme.set_width(5.0)
        thumbsup_meme.move_to([0, -1.5, 0])

        with self.voiceover(text="We use logistic regression which maps all values into the 0-1 range through the sigmoid function.") as tracker:
            self.update_subtitle("Chúng ta sử dụng hồi quy logistic, hàm sigmoid ánh xạ tất cả giá trị vào khoảng 0-1.\n(We use logistic regression which maps all values into the 0-1 range through the sigmoid function.)")
            self.play(Write(logistic_text), run_time=min(1, tracker.duration * 0.3))
            self.play(FadeIn(thumbsup_meme, shift=UP), run_time=min(0.8, tracker.duration * 0.25))

        self.play(
            FadeOut(thumbsup_meme, shift=DOWN),
            logistic_text.animate.next_to(title, DOWN, buff=0.3).scale(0.8),
            run_time=1
        )

        step1_title = Text("1. Linear part", font_size=28, color=YELLOW)
        step1_title.move_to(ORIGIN)
        
        with self.voiceover(text="Let us understand the three-step process.") as tracker:
            self.update_subtitle("Hãy hiểu quy trình ba bước.\n(Let us understand the three-step process.)")
            self.play(Write(step1_title), run_time=min(1, tracker.duration * 0.3))

        self.play(step1_title.animate.next_to(logistic_text, DOWN, buff=0.4), run_time=0.8)

        z_formula = MathTex("z", "=", "b_0", "+", "b_1x_1", "+", "b_2x_2", "+", "b_3x_3","+", "\\cdots","+", "b_nx_n", font_size=42, color=YELLOW)
        z_formula.next_to(step1_title, DOWN, buff=0.4)

        with self.voiceover(text="The linear combination of features weighted by coefficients.") as tracker:
            self.update_subtitle("Tổ hợp tuyến tính của các đặc trưng được tính trọng số bằng các hệ số.\n(The linear combination of features weighted by coefficients.)")
            self.play(FadeIn(z_formula, shift=UP), run_time=min(1, tracker.duration * 0.3))

        factor_x1 = MathTex("x_1:", "\\text{ Distance}", font_size=32, color=GRAY_A)
        factor_x1.next_to(z_formula, DOWN, buff=0.4, aligned_edge=LEFT).shift(RIGHT * 0.5)
        factor_x2 = MathTex("x_2:", "\\text{ Shot angle}", font_size=32, color=GRAY_A)
        factor_x2.next_to(factor_x1, DOWN, buff=0.25, aligned_edge=LEFT)
        factor_x3 = MathTex("x_3:", "\\text{ Shot type}", font_size=32, color=GRAY_A)
        factor_x3.next_to(factor_x2, DOWN, buff=0.25, aligned_edge=LEFT)
        factor_dots = MathTex("\\dots", font_size=32, color=GRAY_A)
        factor_dots.next_to(factor_x3, DOWN, buff=0.2, aligned_edge=LEFT).shift(RIGHT * 0.2)

        with self.voiceover(text="Where x1 is distance, x2 is shot angle, x3 is shot type, and so on.") as tracker:
            self.update_subtitle("Trong đó x1 là khoảng cách, x2 là góc sút, x3 là loại cú sút, v.v...\n(Where x1 is distance, x2 is shot angle, x3 is shot type, and so on.)")
            self.play(
                FadeIn(factor_x1, shift=RIGHT),
                FadeIn(factor_x2, shift=RIGHT),
                FadeIn(factor_x3, shift=RIGHT),
                FadeIn(factor_dots, shift=RIGHT),
                run_time=min(1.2, tracker.duration * 0.4)
            )

        self.play(
            FadeOut(factor_x1), FadeOut(factor_x2), FadeOut(factor_x3), FadeOut(factor_dots),
            run_time=0.6
        )

        step2_title = Text("2. Non-linear exponential", font_size=28, color=BLUE)
        step2_title.move_to(ORIGIN)
        
        with self.voiceover(text="Next, we apply the sigmoid function using exponential transformation.") as tracker:
            self.update_subtitle("Tiếp theo, ta áp dụng hàm sigmoid bằng phép biến đổi hàm mũ.\n(Next, we apply the sigmoid function using exponential transformation.)")
            self.play(Write(step2_title), run_time=min(1, tracker.duration * 0.3))

        self.play(step2_title.animate.next_to(z_formula, DOWN, buff=0.5), run_time=0.8)

        exp_part = MathTex("e^{-", "z", "}", font_size=52, color=BLUE)
        exp_part.next_to(step2_title, DOWN, buff=0.4)

        self.play(
            ReplacementTransform(z_formula[0].copy(), exp_part[1]),
            Write(exp_part[0]), Write(exp_part[2]),
            run_time=min(1.2, tracker.duration * 0.3)
        )
        
        step3_title = Text("3. Probability compression", font_size=28, color=GREEN)
        step3_title.move_to(DOWN * 2.0)
        
        with self.voiceover(text="Finally, we compress the exponential into a probability between 0 and 1 using the sigmoid formula.") as tracker:
            self.update_subtitle("Cuối cùng, ta nén hàm mũ thành xác suất từ 0 đến 1 bằng công thức sigmoid.\n(Finally, we compress the exponential into a probability between 0 and 1 using the sigmoid formula.)")
            self.play(Write(step3_title), run_time=min(1, tracker.duration * 0.3))

        self.play(step3_title.animate.next_to(exp_part, DOWN, buff=0.5), run_time=0.8)

        self.play(
            FadeOut(step1_title),
            FadeOut(step2_title),
            FadeOut(step3_title),
            run_time=0.8
        )

        self.play(z_formula.animate.shift(UP * 0.5), run_time=0.5)

        p_formula = MathTex(
            "P(y=1)", "=", "{ 1", "\\over", "1 + ", "e^{-z}", "}",
            font_size=54
        ).move_to(DOWN * 0.5)
        p_formula.set_color_by_tex("e^{-z}", BLUE)
        p_formula.set_color_by_tex("P(y=1)", GREEN)

        with self.voiceover(text="The logistic regression formula gives us probability between 0 and 1.") as tracker:
            self.update_subtitle("Công thức hồi quy logistic cho ta xác suất giữa 0 và 1.\n(The logistic regression formula gives us probability between 0 and 1.)")
            self.play(
                ReplacementTransform(exp_part, p_formula[5]),
                Write(p_formula[0:2]),
                Write(p_formula[4]),
                Write(p_formula[2]),
                Create(p_formula[3]),
                run_time=min(2, tracker.duration * 0.4)
            )

        final_box = SurroundingRectangle(p_formula, color=GREEN, buff=0.3, stroke_width=3)
        self.play(Create(final_box), run_time=0.8)

        # Subscene 4: Biểu diễn trực quan phân phối xác suất
        self.play(
            FadeOut(p_formula),
            FadeOut(final_box),
            FadeOut(z_formula),
            run_time=0.8
        )

        axes = Axes(
            x_range=[0, 7, 1],
            y_range=[-0.1, 1.2, 0.5],
            x_length=5.8,
            y_length=6.0,
            axis_config={"color": GRAY, "include_ticks": True},
            tips=False
        ).shift(DOWN * 0.3)

        x_label = Text("Distance", font_size=20, color=WHITE).next_to(axes.x_axis.get_end(), DOWN, buff=0.2).shift(LEFT * 0.5)
        y_label = Text("Result", font_size=20, color=WHITE).next_to(axes.y_axis, UP, buff=0.2)
        
        lbl_y1 = MathTex("1 \\text{ (Goal)}", font_size=20, color=GREEN).next_to(axes.c2p(0, 1, 0), LEFT, buff=0.15)
        lbl_y0 = MathTex("0 \\text{ (No Goal)}", font_size=20, color=RED).next_to(axes.c2p(0, 0, 0), LEFT, buff=0.15)

        with self.voiceover(text="Plotting the sigmoid curve on a 2D coordinate system shows how goal probability changes with distance.") as tracker:
            self.update_subtitle("Vẽ đường cong sigmoid trên hệ tọa độ 2D cho thấy xác suất ghi bàn thay đổi theo khoảng cách.\n(Plotting the sigmoid curve on a 2D coordinate system shows how goal probability changes with distance.)")
            self.play(
                Create(axes),
                Write(x_label), Write(y_label),
                Write(lbl_y1), Write(lbl_y0),
                run_time=min(1.2, tracker.duration * 0.3)
            )

        y1_line = DashedLine(start=axes.c2p(0, 1, 0), end=axes.c2p(6.5, 1, 0), color=GREEN_B, stroke_width=2)
        self.play(Create(y1_line), run_time=0.8)

        goals_coords = [(0.8, 1), (2.6, 1), (0.3, 1), (1.5, 1), (5.0, 1), (0.6, 1), (3.5, 1), (1.1, 1), (2.0, 1)]
        nogoals_coords = [(4.2, 0), (0.8, 0), (5.8, 0), (2.8, 0), (4.8, 0), (1.8, 0), (6.2, 0), (3.6, 0), (5.3, 0)]

        goal_dots = VGroup(*[Dot(axes.c2p(x, y, 0), color=GREEN, radius=0.08) for x, y in goals_coords])
        nogoal_dots = VGroup(*[Dot(axes.c2p(x, y, 0), color=RED, radius=0.08) for x, y in nogoals_coords])

        self.play(
            LaggedStart(*[FadeIn(dot, scale=0.3) for dot in goal_dots], lag_ratio=0.25),
            LaggedStart(*[FadeIn(dot, scale=0.3) for dot in nogoal_dots], lag_ratio=0.25),
            run_time=3.0
        )

        k_tracker = ValueTracker(-2.5)
        x0_tracker = ValueTracker(1.0)

        sigmoid_curve = always_redraw(lambda: axes.plot(
            lambda x: 1 / (1 + np.exp(k_tracker.get_value() * (x - x0_tracker.get_value()))),
            x_range=[0, 6.2],
            color=YELLOW,
            stroke_width=4
        ))

        with self.voiceover(text="We fit the sigmoid model to the data by finding optimal parameters.") as tracker:
            self.update_subtitle("Chúng ta khớp mô hình sigmoid với dữ liệu bằng cách tìm các tham số tối ưu.\n(We fit the sigmoid model to the data by finding optimal parameters.)")
            self.play(Create(sigmoid_curve), run_time=min(1, tracker.duration * 0.2))

            self.play(
                k_tracker.animate.set_value(3.0),
                x0_tracker.animate.set_value(5.0),
                run_time=min(1.2, tracker.duration * 0.25), 
                rate_func=linear
            )
            self.play(
                k_tracker.animate.set_value(0.5),
                x0_tracker.animate.set_value(1.5),
                run_time=min(1.0, tracker.duration * 0.2), 
                rate_func=linear
            )
            self.play(
                k_tracker.animate.set_value(1.5),
                x0_tracker.animate.set_value(3.0),
                run_time=min(1.5, tracker.duration * 0.3), 
                rate_func=smooth
            )

        all_coords = goals_coords + nogoals_coords
        projection_lines = VGroup()

        for x, y in all_coords:
            start_pt = axes.c2p(x, y, 0)
            y_sigmoid = 1 / (1 + np.exp(1.5 * (x - 3.0)))
            end_pt = axes.c2p(x, y_sigmoid, 0)
            
            line = DashedLine(start=start_pt, end=end_pt, color=YELLOW_A, stroke_width=1.5)
            projection_lines.add(line)

        with self.voiceover(text="The projection lines show how each data point relates to the fitted sigmoid curve.") as tracker:
            self.update_subtitle("Các đường gióng cho thấy mỗi điểm dữ liệu liên quan đến đường cong sigmoid được khớp.\n(The projection lines show how each data point relates to the fitted sigmoid curve.)")
            self.play(Create(projection_lines), run_time=min(1.8, tracker.duration * 0.4))

        # Subscene 5: KHÔNG GIAN 3D - LOGISTIC REGRESSION SURFACE
        self.play(
            FadeOut(projection_lines),
            FadeOut(sigmoid_curve),
            FadeOut(y1_line),
            FadeOut(x_label), FadeOut(y_label),
            FadeOut(lbl_y1), FadeOut(lbl_y0),
            FadeOut(goal_dots), FadeOut(nogoal_dots),
            run_time=0.8
        )

        self.play(
            FadeOut(axes),
            run_time=0.5
        )

        # self.add_fixed_in_frame_mobjects(title, logistic_text)  # Removed to avoid camera issues in 3D

        with self.voiceover(text="Now we extend this to three dimensions: distance, shot angle, and result.") as tracker:
            # self.update_subtitle("Bây giờ ta mở rộng thành ba chiều: khoảng cách, góc sút, và kết quả.\n(Now we extend this to three dimensions: distance, shot angle, and result.)")
            self.move_camera(phi=70 * DEGREES, theta=-60 * DEGREES, run_time=min(1.5, tracker.duration * 0.3))

        axes_3d = ThreeDAxes(
            x_range=[0, 7, 1],       
            y_range=[0, 90, 15],     
            z_range=[0, 1.2, 0.5],  
            x_length=4.0,
            y_length=4.0,
            z_length=3.0,
            axis_config={
                "color": GRAY,
                "stroke_width": 2,
                "include_numbers": False,
                "include_ticks": False,
            }
        ).move_to(ORIGIN + DOWN * 0.5)

        x_lbl_3d = Text("Distance (X)", font_size=14, color=WHITE)
        y_lbl_3d = Text("Shot Angle (Y)", font_size=14, color=WHITE)
        z_lbl_3d = Text("Result (Z)", font_size=14, color=WHITE)

        x_lbl_3d.next_to(axes_3d.x_axis.get_end(), RIGHT, buff=0.15)
        y_lbl_3d.next_to(axes_3d.y_axis.get_end(), OUT + UP, buff=0.1)
        z_lbl_3d.next_to(axes_3d.z_axis.get_end(), UP, buff=0.1)

        self.play(
            Create(axes_3d),
            Write(x_lbl_3d),
            Write(y_lbl_3d),
            Write(z_lbl_3d),
            run_time=1.5
        )

        prediction_surface = Surface(
            lambda u, v: axes_3d.c2p(
                u,
                v,
                1 / (1 + np.exp(1.5 * (u - 3.0) - 0.05 * (v - 45)))
            ),
            u_range=[0, 6.5],
            v_range=[0, 90],
            resolution=(20, 20),
        )
        prediction_surface.set_style(
            fill_opacity=0.35,
            fill_color=BLUE_C,
            stroke_color=TEAL_D,
            stroke_width=0.6
        )

        goals_3d = [
            (0.8, 75, 1),
            (2.6, 45, 1),
            (0.3, 80, 1),
            (1.5, 60, 1),
            (5.0, 30, 1),
        ]
        nogoals_3d = [
            (4.2, 15, 0),
            (0.8, 25, 0),
            (5.8, 10, 0),
            (2.8, 35, 0),
            (4.8, 15, 0),
        ]

        goal_dots_3d = VGroup(*[
            Dot3D(
                point=axes_3d.c2p(x, y, z),
                color=GREEN,
                radius=0.09
            ) for x, y, z in goals_3d
        ])
        nogoal_dots_3d = VGroup(*[
            Dot3D(
                point=axes_3d.c2p(x, y, z),
                color=RED,
                radius=0.09
            ) for x, y, z in nogoals_3d
        ])

        with self.voiceover(text="The 3D surface shows how goal probability depends on both distance and shot angle simultaneously.") as tracker:
            self.update_subtitle("Bề mặt 3D cho thấy xác suất ghi bàn phụ thuộc vào cả khoảng cách và góc sút cùng một lúc.\n(The 3D surface shows how goal probability depends on both distance and shot angle simultaneously.)")
            self.play(
                Create(prediction_surface),
                run_time=min(2.0, tracker.duration * 0.4)
            )
            self.play(
                FadeIn(goal_dots_3d),
                FadeIn(nogoal_dots_3d),
                run_time=min(1.0, tracker.duration * 0.2)
            )

        self.add_fixed_in_frame_mobjects(self.logo)

        with self.voiceover(text="Rotating the view helps us understand the three-dimensional structure better.") as tracker:
            self.update_subtitle("Xoay góc nhìn giúp chúng ta hiểu rõ hơn về cấu trúc ba chiều.\n(Rotating the view helps us understand the three-dimensional structure better.)")
            self.move_camera(
                phi=55 * DEGREES, theta=20 * DEGREES,
                run_time=min(2.5, tracker.duration * 0.25),
                rate_func=smooth
            )

            self.move_camera(
                phi=25 * DEGREES, theta=20 * DEGREES,
                run_time=min(2.5, tracker.duration * 0.25),
                rate_func=smooth
            )

            self.move_camera(
                phi=75 * DEGREES, theta=80 * DEGREES,
                run_time=min(2.5, tracker.duration * 0.25),
                rate_func=smooth
            )

            self.move_camera(
                phi=70 * DEGREES, theta=-60 * DEGREES,
                run_time=min(2.5, tracker.duration * 0.25),
                rate_func=smooth
            )

        # Subscene 6: Chiến thuật của các HLV
        self.play(
            FadeOut(axes_3d),
            FadeOut(x_lbl_3d), FadeOut(y_lbl_3d), FadeOut(z_lbl_3d),
            FadeOut(prediction_surface),
            FadeOut(goal_dots_3d), FadeOut(nogoal_dots_3d),
            FadeOut(logistic_text), 
            run_time=1.0
        )

        self.move_camera(phi=0 * DEGREES, theta=-90 * DEGREES, run_time=0.1)

        strategy_text = Text("Avoid long shots as much as possible", font_size=36, color=YELLOW)
        strategy_text.next_to(title, DOWN, buff=0.4)

        with self.voiceover(text="That is why modern football coaches like Pep Guardiola and Luis Enrique always try to bring the ball closer to the goal.") as tracker:
            self.update_subtitle("Đó là lý do tại sao các huấn luyện viên bóng đá hiện đại như Pep Guardiola và Luis Enrique luôn cố gắng đưa quả bóng gần gôn hơn.\n(That is why modern football coaches like Pep Guardiola and Luis Enrique always try to bring the ball closer to the goal.)")
            self.play(Write(strategy_text), run_time=min(1.2, tracker.duration * 0.3))

        pep_path = r"C:\Users\doman\Downloads\Project1-main\Roo-Code\assets\pep.png"
        enrique_path = r"C:\Users\doman\Downloads\Project1-main\Roo-Code\assets\enrique.png"

        if os.path.exists(pep_path):
            pep_img = ImageMobject(pep_path).scale_to_fit_width(6.0).move_to(UP * 0.2)
            
            with self.voiceover(text="Pep Guardiola is known for his tactical genius and data-driven approach.") as tracker:
                self.update_subtitle("Pep Guardiola nổi tiếng vì tài năng chiến thuật và phương pháp dựa trên dữ liệu của anh ta.\n(Pep Guardiola is known for his tactical genius and data-driven approach.)")
                self.play(FadeIn(pep_img, shift=UP * 0.3), run_time=min(1.0, tracker.duration * 0.4))
            
            self.play(FadeOut(pep_img, shift=DOWN * 0.3), run_time=0.8)

        if os.path.exists(enrique_path):
            enrique_img = ImageMobject(enrique_path).scale_to_fit_width(3.5).move_to(UP * 0.2)
            
            with self.voiceover(text="Luis Enrique also emphasizes positioning and probability in football.") as tracker:
                self.update_subtitle("Luis Enrique cũng nhấn mạnh vị trí và xác suất trong bóng đá.\n(Luis Enrique also emphasizes positioning and probability in football.)")
                self.play(FadeIn(enrique_img, shift=UP * 0.3), run_time=min(1.0, tracker.duration * 0.4))

        self.play(
            FadeOut(strategy_text),
            FadeOut(enrique_img),
            run_time=0.8
        )

        # Subscene 7: Các nguyên nhân ảnh hưởng xG
        reason_txt = Text("Some reasons may affect the xG", font_size=28, color=YELLOW_B)
        reason_txt.next_to(title, DOWN, buff=0.4)

        with self.voiceover(text="However, in reality, the model is never 100 percent accurate because there are unmeasurable variables like player psychology and grass texture.") as tracker:
            self.update_subtitle("Tuy nhiên, trên thực tế, mô hình không bao giờ chính xác 100% vì có những biến số không thể đo lường như tâm lý cầu thủ và độ xoáy của cỏ.\n(However, in reality, the model is never 100 percent accurate because there are unmeasurable variables like player psychology and grass texture.)")
            self.play(Write(reason_txt), run_time=min(1.0, tracker.duration * 0.3))

        messi_path = r"C:\Users\doman\Downloads\Project1-main\Roo-Code\assets\messi.png"
        ronaldo_path = r"C:\Users\doman\Downloads\Project1-main\Roo-Code\assets\crbuoi-Photoroom.png"

        if os.path.exists(messi_path):
            messi_img = ImageMobject(messi_path).scale_to_fit_width(5.0).move_to(UP * 0.3)
            self.add_fixed_in_frame_mobjects(messi_img)
            
            messi_txt = Text("Bro sent the ball to the universe", font_size=20, color=GRAY_A)
            messi_txt.next_to(messi_img, DOWN, buff=0.3)
            
            with self.voiceover(text="For example, sometimes players miss shots that seem certain.") as tracker:
                self.update_subtitle("Ví dụ, đôi khi cầu thủ bỏ lỡ những cú sút có vẻ chắc chắn.\n(For example, sometimes players miss shots that seem certain.)")
                self.play(FadeIn(messi_img, shift=UP * 0.2), Write(messi_txt), run_time=min(1.0, tracker.duration * 0.4))
            
            self.play(FadeOut(messi_img), FadeOut(messi_txt), run_time=0.6)

        if os.path.exists(ronaldo_path):
            ronaldo_img = ImageMobject(ronaldo_path).scale_to_fit_width(5.0).move_to(UP * 0.3)
            self.add_fixed_in_frame_mobjects(ronaldo_img)
            
            ronaldo_txt = Text("Bro slipped", font_size=18, color=GRAY_A)
            ronaldo_txt.next_to(ronaldo_img, DOWN, buff=0.3)
            
            with self.voiceover(text="Or sometimes they fail to score due to unexpected circumstances like bad footing.") as tracker:
                self.update_subtitle("Hoặc đôi khi họ thất bại trong ghi bàn do những tình huống bất ngờ như bước chân không vững.\n(Or sometimes they fail to score due to unexpected circumstances like bad footing.)")
                self.play(FadeIn(ronaldo_img, shift=UP * 0.2), Write(ronaldo_txt), run_time=min(1.0, tracker.duration * 0.4))
            
            self.play(
                FadeOut(ronaldo_img), 
                FadeOut(ronaldo_txt), 
                FadeOut(reason_txt), 
                run_time=0.8
            )

        # Other methods
        other_methods_title = Text("Other methods", font_size=32, color=BLUE_B, weight=BOLD)
        other_methods_title.next_to(title, DOWN, buff=0.4)
        
        pca_title = Text("1. Principal Component Analysis (PCA)", font_size=24, color=WHITE)
        pca_title.next_to(other_methods_title, DOWN, buff=0.3)
        
        with self.voiceover(text="To handle the enormous number of variables, analysts use techniques like Principal Component Analysis or heat maps.") as tracker:
            self.update_subtitle("Để xử lý số lượng biến khổng lồ, các nhà phân tích dùng các kỹ thuật như Phân tích Thành phần Chính hoặc bản đồ nhiệt.\n(To handle the enormous number of variables, analysts use techniques like Principal Component Analysis or heat maps.)")
            self.play(Write(other_methods_title), run_time=min(0.8, tracker.duration * 0.2))
            self.play(Write(pca_title), run_time=min(0.8, tracker.duration * 0.2))

        pca_img_path = r"C:\Users\doman\Downloads\Project1-main\Roo-Code\assets\1QinDfRawRskupf4mU5bYSA.webp"
        if os.path.exists(pca_img_path):
            pca_img = ImageMobject(pca_img_path).scale_to_fit_width(6.0).next_to(pca_title, DOWN, buff=0.4)
            self.add_fixed_in_frame_mobjects(pca_img)
            
            self.play(FadeIn(pca_img, shift=UP * 0.2), run_time=1.0)
            
            self.play(FadeOut(pca_img), run_time=0.6)

        heatmap_title = Text("2. Heatmap", font_size=24, color=WHITE)
        heatmap_title.next_to(pca_title, DOWN, buff=0.3)
        
        with self.voiceover(text="Heatmaps visualize the distribution of shot quality across different areas of the field.") as tracker:
            self.update_subtitle("Bản đồ nhiệt trực quan hóa sự phân bố chất lượng cú sút trên các khu vực khác nhau của sân.\n(Heatmaps visualize the distribution of shot quality across different areas of the field.)")
            self.play(Write(heatmap_title), run_time=min(0.8, tracker.duration * 0.2))

        heatmap_pitch_group = VGroup()

        pitch_border = Rectangle(width=6.0, height=5.5, stroke_color=GRAY, stroke_width=1.5)
        
        penalty_box = Rectangle(width=4.0, height=2.2, stroke_color=GRAY, stroke_width=1.2)
        penalty_box.align_to(pitch_border, UP) 
        
        goal_post = Rectangle(width=1.0, height=0.25, stroke_color=GRAY, stroke_width=1.2)
        goal_post.next_to(pitch_border, UP, buff=0)
        
        penalty_arc = Arc(
            radius=0.7, 
            start_angle=0 * DEGREES, 
            angle=-180 * DEGREES, 
            stroke_color=GRAY, 
            stroke_width=1.2
        )
        penalty_arc.move_to(penalty_box.get_bottom() + DOWN * 0.02)

        pitch_lines = VGroup(pitch_border, penalty_box, goal_post, penalty_arc)

        DARK_BROWN = "#1C1410"
        MED_BROWN  = "#402414"
        ORANGE_HOT = "#C87424"

        heatmap_data = [
            [("1%", DARK_BROWN),  ("5%", MED_BROWN),   ("3%", MED_BROWN),   ("1%", DARK_BROWN)],
            [("4%", MED_BROWN),   ("9%", ORANGE_HOT),  ("14%", ORANGE_HOT), ("3%", MED_BROWN)],
            [("5%", MED_BROWN),   ("7%", ORANGE_HOT),  ("11%", ORANGE_HOT), ("3%", MED_BROWN)],
            [("6%", MED_BROWN),   ("4%", MED_BROWN),   ("6%", MED_BROWN),   ("4%", MED_BROWN)],
            [("1%", DARK_BROWN),  ("4%", DARK_BROWN),  ("3%", DARK_BROWN),  ("2%", DARK_BROWN)],
            [("1%", DARK_BROWN),  ("1%", DARK_BROWN),  ("2%", DARK_BROWN),  ("1%", DARK_BROWN)]
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
                box.move_to(
                    RIGHT * (c_idx - 1.5) * box_width + 
                    DOWN * (r_idx - 1.0) * box_height
                )
                
                text = Text(pct_str, font="Courier New", font_size=16, color=WHITE)
                text.move_to(box.get_center())
                heatmap_grid.add(VGroup(box, text))

        heatmap_grid.move_to(pitch_border.get_center() + UP * 0.5)
        heatmap_pitch_group.add(pitch_lines, heatmap_grid)
        heatmap_pitch_group.next_to(heatmap_title, DOWN, buff=0.6)
        
        self.add_fixed_in_frame_mobjects(heatmap_pitch_group)

        self.play(FadeIn(heatmap_pitch_group, shift=UP * 0.3), run_time=1.5)

        self.play(FadeOut(heatmap_pitch_group), run_time=0.8)

        etc_text = Text("etc.", font_size=24, color=WHITE, font="Segoe UI", slant=ITALIC)
        etc_text.next_to(heatmap_title, DOWN, buff=0.4)
        
        with self.voiceover(text="And many other analytical methods exist.") as tracker:
            self.update_subtitle("Và nhiều phương pháp phân tích khác tồn tại.\n(And many other analytical methods exist.)")
            self.play(FadeIn(etc_text, shift=DOWN * 0.1), run_time=min(0.5, tracker.duration * 0.2))

        self.play(
            FadeOut(other_methods_title),
            FadeOut(pca_title),
            FadeOut(heatmap_title),
            FadeOut(etc_text),
            run_time=0.8
        )

        # Tóm tắt kiến thức
        sig_subtitle = Text("Statistical Significance: Goals vs xG", font_size=28, color=BLUE)
        sig_subtitle.next_to(title, DOWN, buff=0.3)
        self.add_fixed_in_frame_mobjects(sig_subtitle)

        with self.voiceover(text="In summary, we can see the statistical significance of xG very clearly.") as tracker:
            self.update_subtitle("Tóm lại, chúng ta có thể thấy ý nghĩa thống kê của xG rất rõ ràng.\n(In summary, we can see the statistical significance of xG very clearly.)")
            self.play(FadeIn(sig_subtitle, shift=UP*0.2), run_time=min(1.0, tracker.duration * 0.2))

        chart_data = {
            "Goals": 25,
            "xG": 18
        }
        
        bar_colors = [BLUE_C, RED_C]
        
        finishing_chart = BarChart(
            values=[chart_data["Goals"], chart_data["xG"]],
            bar_names=["Goals", "xG"],
            y_range=[0, 30, 5],
            y_length=4.5,
            x_length=6.0,
            axis_config={"include_numbers": True},
            bar_colors=bar_colors,
        ).scale_to_fit_width(6.5).move_to(DOWN*0.8)

        goals_label = DecimalNumber(chart_data["Goals"], num_decimal_places=0, color=WHITE, font_size=24)
        xg_label = DecimalNumber(chart_data["xG"], num_decimal_places=0, color=WHITE, font_size=24)
        
        goals_label.next_to(finishing_chart.bars[0], UP, buff=0.2)
        xg_label.next_to(finishing_chart.bars[1], UP, buff=0.2)
        
        chart_labels = VGroup(goals_label, xg_label)
        chart_group = VGroup(finishing_chart, chart_labels)

        with self.voiceover(text="If a player scores 25 goals but xG is only 18, they have better finishing skill than average.") as tracker:
            self.update_subtitle("Nếu cầu thủ ghi 25 bàn nhưng xG chỉ 18, anh ta có kỹ năng dứt điểm tốt hơn trung bình.\n(If a player scores 25 goals but xG is only 18, they have better finishing skill than average.)")
            self.play(
                FadeIn(finishing_chart.axes),
                GrowFromEdge(finishing_chart.bars, DOWN),
                FadeIn(chart_labels, shift=UP*0.2),
                run_time=min(2.0, tracker.duration * 0.3)
            )

        diff_line = DashedLine(goals_label.get_center(), xg_label.get_center(), color=YELLOW_C, stroke_width=2)
        diff_text = Text("+7 Goals", font_size=20, color=YELLOW_C)
        diff_text.next_to(diff_line, DOWN, buff=0.1)
        diff_visual = VGroup(diff_line, diff_text)
    
        self.play(Create(diff_line), FadeIn(diff_text), run_time=1.0)

        self.play(FadeOut(diff_visual), run_time=0.5)
        
        new_goals_val = 12
        new_xg_val = 18
        
        with self.voiceover(text="Conversely, scoring only 12 goals when xG was 18 means they were unlucky or lacked finishing skill.") as tracker:
            self.update_subtitle("Ngược lại, ghi chỉ 12 bàn khi xG là 18 có nghĩa là họ không may mắn hoặc thiếu kỹ năng dứt điểm.\n(Conversely, scoring only 12 goals when xG was 18 means they were unlucky or lacked finishing skill.)")
            self.play(
                finishing_chart.animate.change_bar_values([new_goals_val, new_xg_val]),
                FadeOut(chart_labels),
                run_time=min(2.0, tracker.duration * 0.3),
                rate_func=linear
            )

        goals_label_new = DecimalNumber(new_goals_val, num_decimal_places=0, color=WHITE, font_size=24)
        xg_label_new = DecimalNumber(new_xg_val, num_decimal_places=0, color=WHITE, font_size=24)
        
        goals_label_new.next_to(finishing_chart.bars[0], UP, buff=0.2)
        xg_label_new.next_to(finishing_chart.bars[1], UP, buff=0.2)
        
        chart_labels_new = VGroup(goals_label_new, xg_label_new)
        
        self.play(FadeIn(chart_labels_new, shift=UP*0.1), run_time=1.0)

        diff_line_new = DashedLine(goals_label_new.get_center(), xg_label_new.get_center(), color=RED_A, stroke_width=2)
        diff_text_new = Text("-6 Goals", font_size=20, color=RED_A)
        diff_text_new.next_to(diff_line_new, UP, buff=0.1)
        
        diff_visual_new = VGroup(diff_line_new, diff_text_new)
        self.add_fixed_in_frame_mobjects(diff_visual_new)
        
        self.play(Create(diff_line_new), FadeIn(diff_text_new, scale=0.8), run_time=0.8)

        self.play(
            FadeOut(sig_subtitle),
            FadeOut(finishing_chart),
            FadeOut(chart_labels_new),
            FadeOut(diff_visual_new),
            run_time=0.8
        )

        # Model comparison
        model_subtitle = Text("Limit: Difference in AI Models", font_size=28, color=GREEN)
        model_subtitle.next_to(title, DOWN, buff=0.3)
        self.add_fixed_in_frame_mobjects(model_subtitle)

        with self.voiceover(text="Of course, xG also has limitations because different companies like Opta and StatsBomb use different models.") as tracker:
            self.update_subtitle("Tất nhiên xG cũng có hạn chế vì các hãng khác nhau như Opta và StatsBomb dùng các mô hình khác nhau.\n(Of course, xG also has limitations because different companies like Opta and StatsBomb use different models.)")
            self.play(FadeIn(model_subtitle, shift=UP*0.2), run_time=min(1.2, tracker.duration * 0.3))

        opta_label = Text("Opta Model", font_size=24, color=BLUE_B)
        opta_box = RoundedRectangle(corner_radius=0.3, width=3.5, height=1.0, color=BLUE_B, stroke_width=2)
        opta_group = VGroup(opta_box, opta_label).move_to(LEFT*2.2 + DOWN*1.0)
        
        statsbomb_label = Text("StatsBomb Model", font_size=22, color=ORANGE)
        statsbomb_box = RoundedRectangle(corner_radius=0.3, width=3.5, height=1.0, color=ORANGE, stroke_width=2)
        statsbomb_group = VGroup(statsbomb_box, statsbomb_label).move_to(RIGHT*2.2 + DOWN*1.0)
        
        opta_val = Text("xG: 0.23", font_size=22, color=WHITE).next_to(opta_box, DOWN, buff=0.3)
        stats_val = Text("xG: 0.19", font_size=22, color=WHITE).next_to(statsbomb_box, DOWN, buff=0.3)
        
        comparison_group = VGroup(opta_group, statsbomb_group, opta_val, stats_val)
        comparison_group.scale_to_fit_width(6.8)
        
        with self.voiceover(text="For the same chance, different models may calculate different xG values, showing the subjectivity of algorithms.") as tracker:
            self.update_subtitle("Với cùng một cơ hội, các mô hình khác nhau có thể tính toán các giá trị xG khác nhau, cho thấy tính chủ quan của thuật toán.\n(For the same chance, different models may calculate different xG values, showing the subjectivity of algorithms.)")
            self.play(FadeIn(opta_group, shift=RIGHT*0.2), Write(opta_val), run_time=min(1.0, tracker.duration * 0.25))
            self.play(FadeIn(statsbomb_group, shift=LEFT*0.2), Write(stats_val), run_time=min(1.0, tracker.duration * 0.25))

        self.play(
            FadeOut(model_subtitle),
            FadeOut(comparison_group),
            FadeOut(title), 
            run_time=1.0
        )

        with self.voiceover(text="Thank you for watching. Now you understand the concept of expected goals in football!") as tracker:
            self.update_subtitle("Cảm ơn bạn đã xem. Bây giờ bạn hiểu rõ khái niệm bàn thắng kỳ vọng trong bóng đá!\n(Thank you for watching. Now you understand the concept of expected goals in football!)")
            self.wait(min(2, tracker.duration * 0.5))


# Cấu hình và render
if __name__ == "__main__":
    scene = mainScene()
    scene.render()
    
    video_file = Path(config.media_dir) / "videos" / "1280p15" / "mainScene.mp4"
    if video_file.exists():
        print(f"Video rendered successfully: {video_file}")
    else:
        found = list(Path(config.media_dir).glob("**/mainScene.mp4"))
        if found:
            print(f"Video found at: {found[0]}")
        else:
            print("Render completed but video file not found.")
