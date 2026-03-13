import sys
import os
import math
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from skills.fami_lib import *

class Scene4_CTA(FaMIBaseScene):
    """
    Scene 4: Call to action (Câu hỏi cuối)
    - Voiceover: Câu hỏi cuối video...
    - Hình ảnh: Câu hỏi hiện trong khung, kèm dấu chấm hỏi và mũi tên chỉ xuống để Comment.
    """
    def construct(self):
        # 1. KHỞI TẠO ĐỐI TƯỢNG
        title = self.create_title("THỬ THÁCH", "DÀNH CHO BẠN")

        # Dấu hỏi chấm to
        question_mark = Text("?", font="Segoe UI", font_size=120, color=YELLOW, weight=BOLD)
        question_mark.next_to(title, DOWN, buff=0.8)

        # Khung câu hỏi
        question_text_1 = Text("Xử lý như thế nào", font="Segoe UI", font_size=40, color=WHITE)
        question_text_2 = MarkupText("nếu kẻ Spam viết <span fgcolor='#FF0000'>fr€€</span> ?", font="Segoe UI", font_size=45)
        
        q_group = VGroup(question_text_1, question_text_2).arrange(DOWN, buff=0.3)
        
        q_box = RoundedRectangle(corner_radius=0.3, color=FAMI_CYAN, fill_color=BLACK, fill_opacity=0.6)
        q_box.surround(q_group, buff=0.6)
        
        question_card = VGroup(q_box, q_group)
        question_card.next_to(question_mark, DOWN, buff=0.8)

        # Kêu gọi hành động (CTA)
        cta_text = Text("Để lại bình luận nhé!", font="Segoe UI", font_size=40, color=GREEN, weight=BOLD)
        cta_arrow = Arrow(start=UP, end=DOWN*1.5, color=GREEN, stroke_width=8, max_tip_length_to_length_ratio=0.2)
        
        cta_group = VGroup(cta_text, cta_arrow).arrange(DOWN, buff=0.3)
        cta_group.next_to(question_card, DOWN, buff=1.0)

        # Gom tất cả nội dung lại để kiểm soát layout
        main_content = VGroup(question_mark, question_card, cta_group)
        
        if main_content.width > 7.5:
            main_content.scale_to_fit_width(7.5)
            
        # Đảm bảo nội dung luôn nằm dưới title và ko lấn Subtitle
        main_content.next_to(title, DOWN, buff=0.5)
        
        if main_content.get_bottom()[1] < -3.5:
            main_content.scale_to_fit_height(title.get_bottom()[1] - (-3.5) - 0.5)
            main_content.next_to(title, DOWN, buff=0.5)

        # 2. KỊCH BẢN & ĐỒNG BỘ
        with self.voiceover(text="Câu hỏi cuối video dành cho bạn đó là phải xử lý như nào nếu kẻ Spam cố tình viết “free” thành “fr€€”?") as tracker:
            self.update_subtitle("Câu hỏi cuối video dành cho bạn đó là phải xử lý như nào nếu kẻ Spam cố tình viết “free” thành “fr€€”?")
            
            # Tiêu đề và Dấu hỏi (PopIn = scale out)
            self.play(
                Write(title),
                FadeIn(question_mark, scale=0.1),
                run_time=min(1.5, tracker.duration * 0.3)
            )
            
            self.play(Wiggle(question_mark), run_time=tracker.duration * 0.1)
            
            # Xuất hiện khung câu hỏi
            self.play(
                FadeIn(q_box),
                Write(question_text_1),
                run_time=tracker.duration * 0.2
            )
            self.play(
                Write(question_text_2),
                run_time=tracker.duration * 0.2
            )

        with self.voiceover(text="Nếu bạn biết câu trả lời, hãy comment phía dưới.") as tracker:
            self.update_subtitle("Nếu bạn biết câu trả lời, hãy comment phía dưới.")
            
            # Mũi tên đập xuống
            self.play(
                FadeIn(cta_text, shift=DOWN),
                GrowArrow(cta_arrow),
                run_time=tracker.duration * 0.5
            )
            
            # Hiệu ứng nảy mũi tên lặp lại
            self.play(cta_group.animate.shift(DOWN * 0.3), run_time=tracker.duration * 0.15, rate_func=there_and_back)
            self.play(cta_group.animate.shift(DOWN * 0.3), run_time=tracker.duration * 0.15, rate_func=there_and_back)

        # 3. KẾT THÚC
        self.wait(1)