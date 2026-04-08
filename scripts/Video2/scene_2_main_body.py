import sys
import os
import numpy as np
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from skills.fami_lib import *
from skills.fami_effects import animate_pop_in
from skills.fami_assets_helper import load_svg_icon

class Scene2_MainBody(FaMIBaseScene):
    def construct(self):
        title = self.create_title("HỒI QUY TUYẾN TÍNH", "DỰ ĐOÁN TƯƠNG LAI")
        
        # ==========================================
        # 🎨 VÙNG SÁNG TẠO (CREATIVE ZONE)
        # ==========================================
        
        # 1. Khung App điện thoại
        app_bg = RoundedRectangle(width=6.0, height=6.0, corner_radius=0.5, color=WHITE, fill_opacity=0.1)
        app_header = Rectangle(width=6.0, height=0.8, color=WHITE, fill_opacity=0.3).align_to(app_bg, UP)
        app_title = Text("Bất Động Sản AI", font="Segoe UI", font_size=24, color=WHITE).move_to(app_header)
        app_group = VGroup(app_bg, app_header, app_title).move_to(UP * 0.5)

        # 2. Đồ thị Data (Bên trong App)
        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 10, 2],
            x_length=4.5,
            y_length=3.5,
            axis_config={"color": GRAY, "include_tip": False}
        ).move_to(app_bg).shift(UP * 0.2)
        
        # Data points
        np.random.seed(42)
        x_vals = np.random.uniform(1, 9, 15)
        y_vals = 0.8 * x_vals + 1.0 + np.random.normal(0, 0.8, 15) # Y = 0.8X + 1 + noise
        dots = VGroup(*[Dot(axes.c2p(x, y), color=FAMI_CYAN, radius=0.06) for x, y in zip(x_vals, y_vals)])

        # Regression line
        line = axes.plot(lambda x: 0.8 * x + 1.0, color=YELLOW)

        graph_group = VGroup(axes, dots, line)
        
        # 3. Kết quả dự đoán
        result_box = RoundedRectangle(width=4.5, height=1.0, color=SUCCESS, fill_color=BLACK, fill_opacity=0.8)
        result_text = Text("$3.5 TỶ VNĐ", font="Segoe UI", font_size=32, weight=BOLD, color=SUCCESS)
        check_icon = load_svg_icon("assets/check.svg").scale_to_fit_width(0.6).set_color(SUCCESS)
        
        result_text.move_to(result_box).shift(LEFT * 0.4)
        check_icon.next_to(result_text, RIGHT, buff=0.3)
        result_group = VGroup(result_box, result_text, check_icon).next_to(axes, DOWN, buff=0.4)

        # Ensure layout fits
        main_stage = VGroup(app_group, graph_group, result_group)
        if main_stage.width > 7.5:
            main_stage.scale_to_fit_width(7.5)

        # ==========================================
        # 🎬 ĐỒNG BỘ VOICEOVER CHUẨN
        # ==========================================
        with self.voiceover(text="Tóm lại, hồi quy tuyến tính giúp ta tìm ra quy luật từ dữ liệu quá khứ, bằng cách vẽ các đường hoặc mặt phẳng, để tự tin dự báo cho tương lai.") as tracker:
            
            # Ý 1
            self.update_subtitle("Tóm lại, hồi quy tuyến tính giúp ta tìm ra quy luật từ dữ liệu quá khứ")
            self.play(Write(title), run_time=min(1.0, tracker.duration * 0.1))
            self.play(FadeIn(app_group, scale=0.9), FadeIn(axes), run_time=tracker.duration * 0.2)
            self.play(Create(dots), run_time=tracker.duration * 0.2)
            
            # Ý 2
            self.update_subtitle("bằng cách vẽ các đường hoặc mặt phẳng, để tự tin dự báo cho tương lai.")
            self.play(Create(line), run_time=tracker.duration * 0.3)

        with self.voiceover(text="Thông qua đó ta có thể dữ đoán giá nhà với sai lệch nhỏ nhất.") as tracker:
            self.update_subtitle("Thông qua đó ta có thể dự đoán giá nhà với sai lệch nhỏ nhất.")
            
            # Xuất hiện kết quả (Pop-in)
            self.play(animate_pop_in(result_group, scale_factor=1.1, run_time=tracker.duration * 0.6))
            
        self.finish_scene()
