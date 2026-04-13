import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from skills.fami_lib import *
from skills.fami_assets_helper import *

class Scene3_Takeaways(FaMIBaseScene):
    def construct(self):
        title = self.create_title("4 TỪ KHÓA QUAN TRỌNG", "CẦN BỎ TÚI NGAY")
        
        # Mobjects
        cheat_sheet = RoundedRectangle(width=7.0, height=4.5, color=FAMI_BLUE, fill_opacity=0.1, stroke_width=4)
        cheat_sheet.move_to(UP * 0.5)
        
        keywords = [
            "Mô phỏng Monte Carlo",
            "Luật số lớn",
            "Phân phối Nhị thức",
            "Phân phối Bernoulli"
        ]
        
        lines = VGroup()
        for kw in keywords:
            icon = load_svg_icon("assets/check.svg", color=SUCCESS, size=0.25)
            if icon:
                icon.set_stroke(width=8)
            text = Text(kw, font="Segoe UI", font_size=32, weight=BOLD)
            # Create a row
            row = VGroup(icon, text) if icon else VGroup(text)
            row.arrange(RIGHT, buff=0.3)
            lines.add(row)
            
        lines.arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        lines.move_to(cheat_sheet.get_center())
        
        # Search & CTA Arrow
        search_icon = load_svg_icon("assets/search.svg", color=WHITE, size=0.5)
        if search_icon:
            search_icon.set_stroke(width=6)
            search_icon.move_to(DOWN * 2.5)
            
        save_arrow = Arrow(
            start=DOWN * 2.5 + RIGHT * 1.0, 
            end=DOWN * 3.5 + RIGHT * 3.5, 
            color=YELLOW, stroke_width=8, buff=0.1, path_arc=-0.5
        )
        
        with self.voiceover(text="Và 4 từ khóa bạn cần 'bỏ túi' hôm nay là:") as tracker:
            self.update_subtitle("Và 4 từ khóa bạn cần 'bỏ túi' hôm nay là:")
            self.play(Write(title), run_time=min(1.0, tracker.duration * 0.4))
            self.play(Create(cheat_sheet), run_time=min(0.8, tracker.duration * 0.4))
            
        with self.voiceover(text="Mô phỏng Monte Carlo,") as tracker:
            self.update_subtitle("Mô phỏng Monte Carlo,")
            self.play(FadeIn(lines[0], shift=RIGHT), run_time=min(0.8, tracker.duration))
            
        with self.voiceover(text="Luật số lớn,") as tracker:
            self.update_subtitle("Luật số lớn,")
            self.play(FadeIn(lines[1], shift=RIGHT), run_time=min(0.8, tracker.duration))
            
        with self.voiceover(text="Phân phối Nhị thức") as tracker:
            self.update_subtitle("Phân phối Nhị thức")
            self.play(FadeIn(lines[2], shift=RIGHT), run_time=min(0.8, tracker.duration))
            
        with self.voiceover(text="và Bernoulli.") as tracker:
            self.update_subtitle("và Bernoulli.")
            self.play(FadeIn(lines[3], shift=RIGHT), run_time=min(0.8, tracker.duration))
            
        with self.voiceover(text="Lưu lại video và tra cứu ngay để thấy xác suất ứng dụng đỉnh cỡ nào nhé!") as tracker:
            self.update_subtitle("Lưu lại video và tra cứu ngay để thấy xác suất ứng dụng đỉnh cỡ nào nhé!")
            
            if search_icon:
                anim, r_func = skill_pop_in(search_icon)
                self.play(anim, rate_func=r_func, run_time=min(0.5, tracker.duration * 0.2))
                
            self.play(GrowArrow(save_arrow), run_time=min(0.5, tracker.duration * 0.2))
            
            # Blink/Wiggle the arrow
            self.play(Wiggle(save_arrow), run_time=min(0.8, tracker.duration * 0.3))

        self.finish_scene()
