import sys
import os
import numpy as np
# [QUY TẮC 1: HACK PATH]
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from skills.fami_lib import *

class Scene6_QuyMoSo_Part1(FaMIBaseScene):
    def construct(self):
        # 1. TIÊU ĐỀ
        title = self.create_title("BƯỚC 3: BIẾN ĐỔI QUY MÔ", "CHUẨN HÓA DỮ LIỆU")
        
        # ==========================================
        # 🎨 TẠO ASSETS: MA TRẬN VÀ AI LOGO
        # ==========================================
        
        # --- Ma trận Pixel (Bên Trái) ---
        matrix_data = [["255", "120", "85"], ["200", "45", "150"], ["10", "240", "90"]]
        pixel_matrix = Matrix(matrix_data, left_bracket="[", right_bracket="]").set_color(WHITE)
        pixel_matrix.scale(0.8).to_edge(LEFT, buff=1.0)
        
        # --- AI Logo (Bên Phải) - Dùng code của bạn cung cấp ---
        ai_circle = Circle(radius=1.5, color=FAMI_CYAN, stroke_width=2)
        ai_hex = RegularPolygon(n=6, color=FAMI_BLUE, fill_opacity=0.15).scale(1.6)
        ai_text = Text("AI", font="Segoe UI", font_size=65, weight=BOLD, color=WHITE)
        neurons = VGroup(*[Line(ORIGIN, np.array([np.cos(a), np.sin(a), 0]) * 2.2, color=FAMI_CYAN, stroke_width=2, stroke_opacity=0.4)
            for a in np.linspace(0, 2*PI, 12, endpoint=False)])
        dots = VGroup(*[Dot(l.get_end(), color=ACCENT, radius=0.07) for l in neurons])
        
        # Gom nhóm và đặt bên Phải
        ai_logo = VGroup(ai_hex, neurons, dots, ai_circle, ai_text)
        ai_logo.scale(0.6).to_edge(RIGHT, buff=1.0)

        # ==========================================
        # 🎬 ĐỒNG BỘ VOICEOVER
        # ==========================================

        # --- ĐOẠN 1: Hiện Ma trận và Logo ---
        with self.voiceover(text="Khía cạnh cuối cùng là biến đổi Quy mô.") as tracker:
            self.update_subtitle("Khía cạnh cuối cùng là biến đổi Quy mô.")
            self.play(Write(title), run_time=0.6)
            self.play(FadeIn(pixel_matrix, shift=RIGHT*0.2), FadeIn(ai_logo, shift=LEFT*0.2), run_time=min(1.0, tracker.duration * 0.8))

        # --- ĐOẠN 2: Hiệu ứng dữ liệu chảy vào AI ---
        with self.voiceover(text="Khi đưa ảnh vào AI, các pixel mang giá trị từ 0 đến 255.") as tracker:
            self.update_subtitle("Khi đưa ảnh vào AI, các pixel mang giá trị từ 0 đến 255.")
            
            # Tạo hiệu ứng các con số từ ma trận "rút ruột" bay vào logo AI
            # Ta dùng LaggedStart để các số bay ra nối đuôi nhau chứ không bay cùng lúc
            flying_anims = []
            for entry in pixel_matrix.get_entries():
                ghost_num = entry.copy()
                self.add(ghost_num) # Thêm bản sao vào màn hình
                # Animation: Bay theo đường cong (path_arc) thu nhỏ lại và chui vào tâm AI
                anim = ghost_num.animate(path_arc=-PI/4).move_to(ai_logo.get_center()).scale(0.1).set_opacity(0)
                flying_anims.append(anim)
            
            # Thực thi loạt animation bắn số
            # KÉO DÀI HIỆU ỨNG:
            # - Tăng run_time lên (VD: 2.5s)
            # - Tăng lag_ratio lên 0.2 (để các số bay ra cách nhau quãng nghỉ rõ hơn)
            self.play(
                LaggedStart(*flying_anims, lag_ratio=0.1),
                Indicate(ai_logo[3], color=SUCCESS), # Logo AI nhấp nháy nhận dữ liệu
                run_time=max(2.0, tracker.duration * 0.4)
            )

        # --- ĐOẠN 3: Thu nhỏ lên đỉnh và Đồ thị bùng nổ ---
        with self.voiceover(text="Nếu nhân các số lớn này qua hàng chục lớp mạng sẽ gây ra hiện tượng bùng nổ Gradient") as tracker:
            self.update_subtitle("Nhân các số lớn này qua nhiều lớp...")
            
            # Bước A: Đẩy Ma trận và AI lên sát dưới tiêu đề
            self.play(
                pixel_matrix.animate.scale(0.6).next_to(title, DOWN, buff=0.2).shift(LEFT * 2),
                ai_logo.animate.scale(0.6).next_to(title, DOWN, buff=0.2).shift(RIGHT * 2),
                run_time=min(0.8, tracker.duration * 0.3)
            )
            self.wait(tracker.duration * 0.1)
            self.update_subtitle("sẽ gây ra hiện tượng bùng nổ Gradient")
            # Bước B: Khởi tạo và vẽ Đồ thị "Exploding Gradient"
            # Trục tọa độ nằm dưới
            axes = Axes(
                x_range=[0, 5, 1], y_range=[0, 10, 2],
                axis_config={"color": GRAY, "include_tip": False}
            ).scale(0.6).move_to(DOWN * 1.5)
            
            # Đường cong hàm số mũ (vọt lên rất nhanh)
            # Khóa x_range để nó không đâm xuyên ra khỏi trục Y trên cùng
            curve = axes.plot(lambda x: 0.1 * np.exp(x * 1.2), color=DANGER, x_range=[0, 3.8])
            
            # Nhãn cảnh báo
            alert_lbl = Text("EXPLODING GRADIENTS!", font="Segoe UI", font_size=32, weight=BOLD, color=DANGER)
            alert_lbl.next_to(axes, UP, buff=0.2)

            # Thực thi vẽ đồ thị (Đồng bộ với câu "bùng nổ vô cực")
            self.play(Create(axes), run_time=tracker.duration * 0.2)
            self.play(
                Create(curve), 
                Write(alert_lbl), 
                run_time=tracker.duration * 0.3,
                rate_func=rate_functions.ease_in_expo # Hiệu ứng chạy chậm lúc đầu rồi vọt nhanh
            )
            self.wait(tracker.get_remaining_duration())

        # --- ĐOẠN 3: PHÉP CHIA 255 (MIN-MAX SCALING) ---
        with self.voiceover(text="Cách đơn giản nhất là lấy ma trận chia cho 255 để ép mọi con số về khoảng 0 đến 1.") as tracker:
            self.update_subtitle("Cách đơn giản nhất là lấy ma trận chia cho 255...")
            
            # 1. Dọn dẹp màn hình (Logo AI, Đồ thị bùng nổ, Text...)
            self.play(
                FadeOut(ai_logo),
                FadeOut(axes), FadeOut(curve), FadeOut(alert_lbl),
                run_time=0.6
            )
            
            # 2. Đưa ma trận ra giữa màn hình
            self.play(pixel_matrix.animate.scale(1.2).move_to(ORIGIN), run_time=0.6)
            
            # 3. Hiện phép toán "Chia 255" ở trên đầu ma trận
            div_note = MathTex(r"\text{Chia cho } 255", color=FAMI_CYAN).scale(1.2).next_to(pixel_matrix, UP, buff=0.5)
            self.play(Write(div_text := MathTex(r"\div 255", color=FAMI_CYAN).next_to(pixel_matrix, UP, buff=0.5)), run_time=0.6)
            
            # 4. ANIMATION: Thay đổi con số (Ép về 0-1)
            # Dữ liệu ma trận mới
            new_data = [["1.00", "0.47", "0.33"], ["0.78", "0.18", "0.59"], ["0.04", "0.94", "0.35"]]
            self.update_subtitle("để ép mọi con số về khoảng 0 đến 1")
            # Biến đổi các con số cũ thành số mới
            new_matrix = Matrix(new_data, left_bracket="[", right_bracket="]").scale(0.8 * 1.2).move_to(pixel_matrix)
            new_matrix.set_color(FAMI_CYAN) # Đổi màu để nhận diện đã chuẩn hóa
            
            self.play(
                ReplacementTransform(pixel_matrix, new_matrix),
                run_time=min(1.5, tracker.duration * 0.6)
            )
            
            self.play(FadeOut(div_text), run_time=0.4)
            self.wait(tracker.get_remaining_duration())

        # --- ĐOẠN 3: Z-SCORE & NORMALIZATION ---
        with self.voiceover(text="Tuy nhiên, mạng nơ-ron thực sự thích dữ liệu có tính cân bằng quanh điểm 0 hơn.") as tracker:
            self.update_subtitle("Tuy nhiên, mạng nơ-ron thích dữ liệu cân bằng quanh điểm 0 hơn.")
            
            # 1. Dời ma trận [0, 1] lên trên (Sát tiêu đề)
            self.play(
                new_matrix.animate.scale(0.7).next_to(title, DOWN, buff=0.3),
                run_time=0.6
            )
            
            # 2. Đồ thị phân phối (Nằm giữa màn hình, chừa khoảng trống cho phụ đề)
            # Dùng Axes nhỏ hơn, nằm ở Y=0
            dist_axes = Axes(x_range=[-3, 3, 1], y_range=[0, 1, 0.5], axis_config={"include_ticks": True}).scale(0.6).move_to(ORIGIN)
            dist_curve = dist_axes.plot(lambda x: np.exp(-x**2), color=ACCENT)
            dist_group = VGroup(dist_axes, dist_curve)
            
            self.play(FadeIn(dist_group, shift=UP*0.3), run_time=0.8)

        with self.voiceover(text="Đó là lúc ta dùng công thức Z-score: Trừ đi Trung bình miu, chia cho Độ lệch chuẩn xích-ma.") as tracker:
            self.update_subtitle("Đó là lúc ta dùng công thức Z-score: Trừ trung bình, chia độ lệch chuẩn.")
            
            # Hiện công thức Z-score ngay dưới đồ thị
            z_formula = MathTex(r"X_{new} = \frac{X - \mu}{\sigma}", color=WHITE).scale(1.0)
            z_formula.next_to(dist_group, DOWN, buff=0.4)
            self.play(Write(z_formula), run_time=0.8)

        with self.voiceover(text="Dữ liệu sẽ tập trung quanh số 0, có cả âm và dương.") as tracker:
            self.update_subtitle("Dữ liệu sẽ tập trung quanh số 0, có cả âm và dương.")
            
            # 1. Dọn dẹp đồ thị và công thức
            self.play(FadeOut(dist_group), FadeOut(z_formula), run_time=0.5)
            
            # 2. Ma trận ra giữa màn hình
            self.play(new_matrix.animate.scale(1.5).move_to(ORIGIN), run_time=0.6)
            
            # 3. CHUYỂN ĐỔI SỐ (Z-SCORE LOGIC)
            # Dữ liệu Z-score (Ví dụ: [1.2, -0.5, 0.0, -1.1...])
            z_data = [["1.23", "-0.45", "0.02"], ["-0.89", "0.15", "-1.21"], ["0.55", "-0.12", "0.78"]]
            z_matrix = Matrix(z_data, left_bracket="[", right_bracket="]").scale(1.2).move_to(new_matrix)
            z_matrix.set_color(SUCCESS) # Màu xanh thành công cho Z-score
            
            self.play(ReplacementTransform(new_matrix, z_matrix), run_time=1.0)
            
            # Thêm nhãn nhỏ báo hiệu Batch Norm
            batch_label = Text("BATCH NORM", font="Segoe UI", font_size=24, color=SUCCESS, weight=BOLD)
            batch_label.next_to(z_matrix, DOWN, buff=0.5)
            self.play(FadeIn(batch_label), run_time=0.5)
            self.wait(tracker.get_remaining_duration())
        self.finish_scene()