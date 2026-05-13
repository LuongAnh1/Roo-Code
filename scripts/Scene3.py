import sys
import os
import numpy as np
# [QUY TẮC 1: HACK PATH]
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from skills.fami_lib import * 

class Scene3_HoanThien(FaMIBaseScene):
    def construct(self):
        # ==========================================
        # 🎨 KHỞI TẠO TẤT CẢ ASSETS (PRE-LOADING)
        # ==========================================
        title = self.create_title("BƯỚC 1: BIẾN ĐỔI GIÁ TRỊ", "BIẾN ĐỔI MÀU SẮC")
        
        # --- ẢNH MÈO & LỚP PHỦ ---
        try:
            cat_img = ImageMobject("assets/cat.jpg").scale_to_fit_height(5)
        except:
            cat_img = Square(side_length=4, color=WHITE, fill_opacity=0.2)
        cat_img.move_to(ORIGIN).shift(DOWN * 0.5)

        color_filter = Rectangle(
            width=cat_img.width, height=cat_img.height,
            stroke_width=0, fill_color=RED, fill_opacity=0
        ).move_to(cat_img)

        # --- TOÁN HỌC: TẠO ẢNH XÁM ---
        px = cat_img.pixel_array.copy()
        gray_vals = (px[:,:,0]*0.299 + px[:,:,1]*0.587 + px[:,:,2]*0.114).astype(np.uint8)
        px[:,:,0] = px[:,:,1] = px[:,:,2] = gray_vals
        gray_cat = ImageMobject(px).scale_to_fit_height(5).move_to(cat_img)

        # --- MA TRẬN RGB (3 LỚP) ---
        def create_mat_layer(color, label):
            rect = Square(side_length=2.5, color=color, fill_opacity=0.6)
            txt = Text(label, font="Segoe UI", weight=BOLD).move_to(rect.get_corner(UR) + DL * 0.4)
            return VGroup(rect, txt)

        layer_r = create_mat_layer(RED, "R").shift(UR * 0.3)
        layer_g = create_mat_layer(GREEN, "G")
        layer_b = create_mat_layer(BLUE, "B").shift(DL * 0.3)
        rgb_stack = VGroup(layer_b, layer_g, layer_r).move_to(LEFT * 3 + UP * 0.8)

        # --- MA TRẬN GRAY & CÔNG THỨC ---
        gray_matrix = VGroup(
            Square(side_length=2.5, color=GRAY, fill_color=GRAY, fill_opacity=0.8),
            Text("Gray", font="Segoe UI", weight=BOLD).scale(0.8)
        ).move_to(RIGHT * 3 + UP * 0.8)

        formula = MathTex(r"Gray = ", r"0.299", r"R", r" + ", r"0.587", r"G", r" + ", r"0.114", r"B").scale(1.1).move_to(DOWN * 2.5)
        formula[2].set_color(RED); formula[5].set_color(GREEN); formula[8].set_color(BLUE)

        method_text = MarkupText(f"<span color='{FAMI_CYAN}'>Luminosity Method</span>", font="Segoe UI", font_size=25, weight=BOLD).next_to(formula, UP, buff=0.3)

        # Hàm tạo ma trận toán học sạch sẽ
        def create_math_matrix(val, color, title):
            data = [
                [r"\cdots", r"\cdots", r"\cdots"],
                [r"\cdots", str(val), r"\cdots"],
                [r"\cdots", r"\cdots", r"\cdots"]
            ]
            mat = Matrix(data, left_bracket="[", right_bracket="]")
            mat.set_color(WHITE) 
            mat.get_entries().set_color(GRAY_C) 
            
            # Làm nổi bật giá trị ở giữa
            center_val = mat.get_entries()[4]
            center_val.set_color(color).scale(1.3)
            
            lbl = Text(title, font="Segoe UI", weight=BOLD, font_size=24, color=color).next_to(mat, UP, buff=0.2)
            return VGroup(mat, lbl), center_val

        # 1. Khởi tạo 3 ma trận RGB
        grp_r, val_r = create_math_matrix(120, RED, "Red")
        grp_g, val_g = create_math_matrix(45, GREEN, "Green")
        grp_b, val_b = create_math_matrix(200, BLUE, "Blue")
        
        rgb_matrices = VGroup(grp_r, grp_g, grp_b).arrange(RIGHT, buff=0.4).scale(0.7).move_to(UP * 2.5)

        # 2. Khởi tạo Công thức tính toán
        calc_formula = MathTex(
            "120", r"\times 0.299 \ + ", 
            "45", r"\times 0.587 \\ + \ ", # <--- Thêm \\ vào đây để xuống dòng phần màu Xanh dương
            "200", r"\times 0.114 \ = \ ", 
            "85" 
        ).scale_to_fit_width(7.5).move_to(ORIGIN)
        
        calc_formula[0].set_color(RED)
        calc_formula[2].set_color(GREEN)
        calc_formula[4].set_color(BLUE)
        calc_formula[6].set_color(ACCENT)

        # 3. Khởi tạo Ma trận ảnh xám
        grp_gray, val_gray = create_math_matrix("?", ACCENT, "Grayscale Matrix")
        grp_gray.scale(0.8).move_to(DOWN * 2.5)

        stamp = VGroup(
            RoundedRectangle(width=4.5, height=1.5, corner_radius=0.2, color=DANGER, stroke_width=8),
            Text("HARDCODED", color=DANGER, weight=BOLD, font_size=40)
        ).rotate(15 * DEGREES).move_to(gray_matrix)

        # ==========================================
        # 🎬 ĐỒNG BỘ VOICEOVER
        # ==========================================

        # --- ĐOẠN 1: Đổi màu liên tục ---
        with self.voiceover(text="Thao tác đầu tiên: Biến đổi giá trị, hay cụ thể là biến đổi màu sắc.") as tracker:
            self.update_subtitle("Thao tác đầu tiên: Biến đổi giá trị...")
            self.play(Write(title), FadeIn(cat_img), run_time=1.0)
            self.wait(tracker.duration * 0.3)
            
            self.update_subtitle("hay cụ thể là biến đổi màu sắc.")
            # Hiệu ứng đổi màu nhanh 4 nhịp
            colors = [RED, BLUE, GREEN, RED, BLUE, GREEN, RED]
            for c in colors:
                self.play(color_filter.animate.set_fill(c, opacity=0.5), run_time=0.5)

        # --- ĐOẠN 2: So sánh Màu - Xám ---
        with self.voiceover(text="Cách cổ điển nhất là chuyển ảnh màu 3 chiều Red Green Blue về ảnh xám chỉ còn 1 kênh màu.") as tracker:
            self.update_subtitle("Cách cổ điển nhất là chuyển ảnh màu 3 chiều Red Green Blue...")
            
            # Chuẩn bị ảnh màu bên trái, ảnh xám bên phải
            cat_color_left = cat_img.copy().scale(0.6).to_edge(LEFT, buff=0.8).shift(DOWN*0.5)
            gray_cat.scale(0.6).to_edge(RIGHT, buff=0.8).shift(DOWN*0.5)
            arrow = Arrow(LEFT, RIGHT, color=FAMI_CYAN, buff=0).scale(0.5)
            arrow.move_to(ORIGIN).shift(DOWN * 0.5) # Ép mũi tên nằm ngang hàng Y với 2 ảnh

            self.play(
                FadeOut(color_filter),
                ReplacementTransform(cat_img, gray_cat),
                FadeIn(cat_color_left),
                run_time = 1.0
            )
            self.play(GrowArrow(arrow),run_time = 1.0)
            self.wait(tracker.duration * 0.3)
            self.update_subtitle("về ảnh xám chỉ còn 1 kênh màu.")
            

        # --- ĐOẠN 3: HIỆN DANH SÁCH PHƯƠNG PHÁP (PHONG CÁCH TECH CARD) ---
        with self.voiceover(text="Có nhiều phương pháp, nhưng phổ biến nhất là Luminosity Method.") as tracker:
            
            # 1. Hàm tạo Thẻ Công Nghệ (Tech Card)
            def create_tech_card(text, icon_color=WHITE, is_highlighted=False):
                # Khung thẻ bo tròn với viền mỏng sang trọng
                bg = RoundedRectangle(width=6.5, height=1.2, corner_radius=0.15, 
                                      stroke_width=2, stroke_color=WHITE, 
                                      fill_color=BLACK, fill_opacity=0.8)
                
                # Biểu tượng dấu chấm phát sáng
                dot = Dot(color=icon_color).shift(LEFT * 2.8)
                if is_highlighted:
                    dot.scale(1.5).set_glow_factor(1) # Chỉ dành cho bản Manim có hỗ trợ glow, nếu không sẽ tự bỏ qua
                
                label = Text(text, font="Segoe UI", font_size=32, weight=BOLD)
                label.next_to(dot, RIGHT, buff=0.4)
                
                card = VGroup(bg, dot, label)
                return card

            # 2. Khởi tạo 3 thẻ
            card1 = create_tech_card("Lightness Method", icon_color=GRAY)
            card2 = create_tech_card("Average Method", icon_color=GRAY)
            card3 = create_tech_card("Luminosity Method", icon_color=ACCENT, is_highlighted=True)
            
            # Tiêu đề danh sách kiểu Banner
            list_header = Text("ALGORITHM SELECTION", font="Segoe UI", font_size=32, color=FAMI_CYAN, weight=BOLD)
            underline = Line(LEFT, RIGHT, color=FAMI_CYAN, stroke_width=2).scale_to_fit_width(list_header.width)
            header_grp = VGroup(list_header, underline).arrange(DOWN, buff=0.1)

            methods_grp = VGroup(header_grp, card1, card2, card3).arrange(DOWN, buff=0.4).move_to(ORIGIN)

            # 3. ANIMATION: Xuất hiện kiểu Pop-in (Snappy < 1s)
            self.update_subtitle("Có nhiều phương pháp...")
            self.play(
                FadeOut(cat_color_left, scale=0.8),
                FadeOut(gray_cat, scale=0.8),
                FadeOut(arrow),
                FadeIn(header_grp, shift=UP*0.3),
                run_time=0.5
            )
            
            # Các thẻ bay vào lần lượt cực nhanh (Staggered entry)
            for i, card in enumerate([card1, card2, card3]):
                self.play(FadeIn(card, shift=RIGHT*0.5), run_time=0.3)

            # 4. HIGHLIGHT: Làm nổi bật thẻ 3
            self.update_subtitle("nhưng phổ biến nhất là Luminosity Method.")
            self.play(
                # Thẻ 3: Đổi viền sang vàng, phát sáng và hơi nhô lên
                card3[0].animate.set_stroke(ACCENT, width=5).set_fill(ACCENT, opacity=0.2),
                card3[2].animate.set_color(ACCENT),
                # Các thẻ khác: Mờ đi hoàn toàn
                card1.animate.set_opacity(0.2),
                card2.animate.set_opacity(0.2),
                header_grp.animate.set_opacity(0.2),
                run_time=min(1.0, tracker.duration * 0.3)
            )
            self.wait(0.5)


        # --- ĐOẠN 4: CHI TIẾT PHÉP NHÂN MA TRẬN (3D -> 2D) ---
        with self.voiceover(text="Cụ thể, ta sẽ ép dữ liệu của ảnh đang được biểu diễn dưới dạng mảng 3 chiều xuống thành ma trận 2 chiều...") as tracker:
            self.update_subtitle("Ép mảng 3 chiều xuống thành ma trận 2 chiều...")
            
            # --- BƯỚC 4.1: CHUẨN BỊ HIỆU ỨNG TRUNG GIAN ---
            # 1. FIX: Khởi tạo lại hoàn toàn ảnh màu gốc để tránh bị dính cache xám
            try:
                # scale_to_fit_height(5) là size gốc, sau đó scale(0.4) để thu nhỏ
                temp_cat_color = ImageMobject("assets/cat.jpg").scale_to_fit_height(5).scale(0.4).move_to(UP * 2.5)
            except:
                temp_cat_color = Square(side_length=2, color=WHITE, fill_opacity=0.2).move_to(UP * 2.5)

            # Ảnh xám thì ta cứ copy từ gray_cat vì bản chất nó đã là màu xám
            temp_cat_gray = gray_cat.copy().scale(0.4).move_to(DOWN * 2.5)

            # 2. Tạo trạng thái "Xếp chồng 3D" (Stacked) của 3 ma trận RGB
            stacked_b = grp_b.copy().move_to(UP * 2.5)
            stacked_g = grp_g.copy().move_to(UP * 2.5).shift(UR * 0.15)
            stacked_r = grp_r.copy().move_to(UP * 2.5).shift(UR * 0.3)
            stacked_group = VGroup(stacked_b, stacked_g, stacked_r)

            # --- BƯỚC 4.2: THỰC THI ANIMATION ---
            
            # Nhịp 1: Xóa các thẻ Tech Card đi, hiện 2 ảnh mèo (Màu ở trên, Xám ở dưới)
            self.play(
                FadeOut(header_grp), FadeOut(card1), FadeOut(card2), FadeOut(card3),
                FadeIn(temp_cat_color), FadeIn(temp_cat_gray),
                run_time=min(0.8, tracker.duration * 0.2)
            )
            self.wait(1.0)

            # Nhịp 2: Cross-fade (Ảnh biến thành Ma trận xếp chồng và Ma trận xám)
            self.play(
                FadeOut(temp_cat_color, scale=1.2),
                FadeIn(stacked_group, scale=0.8),
                
                FadeOut(temp_cat_gray, scale=1.2),
                FadeIn(grp_gray, scale=0.8),
                
                run_time=min(1.0, tracker.duration * 0.3)
            )
            self.wait(1.0)

            # Nhịp 3: "Bung" 3 ma trận xếp chồng ra thành 3 ma trận ngang
            self.play(
                ReplacementTransform(stacked_r, rgb_matrices[0]), 
                ReplacementTransform(stacked_g, rgb_matrices[1]), 
                ReplacementTransform(stacked_b, rgb_matrices[2]), 
                run_time=min(1.2, tracker.duration * 0.4),
                rate_func=rate_functions.ease_out_back
            )

        with self.voiceover(text="bằng cách nhân với các trọng số cố định, ta sẽ thu được ma trận xám tương ứng.") as tracker:
            self.update_subtitle("bằng cách nhân với các trọng số cố định, ta sẽ thu được ma trận xám tương ứng.")

            # 1. Các giá trị tâm nhấp nháy để báo hiệu bị trích xuất
            self.play(
                Indicate(val_r, scale_factor=1.5), 
                Indicate(val_g, scale_factor=1.5), 
                Indicate(val_b, scale_factor=1.5), 
                run_time=0.4
            )

            # 2. Tạo bản sao để bay đi
            fly_r, fly_g, fly_b = val_r.copy(), val_g.copy(), val_b.copy()

            # 3. Bay vào công thức và hiện các dấu nhân, cộng
            self.play(
                ReplacementTransform(fly_r, calc_formula[0]),
                ReplacementTransform(fly_g, calc_formula[2]),
                ReplacementTransform(fly_b, calc_formula[4]),
                Write(calc_formula[1]), 
                Write(calc_formula[3]), 
                Write(calc_formula[5]),
                run_time=min(1.5, tracker.duration * 0.6)
            )
            
            # 4. Hiện kết quả tính toán
            self.play(Write(calc_formula[6]), run_time=0.3)

        with self.voiceover(text="Các trọng số này được kỹ sư tính toán sẵn dựa trên độ nhạy của sinh học mắt người.") as tracker:
            self.update_subtitle("Các số này tính toán sẵn dựa trên sinh học mắt người.")
            
            # 5. Kết quả 85 bay tọt vào dấu "?" của ma trận Xám
            fly_result = calc_formula[6].copy()
            self.play(
                ReplacementTransform(fly_result, val_gray),
                run_time=0.8,
                path_arc=-PI/4 # Bay theo đường vòng cung nhẹ
            )
            
            # Làm khung ma trận xám lóe sáng lên báo hiệu hoàn thành
            self.play(Indicate(grp_gray[0], color=ACCENT), run_time=0.6)
            
            self.wait(tracker.get_remaining_duration())

        self.finish_scene()