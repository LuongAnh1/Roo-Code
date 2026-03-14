import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from skills.fami_lib import *
from skills.fami_assets_helper import *
from skills.fami_effects import *

class Scene1_Hook(FaMIBaseScene):
    def construct(self):
        title = self.create_title("PHÂN LOẠI", "EMAIL SPAM")
        
        # ==========================================
        # 🎨 VÙNG SÁNG TẠO (CREATIVE ZONE)
        # ==========================================
        # Icon Email ở trung tâm
        email_icon = SVGMobject("assets/gmail.svg")
        email_icon.set_height(2.0)
        email_icon.move_to(UP * 1.0)
        email_icon.set_stroke(width=6)
        apply_fami_gradient(email_icon)
        
        # Nhánh trái (Spam)
        spam_arrow = Arrow(
            start=email_icon.get_bottom() + LEFT * 0.2 + DOWN * 0.2,
            end=LEFT * 2.0 + DOWN * 1.0,
            color=DANGER,
            stroke_width=6,
            tip_length=0.3
        )
        spam_box = RoundedRectangle(height=1.5, width=3.0, color=DANGER, fill_opacity=0.2).move_to(LEFT * 2.0 + DOWN * 2.0)
        spam_text = Text("SPAM", font="Segoe UI", font_size=40, color=DANGER, weight=BOLD).move_to(spam_box)
        spam_group = VGroup(spam_box, spam_text)

        # Nhánh phải (Normal)
        normal_arrow = Arrow(
            start=email_icon.get_bottom() + RIGHT * 0.2 + DOWN * 0.2,
            end=RIGHT * 2.0 + DOWN * 1.0,
            color=SUCCESS,
            stroke_width=6,
            tip_length=0.3
        )
        normal_box = RoundedRectangle(height=1.5, width=3.0, color=SUCCESS, fill_opacity=0.2).move_to(RIGHT * 2.0 + DOWN * 2.0)
        normal_text = Text("NORMAL", font="Segoe UI", font_size=40, color=SUCCESS, weight=BOLD).move_to(normal_box)
        normal_group = VGroup(normal_box, normal_text)
        
        # ==========================================
        # 🎬 ĐỒNG BỘ VOICEOVER CHUẨN
        # ==========================================
        with self.voiceover(text="Làm sao để phân loại Email Spam?") as tracker:
            self.update_subtitle("Làm sao để phân loại Email Spam?")
            
            # Khóa run_time tối đa 1.5s
            self.play(Write(title), run_time=min(1.0, tracker.duration * 0.3))
            
            pop_in_anim, pop_in_rate = skill_pop_in(email_icon)
            self.play(pop_in_anim, rate_func=pop_in_rate, run_time=min(0.5, tracker.duration * 0.2))
            
            # Hai mũi tên chĩa ra
            self.play(
                GrowArrow(spam_arrow),
                GrowArrow(normal_arrow),
                run_time=min(0.5, tracker.duration * 0.1)
            )
            
            # Hai hộp hiện ra
            self.play(
                FadeIn(spam_group, shift=DOWN*0.5),
                FadeIn(normal_group, shift=DOWN*0.5),
                run_time=min(0.5, tracker.duration * 0.2)
            )
            
        self.finish_scene()
