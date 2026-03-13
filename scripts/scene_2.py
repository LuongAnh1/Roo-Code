import sys
import os
import math
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from skills.fami_lib import *

class Scene2_MainBody(FaMIBaseScene):
    """
    Scene 2: Tổng kết kiến thức liên quan
    - Ưu điểm và nhược điểm
    - Biến tấu từ khóa spam
    """
    def construct(self):
        # 1. KHỞI TẠO ĐỐI TƯỢNG (Khai báo trước khi play)
        title = self.create_title("TỔNG KẾT", "KIẾN THỨC THỰC TIỄN")

        # --- ƯU ĐIỂM ---
        pros_title = Text("Ưu điểm:", font="Segoe UI", font_size=36, color=GREEN, weight=BOLD)
        pros_1 = Text("• Khả năng học từ dữ liệu mới", font="Segoe UI", font_size=32, color=WHITE)
        pros_2 = Text("• Giảm đánh nhầm email quan trọng", font="Segoe UI", font_size=32, color=WHITE)
        pros_3 = Text("• Tốc độ tính toán nhanh", font="Segoe UI", font_size=32, color=WHITE)
        
        pros_list = VGroup(pros_title, pros_1, pros_2, pros_3).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        pros_box = RoundedRectangle(corner_radius=0.2, color=GREEN, fill_color=BLACK, fill_opacity=0.5)
        pros_box.surround(pros_list, buff=0.5)
        pros_group = VGroup(pros_box, pros_list)

        # --- NHƯỢC ĐIỂM ---
        cons_title = Text("Nhược điểm:", font="Segoe UI", font_size=36, color=RED, weight=BOLD)
        cons_1 = Text("• Spam ngày càng tinh vi", font="Segoe UI", font_size=32, color=WHITE)
        cons_2 = Text("• Dễ bị qua mặt bằng biến tấu từ khóa", font="Segoe UI", font_size=32, color=WHITE)
        
        cons_list = VGroup(cons_title, cons_1, cons_2).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        cons_box = RoundedRectangle(corner_radius=0.2, color=RED, fill_color=BLACK, fill_opacity=0.5)
        cons_box.surround(cons_list, buff=0.5)
        cons_group = VGroup(cons_box, cons_list)

        # Sắp xếp tổng thể
        cards_group = VGroup(pros_group, cons_group).arrange(DOWN, buff=0.5)
        
        # --- ICON EMAIL ---
        email_icon = SVGMobject("assets/gmail.svg")
        email_icon.set_color(WHITE)
        email_icon.set_style(fill_color=WHITE, stroke_color=WHITE)
        email_icon.set_width(1.5)

        # --- TEXT BIẾN TẤU ---
        spam_text_1 = Text('"free"', font="Consolas", font_size=50, color=YELLOW)
        spam_text_2 = Text('"fr33"', font="Consolas", font_size=50, color=ORANGE)
        spam_text_3 = Text('"f.r.e.e"', font="Consolas", font_size=50, color=RED_B)
        spam_text_4 = Text('"fr€€"', font="Consolas", font_size=50, color=RED)

        spam_texts = [spam_text_1, spam_text_2, spam_text_3, spam_text_4]
        
        # Gom tất cả vào 1 group chính để scale chung
        main_content = VGroup(email_icon, cards_group, spam_text_1).arrange(DOWN, buff=0.5)
        
        # Đảm bảo không tràn viền ngang 7.5
        if main_content.width > 7.5:
            main_content.scale_to_fit_width(7.5)
            
        # Đảm bảo nằm dưới Title và không bị chèn vào Subtitle
        main_content.next_to(title, DOWN, buff=0.5)
        
        # Ép chiều cao nếu quá dài để không lấn xuống Subtitle (Y = -4.5)
        if main_content.get_bottom()[1] < -3.5:
            main_content.scale_to_fit_height(title.get_bottom()[1] - (-3.5) - 0.5)
            main_content.next_to(title, DOWN, buff=0.5)

        # Cập nhật vị trí các text biến tấu khác bám theo text 1
        for t in spam_texts[1:]:
            t.move_to(spam_text_1.get_center())
            t.match_height(spam_text_1)

        # 2. KỊCH BẢN & ĐỒNG BỘ
        
        # Phần 1: Giới thiệu
        with self.voiceover(text="Qua câu chuyện này, ta thấy rằng Định lý Bayes không chỉ là công thức lý thuyết mà còn được ứng dụng trực tiếp trong đời sống.") as tracker:
            self.update_subtitle("Qua câu chuyện này, ta thấy rằng Định lý Bayes không chỉ là công thức lý thuyết mà còn được ứng dụng trực tiếp trong đời sống.")
            self.play(Write(title), FadeIn(email_icon, shift=UP), run_time=min(1.5, tracker.duration * 0.4))
            
        # Phần 2: Ưu điểm
        with self.voiceover(text="Về ưu điểm, đây không phải thuật toán tĩnh, nó có khả năng học từ dữ liệu mới, giảm thiểu việc đánh nhầm email quan trọng thành Spam cùng tốc độ tính toán nhanh") as tracker:
            self.update_subtitle("Về ưu điểm, đây không phải thuật toán tĩnh, nó có khả năng học từ dữ liệu mới, giảm thiểu việc đánh nhầm email quan trọng thành Spam cùng tốc độ tính toán nhanh")
            
            # Fade in box and title
            self.play(FadeIn(pros_box), Write(pros_title), run_time=tracker.duration * 0.15)
            # Write points sequentially
            self.play(Write(pros_1), run_time=tracker.duration * 0.2)
            self.play(Write(pros_2), run_time=tracker.duration * 0.2)
            self.play(Write(pros_3), run_time=tracker.duration * 0.2)
            
        # Phần 3: Hạn chế
        with self.voiceover(text="Về hạn chế thì Spam ngày nay ngày càng tinh vi. Thay vì viết “free”, kẻ gửi có thể viết “fr33”; “f.r.e.e”; “fr€€” làm hệ thống dựa trên từ khóa khó nhận diện.") as tracker:
            self.update_subtitle("Về hạn chế thì Spam ngày nay ngày càng tinh vi. Thay vì viết “free”, kẻ gửi có thể viết “fr33”; “f.r.e.e”; “fr€€” làm hệ thống dựa trên từ khóa khó nhận diện.")
            
            # Cân đối thời gian cho đoạn thoại dài này (giả sử mất khoảng 8s)
            # Hiện hộp nhược điểm (20%)
            self.play(
                FadeIn(cons_box), 
                Write(cons_title), 
                Write(cons_1), 
                Write(cons_2),
                run_time=tracker.duration * 0.2
            )
            
            # Trình diễn text biến tấu (mỗi từ chiếm 10-15%)
            self.play(FadeIn(spam_text_1, shift=UP), run_time=tracker.duration * 0.1)
            self.play(ReplacementTransform(spam_text_1, spam_text_2), run_time=tracker.duration * 0.15)
            self.play(ReplacementTransform(spam_text_2, spam_text_3), run_time=tracker.duration * 0.15)
            self.play(ReplacementTransform(spam_text_3, spam_text_4), run_time=tracker.duration * 0.15)
            
            # Wiggle text cuối để nhấn mạnh sự nguy hiểm
            self.play(Wiggle(spam_text_4), run_time=tracker.duration * 0.1)

        # 3. KẾT THÚC
        self.wait(1)