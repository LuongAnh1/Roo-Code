import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from skills.fami_lib import *

class Scene1_Hook(FaMIBaseScene):
    def construct(self):
        # --- CONFIG from tiktok_layout_guide.md ---
        PRIMARY = "#00d4ff"
        ACCENT = "#fffa65"
        DANGER = "#ff4d4d"
        SUCCESS = "#00e676"
        
        VOICEOVER_TEXT = "Làm sao để phân loại Email Spam?"

        # --- OBJECTS (Layout-First Rule) ---
        
        # 1. Khai báo đối tượng
        title = self.create_title("PHÂN LOẠI EMAIL", "Sử dụng Định lý Bayes")
        email_icon = SVGMobject("assets/email_icon.svg").set(height=2.5)
        spam_text = Text("SPAM", font_size=45, color=DANGER, font="Segoe UI")
        normal_text = Text("NORMAL", font_size=45, color=SUCCESS, font="Segoe UI")

        # 2. Gom nhóm và Căn lề
        content_group = VGroup(normal_text, email_icon, spam_text).arrange(RIGHT, buff=0.7)
        
        # 3. Scale và Định vị cuối cùng
        content_group.scale_to_fit_width(8.0)
        content_group.move_to(ORIGIN)
        
        # 4. CUỐI CÙNG: Mới tạo Arrow
        spam_arrow = Arrow(email_icon.get_right(), spam_text.get_left(), buff=0.2, stroke_width=8, max_tip_length_to_length_ratio=0.15)
        normal_arrow = Arrow(email_icon.get_left(), normal_text.get_right(), buff=0.2, stroke_width=8, max_tip_length_to_length_ratio=0.15)

        # --- ANIMATION ---
        self.play(Write(title), run_time=min(1.5, 3 * 0.4)) # Assuming voiceover is ~3s
        
        with self.voiceover(text=VOICEOVER_TEXT) as tracker:
            self.update_subtitle(VOICEOVER_TEXT)

            # Animation được chia nhỏ và có nhịp điệu
            self.play(
                FadeIn(email_icon, scale=0.7),
                run_time=min(1.0, tracker.duration * 0.3)
            )
            
            self.play(
                LaggedStart(
                    GrowArrow(normal_arrow),
                    FadeIn(normal_text, shift=LEFT*0.2),
                    lag_ratio=0.5
                ),
                 run_time=min(1.2, tracker.duration * 0.35)
            )

            self.play(
                LaggedStart(
                    GrowArrow(spam_arrow),
                    FadeIn(spam_text, shift=RIGHT*0.2),
                    lag_ratio=0.5
                ),
                run_time=min(1.2, tracker.duration * 0.35)
            )

        # --- CLEANUP ---
        self.wait(1)
