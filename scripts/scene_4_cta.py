import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from skills.fami_lib import *
from skills.fami_assets_helper import *
from skills.fami_effects import *

class Scene4_CTA(FaMIBaseScene):
    def construct(self):
        title = self.create_title("CÂU HỎI", "CHO BẠN")

        # ==========================================
        # 🎨 VÙNG SÁNG TẠO CÂU HỎI
        # ==========================================
        free_text = Text('"free"', font="Segoe UI", font_size=70, color=SUCCESS, weight=BOLD)
        free_text.move_to(UP * 1.5)
        
        spam_text = Text('"fr€€"', font="Segoe UI", font_size=80, color=DANGER, weight=BOLD)
        spam_text.move_to(UP * 1.5)
        
        question_mark = Text("?", font="Segoe UI", font_size=120, color=ACCENT, weight=BOLD)
        question_mark.move_to(DOWN * 0.2)

        # ==========================================
        # 🔒 VÙNG KHÓA CỨNG CTA
        # ==========================================
        cta_box = RoundedRectangle(height=1.0, width=6.5, color=FAMI_CYAN, fill_color=FAMI_BLUE, fill_opacity=0.3)
        cta_text = Text("Comment câu trả lời của bạn!", font="Segoe UI", font_size=32)
        apply_fami_gradient(cta_text)
        cta_text.move_to(cta_box)
        cta_group = VGroup(cta_box, cta_text).move_to(DOWN * 2.8)

        arrow = Arrow(cta_group.get_bottom() + DOWN*0.1, cta_group.get_bottom() + DOWN * 1.2, color=SUCCESS, stroke_width=8, tip_length=0.4)

        # ==========================================
        # 🎬 ĐỒNG BỘ VOICEOVER CHUẨN
        # ==========================================
        with self.voiceover(text="Câu hỏi cuối video dành cho bạn đó là phải xử lý như nào nếu kẻ Spam cố tình viết “free” thành “fr€€”?") as tracker:
            self.update_subtitle('Xử lý như nào nếu kẻ Spam cố tình viết "free" thành "fr€€"?')
            
            self.play(Write(title), run_time=min(1.0, tracker.duration * 0.2))
            
            self.play(FadeIn(free_text, shift=DOWN*0.5), run_time=min(0.8, tracker.duration * 0.2))
            
            # Biến hình
            self.play(ReplacementTransform(free_text, spam_text), run_time=min(0.8, tracker.duration * 0.2))
            
            # Dấu chấm hỏi nảy lên
            pop_in_anim, pop_in_rate = skill_pop_in(question_mark)
            self.play(pop_in_anim, rate_func=pop_in_rate, run_time=min(0.5, tracker.duration * 0.2))

        with self.voiceover(text="Nếu bạn biết câu trả lời, hãy comment phía dưới.") as tracker:
            self.update_subtitle("Nếu bạn biết câu trả lời, hãy comment phía dưới.")
            
            # Nút CTA hiện lên
            self.play(FadeIn(cta_group, shift=UP*0.5), GrowArrow(arrow), run_time=min(1.0, tracker.duration * 0.5))

        self.finish_scene()
