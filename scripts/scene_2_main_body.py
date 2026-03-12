import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from skills.fami_lib import *

class Scene2_MainBody(FaMIBaseScene):
    def construct(self):
        # 1. KỊCH BẢN
        VO_1 = "Qua câu chuyện này, ta thấy rằng Định lý Bayes không chỉ là công thức lý thuyết mà còn được ứng dụng trực tiếp trong đời sống."
        VO_2 = "Về ưu điểm, đây không phải thuật toán tĩnh, nó có khả năng học từ dữ liệu mới, giảm thiểu việc đánh nhầm email quan trọng."
        VO_3 = "Về hạn chế thì Spam ngày nay ngày càng tinh vi với các biến tấu từ khóa như fr33 hoặc fr€."

        # 2. ĐỐI TƯỢNG (Khóa font Segoe UI và bóp Width)
        title = self.create_title("ƯU & NHƯỢC ĐIỂM", "của Lọc Spam Bayes")

        # Công thức
        formula = MathTex(r"P(A|B) = \frac{P(B|A) \cdot P(A)}{P(B)}", font_size=60).move_to(POS_CENTER)
        
        # Khối Ưu điểm (Xếp dọc)
        pros_title = Text("Ưu điểm:", font="Segoe UI", weight=BOLD, font_size=35, color=SUCCESS)
        advantage_1 = MarkupText("• <b>Học hỏi</b> từ dữ liệu mới", font="Segoe UI", font_size=30)
        advantage_2 = MarkupText("• <b>Tốc độ</b> xử lý nhanh", font="Segoe UI", font_size=30)
        pros_group = VGroup(pros_title, advantage_1, advantage_2).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        
        # Khối Nhược điểm (Xếp dọc)
        cons_title = Text("Nhược điểm:", font="Segoe UI", weight=BOLD, font_size=35, color=DANGER)
        cons_text = MarkupText(f'Biến tấu: <span color="{ACCENT}">fr33, f.r.e.e, fr€</span>', font="Segoe UI", font_size=30)
        cons_group = VGroup(cons_title, cons_text).arrange(DOWN, aligned_edge=LEFT, buff=0.2)

        # Toàn bộ nội dung xếp dọc thay vì ngang
        main_content = VGroup(pros_group, cons_group).arrange(DOWN, buff=0.8).move_to(POS_CENTER)
        if main_content.width > 7.5:
            main_content.scale_to_fit_width(7.5)

        # 3. ANIMATION (Tuân thủ quy tắc 80% thời gian)
        with self.voiceover(text=VO_1) as tracker:
            self.update_subtitle("Định lý Bayes ứng dụng trực tiếp trong đời sống.")
            self.play(Write(title), run_time=1.0)
            self.play(Write(formula), run_time=min(2.0, tracker.duration * 0.7))

        with self.voiceover(text=VO_2) as tracker:
            self.update_subtitle("Ưu điểm: Khả năng học hỏi và tốc độ cao.")
            # Biến hình từ công thức sang Ưu điểm
            self.play(ReplacementTransform(formula, pros_group.move_to(UP*1)), run_time=1.5)

        with self.voiceover(text=VO_3) as tracker:
            self.update_subtitle("Nhược điểm: Spam biến tấu từ khóa tinh vi.")
            # Hiện thêm nhược điểm ở phía dưới
            self.play(FadeIn(cons_group.next_to(pros_group, DOWN, buff=0.8), shift=UP*0.5), run_time=1.5)

        self.finish_scene()
