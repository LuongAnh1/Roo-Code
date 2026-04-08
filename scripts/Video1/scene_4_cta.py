import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from skills.fami_lib import *
from skills.fami_assets_helper import *

class Scene4_CTA(FaMIBaseScene):
    def construct(self):
        title = self.create_title("GỢI Ý TIẾP THEO")

        # LEVEL 2 Text
        level2_text = Text("LEVEL 2", font="Segoe UI", font_size=90, weight=BOLD, color=YELLOW)
        level2_text.move_to(UP * 1.0)
        
        # Mobjects
        wave_noise = load_svg_icon("assets/Nhieu_Song/CTA/wave-and-noise.svg")
        if wave_noise:
            wave_noise.set_stroke(width=6, color=WHITE)
            wave_noise.set_fill(color=BLUE, opacity=0.8)
            wave_noise.scale(1.2).move_to(DOWN * 0.5)
            
        bell_curve = load_svg_icon("assets/Nhieu_Song/CTA/bell-curve-mold.svg")
        if bell_curve:
            bell_curve.set_stroke(width=6, color=YELLOW)
            bell_curve.set_fill(color=FAMI_CYAN, opacity=0.8)
            bell_curve.scale(1.2).move_to(UP * 2.5) # Above the noise

        ready_text = Text("SẴN SÀNG CHƯA?", font="Segoe UI", font_size=70, weight=BOLD, color=RED)
        ready_text.move_to(UP * 1.0)

        # 🔒 VÙNG KHÓA CỨNG CTA (LOCKED CTA ZONE)
        cta_box = RoundedRectangle(height=1.0, width=6.5, color=FAMI_CYAN)
        cta_text = Text("Comment nếu bạn đã sẵn sàng!", font="Segoe UI", font_size=30).move_to(cta_box)
        cta_group = VGroup(cta_box, cta_text).move_to(DOWN * 1.5)

        arrow = Arrow(
            cta_group.get_bottom() + DOWN * 0.2, 
            cta_group.get_bottom() + DOWN * 1.2, 
            color=SUCCESS, 
            stroke_width=20,
            max_tip_length_to_length_ratio=0.4
        )

        with self.voiceover(text="Đó là bài toán hôm nay. Còn gợi ý cho Level tiếp theo:") as tracker:
            self.update_subtitle("Đó là bài toán hôm nay. Còn gợi ý cho Level tiếp theo:")
            self.play(Write(title), run_time=min(1.0, tracker.duration * 0.3))
            
            # Level 2 popup
            anim, r_func = skill_pop_in(level2_text)
            self.play(anim, rate_func=r_func, run_time=min(0.8, tracker.duration * 0.4))
            self.play(Wiggle(level2_text), run_time=min(1.0, tracker.duration * 0.2))
            self.play(FadeOut(level2_text), run_time=min(0.5, tracker.duration * 0.1))

        with self.voiceover(text="Mô phỏng Nhiễu trắng Gaussian") as tracker:
            self.update_subtitle("Mô phỏng Nhiễu trắng Gaussian")
            if wave_noise:
                anim, r_func = skill_pop_in(wave_noise)
                self.play(anim, rate_func=r_func, run_time=min(0.8, tracker.duration))
                
        with self.voiceover(text="bằng Phân phối chuẩn.") as tracker:
            self.update_subtitle("bằng Phân phối chuẩn.")
            if bell_curve:
                # fall down from above
                bell_curve.shift(UP * 4)
                self.play(bell_curve.animate.shift(DOWN * 4), rate_func=rate_functions.ease_in_out_bounce, run_time=min(1.0, tracker.duration))

        with self.voiceover(text="Bạn đã sẵn sàng chưa?") as tracker:
            self.update_subtitle("Bạn đã sẵn sàng chưa?")
            
            anims_out = []
            if wave_noise: anims_out.append(FadeOut(wave_noise, shift=DOWN))
            if bell_curve: anims_out.append(FadeOut(bell_curve, shift=DOWN))
            if anims_out:
                self.play(*anims_out, run_time=min(0.5, tracker.duration * 0.2))
                
            anim, r_func = skill_pop_in(ready_text)
            self.play(anim, rate_func=r_func, run_time=min(0.8, tracker.duration * 0.4))
            
            # Show CTA
            self.play(FadeIn(cta_group, shift=UP*0.5), GrowArrow(arrow), run_time=min(0.8, tracker.duration * 0.3))
            
        self.finish_scene()
