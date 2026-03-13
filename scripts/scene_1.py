import sys
import os
import math
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from skills.fami_lib import *

class Scene1_Hook(FaMIBaseScene):
    """
    Scene 1: Tình huống dẫn nhập.
    - Voiceover: Làm sao để phân loại Email Spam?
    - Visual: Icon Email, mũi tên chĩa ra 2 hộp Spam (Đỏ) và Normal (Xanh)
    """
    def construct(self):
        # 1. KHỞI TẠO ĐỐI TƯỢNG (Khai báo trước khi play)
        title = self.create_title("LÀM SAO ĐỂ PHÂN LOẠI", "EMAIL SPAM?")

        # Tải Icon Email (gmail.svg)
        email_icon = SVGMobject("assets/gmail.svg")
        email_icon.set_color(WHITE)
        email_icon.set_style(fill_color=WHITE, stroke_color=WHITE)
        email_icon.scale(1.5).move_to(UP * 1.5)

        # Mũi tên chẽ ra 2 hướng
        arrow_spam = Arrow(start=email_icon.get_bottom() + DOWN * 0.2, end=DOWN * 1.5 + LEFT * 2.5, color=RED)
        arrow_normal = Arrow(start=email_icon.get_bottom() + DOWN * 0.2, end=DOWN * 1.5 + RIGHT * 2.5, color=GREEN)

        # Nhãn Spam
        box_spam = RoundedRectangle(corner_radius=0.2, color=RED, height=1.2, width=3.0)
        box_spam.move_to(arrow_spam.get_end() + DOWN * 0.8)
        text_spam = Text("Spam", font="Segoe UI", font_size=40, color=WHITE).move_to(box_spam.get_center())
        spam_group = VGroup(box_spam, text_spam)

        # Nhãn Normal
        box_normal = RoundedRectangle(corner_radius=0.2, color=GREEN, height=1.2, width=3.0)
        box_normal.move_to(arrow_normal.get_end() + DOWN * 0.8)
        text_normal = Text("Normal", font="Segoe UI", font_size=40, color=WHITE).move_to(box_normal.get_center())
        normal_group = VGroup(box_normal, text_normal)

        # Đảm bảo nội dung không tràn
        main_content = VGroup(email_icon, arrow_spam, arrow_normal, spam_group, normal_group)
        if main_content.width > 7.5:
            main_content.scale_to_fit_width(7.5)
            # Khóa Y sau khi scale để không bị tụt
            main_content.move_to(UP * 0.5)

        # 2. KỊCH BẢN & ĐỒNG BỘ
        with self.voiceover(text="Làm sao để phân loại Email Spam?") as tracker:
            self.update_subtitle("Làm sao để phân loại Email Spam?")
            
            # Action 1: Write title and fade in email icon (40% duration)
            self.play(
                Write(title),
                FadeIn(email_icon, scale=0.5),
                run_time=min(1.5, tracker.duration * 0.4)
            )
            
            # Action 2: Grow arrows and drop down tags (40% duration)
            self.play(
                GrowArrow(arrow_spam),
                GrowArrow(arrow_normal),
                FadeIn(spam_group, shift=DOWN),
                FadeIn(normal_group, shift=DOWN),
                run_time=min(1.5, tracker.duration * 0.4)
            )

        # 3. KẾT THÚC
        self.wait(1)
