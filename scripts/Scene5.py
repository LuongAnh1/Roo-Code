import sys
import os
import numpy as np
# [QUY TẮC 1: HACK PATH]
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from skills.fami_lib import *

class Scene5_BiendoiKhongGian_Fixed(FaMIBaseScene):
    def construct(self):
        # ==========================================
        # 🎨 KHỞI TẠO ASSETS (BỐ CỤC MỚI)
        # ==========================================
        title = self.create_title("BƯỚC 2: BIẾN ĐỔI KHÔNG GIAN", "AFFINE TRANSFORMATION")
        self.add(title)

        # 1. HỆ TRỤC TỌA ĐỘ
        axes = Axes(
            x_range=[-6, 6, 1], y_range=[-2, 2, 1],
            axis_config={"color": GRAY, "stroke_width": 2}
        ).scale(0.8).move_to(UP * 2.0) 
        
        try:
            subject_img = ImageMobject("assets/cat.jpg").scale_to_fit_width(1.5)
        except:
            subject_img = Rectangle(width=1.5, height=1.5, color=FAMI_CYAN, fill_opacity=0.8)
        
        # Đưa ảnh về chính tâm tọa độ (0,0)
        subject_img.move_to(axes.c2p(0, 0))

        # ĐIỀU CHỈNH CHẤM TỌA ĐỘ
        coord_dot = Dot(subject_img.get_corner(UR), color=ACCENT)
        # Điều chỉnh nhẹ vị trí chữ để không bị chèn vào ảnh khi xoay
        coord_label = MathTex(r"(x, y)", font_size=28, color=ACCENT).next_to(coord_dot, UR, buff=0.15)
        
        target_point = VGroup(coord_dot, coord_label)

        # ⭐ SỬA LỖI Ở ĐÂY: Gom Ảnh và Điểm (x,y) vào chung 1 Group
        # BỎ HẲN add_updater. Từ nay ta sẽ animate biến 'grouped_subject'
        grouped_subject = Group(subject_img, target_point)

        # 2. CÁC CÔNG THỨC TOÁN HỌC
        form_2x2 = MathTex(
            r"\begin{bmatrix} a & b \\ c & d \end{bmatrix}", r"\times", r"\begin{bmatrix} x \\ y \end{bmatrix}"
        ).scale(1.2).move_to(DOWN * 2.0)
        form_2x2[0].set_color(FAMI_CYAN) 
        form_2x2[2].set_color(ACCENT)    

        form_error = MathTex(
            r"\begin{bmatrix} a & b \\ c & d \end{bmatrix}", r"\times", r"\begin{bmatrix} x \\ y \end{bmatrix}",
            r"+", r"\begin{bmatrix} t_x \\ t_y \end{bmatrix}"
        ).scale(1.2).move_to(DOWN * 2.0)
        form_error[0].set_color(FAMI_CYAN)
        form_error[2].set_color(ACCENT)
        form_error[3].set_color(DANGER) 
        form_error[4].set_color(DANGER) 

        form_affine = MathTex(
            r"\begin{bmatrix} a & b &", r"t_x", r"\\ c & d &", r"t_y", r"\\ 0 & 0 &", r"1", r"\end{bmatrix}", 
            r"\times", 
            r"\begin{bmatrix} x \\ y \\ 1 \end{bmatrix}"
        ).scale(1.2).move_to(DOWN * 2.0)
        form_affine[0:7].set_color(SUCCESS) 
        form_affine[8].set_color(ACCENT)    

        # ==========================================
        # 🎬 ĐỒNG BỘ VOICEOVER
        # ==========================================

        # --- NHỊP 1: TỌA ĐỘ PIXEL ---
        with self.voiceover(text="Thao tác thứ hai: Biến đổi không gian. Như đã nói, bản chất bức ảnh là một ma trận, và mỗi điểm ảnh đều có một tọa độ (x, y) riêng biệt.") as tracker:
            self.update_subtitle("Thao tác thứ hai: Biến đổi không gian")
            self.play(Create(axes), run_time=0.6)
            # Hiển thị toàn bộ group ra thay vì FadeIn từng cái
            self.play(FadeIn(grouped_subject), run_time=0.6)
            self.wait(tracker.duration * 0.25)
            self.update_subtitle("Như đã nói, bản chất bức ảnh là một ma trận...")
            self.wait(tracker.duration * 0.3)
            self.update_subtitle("và mỗi điểm ảnh đều có một tọa độ (x, y) riêng biệt")
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(text="Để thay đổi hình dáng hay vị trí của ảnh, chúng ta chính là đang tác động vào những tọa độ này.") as tracker:
            self.update_subtitle("Để thay đổi hình dáng hay vị trí của ảnh...")
            self.play(Indicate(coord_label, color=WHITE, scale_factor=1.5), run_time=tracker.duration * 0.4)
            self.update_subtitle("chúng ta chính là đang tác động vào những tọa độ này")

        # --- NHỊP 2: PHÉP NHÂN 2x2 ---
        with self.voiceover(text="Hãy bắt đầu từ cơ bản: Trong không gian 2D, khi nhân tọa độ điểm ảnh với một ma trận 2x2,") as tracker:
            self.update_subtitle("Hãy bắt đầu từ cơ bản: Trong không gian 2D...")
            self.play(Write(form_2x2), run_time=min(1.0, tracker.duration * 0.5))
            self.update_subtitle("khi nhân tọa độ điểm ảnh với một ma trận 2x2...")

        # --- NHỊP 3: THỰC THI BIẾN ĐỔI ---
        # Copy lại trạng thái gốc nếu cần dùng sau này
        subject_original = grouped_subject.copy()
        
        with self.voiceover(text="ta có thể làm được 3 việc: Co giãn, Xoay và làm Biến dạng hình ảnh.") as tracker:
            self.update_subtitle("ta làm được: Co giãn, Xoay và làm Biến dạng.")
            
            # 1. CO GIÃN (Scale) - Áp dụng cho grouped_subject
            self.play(
                grouped_subject.animate.scale(1.5),
                run_time=tracker.duration * 0.3
            )
            
            # 2. XOAY (Rotate) - Dùng .animate.rotate thay vì Rotate() để mượt hơn với Group
            self.play(
                grouped_subject.animate.rotate(30 * DEGREES),
                run_time=tracker.duration * 0.3
            )
            
            # 3. BIẾN DẠNG (Shear) - Áp dụng cho grouped_subject
            self.play(
                grouped_subject.animate.stretch(1.2, dim=0).stretch(0.8, dim=1),
                run_time=tracker.duration * 0.4
            )
            
        # Không cần clear_updaters nữa vì ta đã xóa nó ở trên
            
            
        # # --- NHỊP 3: LỖI PHÉP CỘNG ---
        # with self.voiceover(text="Nhưng có một vấn đề: Phép nhân ma trận 2x2 không thể giúp ta di chuyển bức ảnh đi chỗ khác.") as tracker:
        #     self.update_subtitle("Vấn đề: Phép nhân 2x2 KHÔNG THỂ di chuyển bức ảnh.")
        #     self.play(Wiggle(form_2x2, rotation_angle=0.04), run_time=min(1.0, tracker.duration * 0.8))

        # with self.voiceover(text="Để dịch chuyển, ta buộc phải dùng phép CỘNG với một Vector độ dời t x, t y.") as tracker:
        #     self.update_subtitle("Để dịch chuyển, buộc phải CỘNG với Vector dời tx, ty.")
        #     self.play(ReplacementTransform(form_2x2, form_error), run_time=min(1.0, tracker.duration * 0.5))
        #     self.play(Indicate(form_error[3], color=DANGER, scale_factor=2), run_time=0.5) 

        # # --- NHỊP 4: GIẢI PHÁP 3X3 ---
        # with self.voiceover(text="Để đưa tất cả về duy nhất một phép nhân cho gọn nhẹ, các nhà toán học dùng một mẹo: Thêm số 1 vào cuối tọa độ.") as tracker:
        #     self.update_subtitle("Mẹo: Thêm số 1 vào cuối tọa độ để gộp thành 1 phép nhân.")
        #     self.play(ReplacementTransform(form_error, form_affine), run_time=min(1.5, tracker.duration * 0.8))

        # with self.voiceover(text="Lúc này, phép cộng tịnh tiến ban nãy đã được 'nhốt' gọn vào cột thứ 3 của một ma trận 3x3 mới.") as tracker:
        #     self.update_subtitle("Phép tịnh tiến được 'nhốt' gọn vào cột 3 của ma trận 3x3.")
            
        #     # FIX LỖI KHOANH VÙNG CỘT 3: 
        #     # Gom chính xác các phần tử t_x, t_y, 1 (Index 1, 3, 5 trong form_affine)
        #     col_3_group = VGroup(form_affine[1], form_affine[3], form_affine[5])
        #     highlight_col = SurroundingRectangle(col_3_group, color=ACCENT, buff=0.15, stroke_width=3)
            
        #     self.play(Create(highlight_col), run_time=tracker.duration * 0.4)
        #     self.play(FadeOut(highlight_col), run_time=0.3)

        # # --- NHỊP 5: KẾT LUẬN & DATA AUGMENTATION ---
        # with self.voiceover(text="Và đây chính là Ma trận biến đổi A phin. Một ma trận chứa đựng sức mạnh tổng hợp: Vừa xoay, co giãn, vừa dịch chuyển chỉ bằng một phép nhân.") as tracker:
        #     self.update_subtitle("Đó là Ma trận Affine: Xoay, co giãn, dịch chuyển bằng 1 phép nhân.")
            
        #     lbl_affine = Text("AFFINE MATRIX", font="Segoe UI", font_size=24, color=SUCCESS, weight=BOLD).next_to(form_affine, UP, buff=0.2)
        #     self.play(FadeIn(lbl_affine, shift=DOWN*0.2), run_time=0.5)

        #     # Chuyển động Affine: Bay về góc dưới bên trái của ĐỒ THỊ
        #     self.play(
        #         subject.animate.move_to(axes.c2p(-3, -1)).scale(0.6).rotate(-60 * DEGREES),
        #         target_point.animate.move_to(axes.c2p(-3, -1.5) + UP*0.8),
        #         run_time=min(2.0, tracker.duration * 0.5)
        #     )

        # with self.voiceover(text="Đây là trái tim của việc sinh ra dữ liệu mới (Data Augmentation) trong AI.") as tracker:
        #     self.update_subtitle("Đây là cốt lõi của việc Tăng cường dữ liệu (Data Augmentation).")
            
        #     # CHỮ DATA AUGMENTATION ĐƯỢC ĐẨY LÊN SÁT TIÊU ĐỀ
        #     aug_title = Text("DATA AUGMENTATION", font="Segoe UI", font_size=32, color = YELLOW, weight=BOLD)
        #     aug_title.next_to(title, DOWN, buff=0.3)
        #     self.play(FadeIn(aug_title, shift=UP*0.2), FadeOut(target_point), run_time=0.4)

        #     # ⭐ TẠO CLONES TỬ BẢN COPY SẠCH (KHÔNG BỊ HỎI)
        #     # Sử dụng subject_original thay vì subject (cái bị biến dạng)
        #     clone1 = subject_original.copy().move_to(axes.c2p(3, 1.5)).scale(1.2).rotate(30*DEGREES)
        #     clone2 = subject_original.copy().move_to(axes.c2p(-3, 1.5)).scale(0.8)
        #     clone3 = subject_original.copy().move_to(axes.c2p(4, -1)).rotate(-45*DEGREES)
        #     clone4 = subject_original.copy().move_to(axes.c2p(0, 0)).scale(1.3)

        #     self.play(
        #         FadeIn(clone1, shift=UR), FadeIn(clone2, shift=UL),
        #         FadeIn(clone3, shift=DR), FadeIn(clone4, shift=UP),
        #         run_time=tracker.duration * 0.6
        #     )
        #     self.wait(1)

        self.finish_scene()