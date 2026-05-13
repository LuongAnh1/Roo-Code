import sys
import os
import random
import numpy as np

# Fix path to load skills/fami_lib
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from skills.fami_lib import *

class Scene1_Hook(FaMIBaseScene):
    def construct(self):
        title = self.create_title("GÓC NHÌN", "CỦA AI")
        
        # ==========================================
        # 🎨 VÙNG SÁNG TẠO (CREATIVE ZONE)
        # ==========================================
        try:
            cat_img = ImageMobject("assets/cat.jpg")
            cat_img.scale_to_fit_width(6.5)
        except Exception as e:
            # Fallback if cat.jpg doesn't exist
            cat_img = Rectangle(width=6.5, height=6.5, color=WHITE)
            text_fallback = Text("Image: cat.jpg", color=WHITE).move_to(cat_img)
            cat_img = VGroup(cat_img, text_fallback)
            
        cat_img.move_to(ORIGIN + UP*0.5)

        # AI Logo the user requested
        ai_circle = Circle(radius=1.5, color=FAMI_CYAN, stroke_width=2)
        ai_hex = RegularPolygon(n=6, color=FAMI_BLUE, fill_opacity=0.15).scale(1.6)
        ai_text = Text("AI", font="Segoe UI", font_size=65, weight=BOLD, color=WHITE)
        neurons = VGroup(*[Line(ORIGIN, np.array([np.cos(a), np.sin(a), 0]) * 2.2, color=FAMI_CYAN, stroke_width=2, stroke_opacity=0.4)
            for a in np.linspace(0, 2*PI, 12, endpoint=False)])
        dots = VGroup(*[Dot(l.get_end(), color=ACCENT, radius=0.07) for l in neurons])
        
        ai_logo = VGroup(ai_hex, neurons, dots, ai_circle, ai_text)
        
        # Thêm dấu hỏi chấm theo yêu cầu
        question_mark = Text("?", font="Segoe UI", font_size=100, weight=BOLD, color=ACCENT)
        question_mark.next_to(ai_logo, UP + RIGHT, buff=-0.5)
        
        ai_group = VGroup(ai_logo, question_mark)
        ai_group.scale_to_fit_width(5.0)
        ai_group.move_to(cat_img)

        # ==========================================
        # 🎬 ĐỒNG BỘ VOICEOVER CHUẨN
        # ==========================================
        with self.voiceover(text="Khi bạn nhìn một con mèo… bạn thấy tai, mắt, bộ lông.") as tracker:
            self.update_subtitle("Khi bạn nhìn một con mèo… bạn thấy tai, mắt, bộ lông.")
            self.play(Write(title), run_time=min(1.0, tracker.duration * 0.2))
            self.play(FadeIn(cat_img, shift=UP*0.5), run_time=min(1.5, tracker.duration * 0.5))

        with self.voiceover(text="Nhưng với AI thì sao?") as tracker:
            self.update_subtitle("Nhưng với AI thì sao?")
            # Biến đổi ảnh mèo thành AI Logo + Dấu hỏi
            self.play(FadeOut(cat_img), FadeIn(ai_group), run_time=min(1.5, tracker.duration * 0.6))
            
            # Animation nhẹ cho AI Logo để thêm sinh động
            self.play(Rotate(ai_hex, angle=PI/4), run_time=min(0.8, tracker.duration * 0.2))
            
        self.finish_scene()
