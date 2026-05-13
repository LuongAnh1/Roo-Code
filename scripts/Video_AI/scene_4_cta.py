import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from skills.fami_lib import *
from skills.fami_effects import *

class Scene4_CTA(FaMIBaseScene):
    def construct(self):
        title = self.create_title("ĐÓN XEM", "TẬP SAU")
        
        # ==========================================
        # 🎨 VÙNG SÁNG TẠO CÂU HỎI (CREATIVE QUESTION ZONE)
        # ==========================================
        # Tạo Ma trận lớn (5x5) đại diện cho ảnh
        grid = VGroup(*[
            Square(side_length=0.7, stroke_color=GRAY_D, stroke_width=2, fill_opacity=0.2, fill_color=FAMI_BLUE)
            for _ in range(25)
        ]).arrange_in_grid(5, 5, buff=0)
        
        # Tạo Ma trận trượt (Kernel 3x3) đại diện cho Convolution
        kernel = VGroup(*[
            Square(side_length=0.7, stroke_color=ACCENT, stroke_width=5, fill_opacity=0.3, fill_color=YELLOW)
            for _ in range(9)
        ]).arrange_in_grid(3, 3, buff=0)
        
        grid_group = VGroup(grid, kernel)
        grid_group.move_to(UP * 1.5)
        
        # Đặt kernel ở góc trên cùng bên trái của grid (Căn chuẩn 3x3 nằm lọt lòng 5x5)
        kernel.move_to(grid.get_center() + LEFT*0.7 + UP*0.7)
        
        # Tạo text chú thích cho phần này
        caption = Text("Convolutional Layer", font="Segoe UI", font_size=36, weight=BOLD, color=FAMI_CYAN)
        caption.next_to(grid, DOWN, buff=0.5)

        # ==========================================
        # 🔒 VÙNG KHÓA CỨNG CTA (LOCKED CTA ZONE)
        # ==========================================
        cta_box = RoundedRectangle(height=1.0, width=6.5, corner_radius=0.15, color=FAMI_CYAN)
        cta_text = Text("Comment nếu bạn sẵn sàng!", font="Segoe UI", font_size=30, weight=BOLD).move_to(cta_box)
        cta_group = VGroup(cta_box, cta_text).move_to(DOWN * 2.8)
        apply_fami_gradient(cta_box)
        
        # Mũi tên chỉ xuống nút comment
        arrow = Arrow(cta_group.get_top() + UP*0.6, cta_group.get_top(), color=SUCCESS, stroke_width=6)

        # ==========================================
        # ĐỒNG BỘ VOICEOVER
        # ==========================================
        with self.voiceover(text="Dữ liệu đã xong, tập sau chúng ta sẽ giải mã Convolutional Layer, nơi phép Nhân ma trận vận hành trên cấu trúc trượt của Morphology để tạo nên thị giác cho AI nhé. Hẹn gặp lại bạn ở video tiếp theo!") as tracker:
            self.update_subtitle("Dữ liệu đã xong, tập sau chúng ta sẽ giải mã Convolutional Layer...")
            
            # Hiện tiêu đề và khối
            self.play(
                Write(title), 
                FadeIn(grid), 
                FadeIn(caption), 
                run_time=min(1.0, tracker.duration * 0.15)
            )
            
            # Hiện kernel chớp nhoáng
            self.play(FadeIn(kernel, scale=1.5), run_time=min(0.5, tracker.duration * 0.1))
            
            # Hiệu ứng trượt kernel (Convolution)
            # Trượt sang phải 1 ô
            self.play(kernel.animate.shift(RIGHT * 0.7), run_time=min(0.5, tracker.duration * 0.15))
            # Trượt sang phải 1 ô nữa (Hết viền)
            self.play(kernel.animate.shift(RIGHT * 0.7), run_time=min(0.5, tracker.duration * 0.15))
            # Trượt xuống 1 ô, quay lại trái
            self.play(kernel.animate.shift(DOWN * 0.7 + LEFT * 1.4), run_time=min(0.6, tracker.duration * 0.15))
            # Trượt sang phải
            self.play(kernel.animate.shift(RIGHT * 0.7), run_time=min(0.5, tracker.duration * 0.15))
            
           

            # Hiện nút CTA khóa cứng ở đáy
            self.play(
                FadeIn(cta_group, shift=UP*0.5), 
                GrowArrow(arrow), 
                run_time= 1.5
            )
            self.update_subtitle("nơi phép Nhân ma trận vận hành trên cấu trúc trượt của...")
            self.wait(tracker.duration * 0.3)
            self.update_subtitle("Morphology để tạo nên thị giác cho AI nhé!")
            self.wait(tracker.duration * 0.3)
            self.update_subtitle("Hẹn gặp lại bạn ở video tiếp theo!")


        self.finish_scene()
