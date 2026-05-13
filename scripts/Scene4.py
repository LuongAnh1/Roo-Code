import sys
import os
import numpy as np
# [QUY TẮC 1: HACK PATH]
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from skills.fami_lib import *

class Scene4_HoanThien_AI_Training(FaMIBaseScene):
    def construct(self):
        # ==========================================
        # 🎨 KHỞI TẠO ASSETS (Phần 1: Cảnh cũ)
        # ==========================================
        def create_math_matrix(val, color, title):
            data = [[r"\cdots", r"\cdots", r"\cdots"],[r"\cdots", str(val), r"\cdots"],[r"\cdots", r"\cdots", r"\cdots"]]
            mat = Matrix(data, left_bracket="[", right_bracket="]").set_color(WHITE)
            mat.get_entries().set_color(GRAY_C)
            mat.get_entries()[4].set_color(color).scale(1.3)
            lbl = Text(title, font="Segoe UI", weight=BOLD, font_size=24, color=color).next_to(mat, UP, buff=0.2)
            return VGroup(mat, lbl)

        grp_r = create_math_matrix(120, RED, "Red")
        grp_g = create_math_matrix(45, GREEN, "Green")
        grp_b = create_math_matrix(200, BLUE, "Blue")
        rgb_matrices = VGroup(grp_r, grp_g, grp_b).arrange(RIGHT, buff=0.4).scale(0.7).move_to(UP * 2.5)
        grp_gray = create_math_matrix(85, ACCENT, "Gray").scale(0.8).move_to(DOWN * 2.5)

        formula_2lines = MathTex(
            "120", r"\times 0.299 \ + ", "45", r"\times 0.587 \\ + \ ", "200", r"\times 0.114 \ = \ ", "85" 
        ).scale_to_fit_width(7.5).move_to(ORIGIN)
        for i, color in zip([0, 2, 4, 6], [RED, GREEN, BLUE, ACCENT]): formula_2lines[i].set_color(color)

        formula_1line = MathTex(
            "120", r"\times 0.299 \ + \ ", "45", r"\times 0.587 \ + \ ", "200", r"\times 0.114 \ = \ ", "85"
        ).scale_to_fit_width(8.5).move_to(ORIGIN)
        for i, color in zip([0, 2, 4, 6], [RED, GREEN, BLUE, ACCENT]): formula_1line[i].set_color(color)

        title = self.create_title("BƯỚC 1: BIẾN ĐỔI GIÁ TRỊ", "LUMINOSITY METHOD")
        self.add(title, rgb_matrices, grp_gray, formula_2lines)

        # ==========================================
        # 🎨 KHỞI TẠO ASSETS (Phần 2: AI & Training)
        # ==========================================
        
        # LOGO AI
        ai_circle = Circle(radius=1.5, color=FAMI_CYAN, stroke_width=2)
        ai_hex = RegularPolygon(n=6, color=FAMI_BLUE, fill_opacity=0.15).scale(1.6)
        ai_text = Text("AI", font="Segoe UI", font_size=65, weight=BOLD, color=WHITE)
        neurons = VGroup(*[Line(ORIGIN, np.array([np.cos(a), np.sin(a), 0]) * 2.2, color=FAMI_CYAN, stroke_width=2, stroke_opacity=0.4)
            for a in np.linspace(0, 2*PI, 12, endpoint=False)])
        dots = VGroup(*[Dot(l.get_end(), color=ACCENT, radius=0.07) for l in neurons])
        ai_logo = VGroup(ai_hex, neurons, dots, ai_circle, ai_text).move_to(UP * 0.2)
        
        conv_label = Text("CONVOLUTIONAL LAYER", font="Segoe UI", font_size=32, weight=BOLD, color=FAMI_CYAN)

        # CÔNG THỨC W_i (AI tự học)
        formula_w = MathTex("120", r"\times", "w_1", "+", "45", r"\times", "w_2", "+", "200", r"\times", "w_3", "=", "?")
        formula_w.scale(0.8).next_to(conv_label, DOWN, buff=0.5)
        formula_w[0].set_color(RED); formula_w[2].set_color(RED)
        formula_w[4].set_color(GREEN); formula_w[6].set_color(GREEN)
        formula_w[8].set_color(BLUE); formula_w[10].set_color(BLUE)

        # VECTOR TRỌNG SỐ (Bên Trái)
        val_w1 = ValueTracker(0.29); val_w2 = ValueTracker(0.58); val_w3 = ValueTracker(0.11)
        def get_vector():
            vec = MathTex(
                r"\begin{bmatrix} w_1 \\ w_2 \\ w_3 \end{bmatrix} = \begin{bmatrix}",
                f"{val_w1.get_value():.2f}", r"\\", f"{val_w2.get_value():.2f}", r"\\", f"{val_w3.get_value():.2f}", r"\end{bmatrix}"
            ).scale(0.8).to_edge(LEFT, buff=0.6).shift(DOWN * 1.5)
            vec[1].set_color(RED); vec[3].set_color(GREEN); vec[5].set_color(BLUE)
            return vec
        weights_vector = always_redraw(get_vector)

        # CÀ CHUA INPUT & OUTPUT (Bên Phải)
        try:
            tomato_in = ImageMobject("assets/tomato.jpg").scale_to_fit_width(2.0)
            px = tomato_in.pixel_array.copy()
            gray = (px[:,:,0]*0.299 + px[:,:,1]*0.587 + px[:,:,2]*0.114).astype(np.uint8)
            px[:,:,0] = px[:,:,1] = px[:,:,2] = gray
            tomato_gray = ImageMobject(px).scale_to_fit_width(2.0)
        except:
            tomato_in = Circle(radius=1.0, color=RED, fill_opacity=0.8)
            tomato_gray = Circle(radius=1.0, color=GRAY, fill_opacity=0.8)

        tomato_in.to_edge(RIGHT, buff=0.8).shift(UP * 0.5)
        tomato_gray.next_to(tomato_in, DOWN, buff=0.8)
        lbl_in = Text("Input", font_size=18, weight=BOLD).next_to(tomato_in, UP, buff=0.1)
        lbl_out = Text("Output (Xám)", font_size=18, weight=BOLD).next_to(tomato_gray, UP, buff=0.1)
        arrow_proc = Arrow(tomato_in.get_bottom(), tomato_gray.get_top(), color=FAMI_CYAN, buff=0.1)
        
        # Mask xám/đen che cà chua
        black_mask = Rectangle(width=2.0, height=2.0, fill_color=BLACK, fill_opacity=0, stroke_width=0).move_to(tomato_gray)

        # ==========================================
        # 🎬 ĐỒNG BỘ VOICEOVER
        # ==========================================

        # --- ĐOẠN 1: TỪ CHỐI CỐ ĐỊNH, GỌI TÊN AI ---
        with self.voiceover(text="NHƯNG, với AI thì khác!") as tracker:
            self.update_subtitle("NHƯNG, với AI thì khác!")
            new_title = self.create_title("BƯỚC 1: BIẾN ĐỔI GIÁ TRỊ", "CNN 1x1 (AI TỰ HỌC)")
            self.play(
                FadeOut(rgb_matrices, shift=UP), FadeOut(grp_gray, shift=DOWN),
                formula_2lines.animate.scale(0.6).move_to(DOWN * 3.5),
                FadeIn(ai_logo, scale=0.5), Transform(title, new_title),
                run_time=min(1.2, tracker.duration * 0.8)
            )

        with self.voiceover(text="Một lớp Convolution 1 nhân 1 trong mạng CNN cũng làm y hệt phép toán này.") as tracker:
            self.update_subtitle("Một lớp Convolution 1x1 cũng làm y hệt phép toán này.")
            self.play(
                ai_logo.animate.scale(0.3).next_to(title, DOWN, buff=0.2),
                FadeIn(conv_label.next_to(ai_logo, DOWN, buff=0.1), shift=UP*0.2),
                ReplacementTransform(formula_2lines, formula_1line),
                run_time=min(1.5, tracker.duration * 0.8)
            )

        with self.voiceover(text="Điểm khác biệt là: AI không dùng số cố định, nó tự học!") as tracker:
            self.update_subtitle("Điểm khác biệt: AI không dùng số cố định, nó TỰ HỌC!")
            
            fixed_text = Text("CỐ ĐỊNH (HARDCODED)", font="Segoe UI", font_size=28, color=DANGER, weight=BOLD).next_to(formula_1line, DOWN, buff=0.4)
            hardcoded_content = VGroup(formula_1line, fixed_text)
            box = RoundedRectangle(corner_radius=0.2, width=hardcoded_content.width + 0.8, height=hardcoded_content.height + 0.6, color=DANGER, stroke_width=3, fill_color=DANGER, fill_opacity=0.1).move_to(hardcoded_content)
            hardcoded_module = VGroup(box, hardcoded_content)
            if hardcoded_module.width > 8.2: hardcoded_module.scale_to_fit_width(8.2)

            self.play(
                Indicate(formula_1line[1], color=DANGER, scale_factor=1.2),
                Indicate(formula_1line[3], color=DANGER, scale_factor=1.2),
                Indicate(formula_1line[5], color=DANGER, scale_factor=1.2),
                run_time=tracker.duration * 0.4
            )
            self.play(Create(box), Write(fixed_text), run_time=tracker.duration * 0.4)
            self.play(Indicate(hardcoded_module, scale_factor=1.03, color=DANGER), run_time=0.5)

        # --- ĐOẠN 2: TRAINING CÀ CHUA ---
        with self.voiceover(text="Ví dụ bạn dạy nó nhận diện quả cà chua chín, thuật toán sẽ tự động ép trọng số màu Đỏ tăng vọt lên,") as tracker:
            self.update_subtitle("Ví dụ dạy nhận diện quả cà chua chín...")
            
            # 1. TẠO BỐ CỤC ĐÍCH (TARGET) MÀ KHÔNG LÀM THAY ĐỔI VẬT THỂ THẬT NGAY LẬP TỨC
            # Ta dùng .copy() để tạo các bản sao ảo nhằm tính toán tọa độ
            header_target = VGroup(ai_logo.copy(), conv_label.copy()).arrange(RIGHT, buff=0.3)
            header_target.scale(0.8).next_to(title, DOWN, buff=0.2)
            
            # Tính toán vị trí cho công thức w_i (đặt dưới cụm header vừa tính)
            formula_w_target_pos = header_target.get_bottom() + DOWN * 0.3

            # 2. THỰC THI ANIMATION: BÂY GIỜ CÁC VẬT THỂ SẼ DI CHUYỂN
            self.play(
                # Dọn dẹp module cũ
                FadeOut(box), 
                FadeOut(fixed_text),
                
                # DI CHUYỂN Logo và Chữ sang ngang hàng
                ai_logo.animate.move_to(header_target[0].get_center()).scale(0.8),
                conv_label.animate.move_to(header_target[1].get_center()).scale(0.8),
                
                # BIẾN ĐỔI công thức cũ thành w_i và bay lên vị trí dưới header
                ReplacementTransform(formula_1line, formula_w.move_to(formula_w_target_pos).scale(0.9)),

                # Hiện các thành phần training ở dưới
                FadeIn(weights_vector, shift=RIGHT*0.3),
                FadeIn(VGroup(tomato_in, lbl_in, tomato_gray, lbl_out, black_mask), shift=LEFT*0.3),
                
                run_time=1.2 # Thời gian đủ để thấy sự sắp xếp lại
            )
            
            self.update_subtitle("thuật toán tự động ép trọng số màu Đỏ tăng vọt lên,")
            
            # 3. TIẾN TRÌNH TRAINING (Số nhảy, ảnh tối dần)
            self.play(
                val_w1.animate.set_value(0.98), 
                val_w2.animate.set_value(0.01), 
                val_w3.animate.set_value(0.01),
                black_mask.animate.set_fill(opacity=0.8), 
                run_time=min(2.0, tracker.duration * 0.6), 
                rate_func=rate_functions.ease_in_out_sine
            )
            
        # --- NHỊP TIẾP THEO: KẾT LUẬN ---
        with self.voiceover(text="biến lớp Convolution này thành một bộ lọc màu tối ưu riêng cho cà chua!") as tracker:
            self.update_subtitle("biến lớp Convolution thành bộ lọc tối ưu RIÊNG cho cà chua!")
            self.play(
                Indicate(formula_w[2], color=SUCCESS), 
                Indicate(tomato_gray, color=RED, scale_factor=1.1), 
                run_time=tracker.duration * 0.8
            )
        # --- ĐOẠN 3: KẾT THÚC (LIỆT KÊ SỨC MẠNH CNN) ---
        with self.voiceover(text="Sức mạnh của CNN không chỉ dừng ở đó mà còn ở các lớp Convolution lớn hơn như Conv 3x3, Conv 6x6,…") as tracker:
            self.update_subtitle("Sức mạnh của CNN còn ở các lớp Convolution lớn hơn...")
            
            # Dọn dẹp màn hình cực nhanh
            self.play(
                FadeOut(VGroup(ai_logo, conv_label, formula_w, weights_vector, tomato_in, lbl_in, tomato_gray, lbl_out, black_mask)),
                run_time=0.5
            )

            # TẠO DANH SÁCH LIỆT KÊ (NEAT & CLEAN)
            list_title = Text("SỨC MẠNH MỞ RỘNG CỦA CNN", font="Segoe UI", font_size=32, color=FAMI_CYAN, weight=BOLD)
            
            def create_item(icon_text, desc_text, color):
                box = RoundedRectangle(width=1.5, height=0.8, corner_radius=0.1, stroke_width=2, color=color, fill_opacity=0.1)
                icon = Text(icon_text, font="Segoe UI", font_size=24, weight=BOLD, color=color).move_to(box)
                desc = Text(desc_text, font="Segoe UI", font_size=28).next_to(box, RIGHT, buff=0.4)
                return VGroup(box, icon, desc)

            item1 = create_item("1x1", "Xử lý màu sắc (Pixel)", GRAY)
            item2 = create_item("3x3", "Phát hiện Góc, Cạnh", ACCENT)
            item3 = create_item("6x6", "Nhận diện Hình khối lớn", FAMI_CYAN)

            features_list = VGroup(list_title, item1, item2, item3).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to(ORIGIN)

            self.play(FadeIn(list_title, shift=UP*0.2), run_time=0.4)
            self.play(FadeIn(item1, shift=RIGHT*0.2), run_time=0.3)
            
            self.update_subtitle("như Conv 3x3, Conv 6x6...")
            self.play(FadeIn(item2, shift=RIGHT*0.2), run_time=0.3)
            self.play(FadeIn(item3, shift=RIGHT*0.2), run_time=0.3)

        with self.voiceover(text="Vấn đề này ta sẽ bàn sâu ở video sau.") as tracker:
            self.update_subtitle("Vấn đề này ta sẽ bàn sâu ở video sau.")
            
            # 1. Mờ danh sách liệt kê đi để tập trung vào lời chào kết
            # (Giả sử danh sách của bạn tên là features_list hoặc tương đương)
            if 'features_list' in locals() or 'item1' in locals():
                # Nếu bạn dùng biến list_title, item1, item2 từ code trước:
                self.play(
                    VGroup(list_title, item1, item2).animate.set_opacity(0.1), 
                    run_time=0.4
                )
            
            # 2. Tạo dòng chữ vàng "TÌM HIỂU Ở VIDEO SAU"
            # Vị trí DOWN * 3.5 là ngay phía trên vùng phụ đề (vùng an toàn)
            final_cta = Text(
                "TÌM HIỂU Ở VIDEO SAU", 
                font="Segoe UI", 
                font_size=40, 
                weight=BOLD, 
                color=ACCENT
            ).move_to(DOWN * 3.5)

            # 3. Hiệu ứng xuất hiện dứt khoát
            self.play(
                FadeIn(final_cta, shift=UP * 0.3),
                Flash(final_cta, color=ACCENT, line_length=0.3), # Thêm hiệu ứng lóe sáng cho bắt mắt
                run_time=tracker.duration * 0.8
            )
            
            self.wait(1) # Chờ một chút trước khi kết thúc Scene

        self.finish_scene()