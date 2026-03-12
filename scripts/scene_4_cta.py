import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from skills.fami_lib import *

class Scene4_CTA(FaMIBaseScene):
    def construct(self):
        # 1. KỊCH BẢN
        VO_TEXT = "Câu hỏi cuối video dành cho bạn đó là phải xử lý như nào nếu kẻ Spam cố tình viết “free” thành “fr€€”"

        # 2. ĐỐI TƯỢNG
        title = self.create_title("CÂU HỎI CHO BẠN")

        question_mark = Text("?", font_size=160, color=ACCENT, weight=BOLD)
        glow = question_mark.copy().set_stroke(color=ACCENT, width=20, opacity=0.3).set_fill(opacity=0)
        q_mark_group = VGroup(question_mark, glow)

        # Sửa lỗi: Sử dụng ORIGIN thay vì CENTER và đảm bảo chuỗi là raw hoặc chuẩn Unicode
        line1 = MarkupText('Phải xử lý thế nào nếu kẻ Spam viết "free"', font="Segoe UI", font_size=32)
        line2 = MarkupText(f'thành <span color="{ACCENT}">"fr€€"</span> như thế nào?', font="Segoe UI", font_size=32)
        
        # aligned_edge=ORIGIN là cách viết chuẩn để căn giữa các đối tượng trong VGroup
        question_text = VGroup(line1, line2).arrange(DOWN, buff=0.3, aligned_edge=ORIGIN)
        question_text.next_to(self.logo, DOWN, buff=1.0)
        
        if question_text.width > 8.0:
            question_text.scale_to_fit_width(8.0)

        cta_text = Text("Comment câu trả lời của bạn!", font="Segoe UI", font_size=32, color=FAMI_CYAN)

        # Bố cục dọc
        main_content = VGroup(q_mark_group, question_text).arrange(DOWN, buff=0.6)
        VGroup(main_content, cta_text).arrange(DOWN, buff=1.0).move_to(POS_CENTER)
        
        # 3. ANIMATION
        self.play(Write(title))
        
        with self.voiceover(text=VO_TEXT) as tracker:
            self.update_subtitle(VO_TEXT)

            self.play(
                FadeIn(q_mark_group, scale=0.5, shift=UP*0.5, rate_func=rate_functions.ease_out_back),
                run_time = tracker.duration * 0.3
            )
            self.play(
                Write(question_text),
                run_time=tracker.duration * 0.5
            )
            self.play(
                FadeIn(cta_text, shift=UP*0.2),
                run_time=tracker.duration * 0.2
            )

        self.finish_scene()
