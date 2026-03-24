import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from skills.fami_lib import *
from skills.fami_assets_helper import *

class Scene1_Hook(FaMIBaseScene):
    def construct(self):
        title = self.create_title("TIN NHẮN DỄ BỊ NHIỄU SÓNG?", "LÀM SAO ĐỂ ĐO LƯỜNG?")
        
        # Mobjects
        tin_nhan = load_svg_icon("assets/Nhieu_Song/Hook/tin-nhan.svg")
        if tin_nhan:
            tin_nhan.set_stroke(width=4)
            tin_nhan.scale(1.0).move_to(LEFT * 2.0 + UP * 0.5)
        
        may_bao = load_svg_icon("assets/Nhieu_Song/Hook/may-bao.svg")
        if may_bao:
            may_bao.set_stroke(width=4)
            may_bao.scale(1.2).move_to(RIGHT * 1.5 + UP * 0.5)
        
        clock = load_svg_icon("assets/Nhieu_Song/Hook/clock.svg")
        if clock:
            clock.set_stroke(width=4)
            clock.scale(1.5).move_to(UP * 0.5)
        
        with self.voiceover(text="Tin nhắn gửi đi rất dễ bị nhiễu sóng.") as tracker:
            self.update_subtitle("Tin nhắn gửi đi rất dễ bị nhiễu sóng.", 'neon')
            self.play(Write(title), run_time=min(1.0, tracker.duration * 0.3))
            
            if tin_nhan:
                anim, r_func = skill_pop_in(tin_nhan)
                self.play(anim, rate_func=r_func, run_time=min(0.5, tracker.duration * 0.2))
            
            if may_bao and tin_nhan:
                self.play(
                    FadeIn(may_bao, shift=DOWN), 
                    Wiggle(tin_nhan, scale_value=1.2, rotation_angle=0.1 * PI),
                    run_time=min(1.0, tracker.duration * 0.3)
                )
            
        with self.voiceover(text="Vậy lấy gì để đo lường chất lượng đường truyền?") as tracker:
            self.update_subtitle("Vậy lấy gì để đo lường chất lượng đường truyền?", 'neon')
            
            anims_out = []
            if tin_nhan: anims_out.append(FadeOut(tin_nhan, shift=LEFT))
            if may_bao: anims_out.append(FadeOut(may_bao, shift=UP))
            if anims_out:
                self.play(*anims_out, run_time=min(0.5, tracker.duration * 0.2))
            
            if clock:
                anim, r_func = skill_pop_in(clock)
                self.play(anim, rate_func=r_func, run_time=min(0.8, tracker.duration * 0.4))
                
                # Sóng tỏa ra
                arcs = VGroup(*[
                    Arc(radius=1.5 + i*0.6, angle=PI/2, start_angle=PI/4, color=SUCCESS, stroke_width=8)
                    for i in range(3)
                ])
                arcs.rotate(PI/4)
                arcs.next_to(clock, UP, buff=0.3)
                
                self.play(Create(arcs, lag_ratio=0.5), run_time=min(1.0, tracker.duration * 0.2))

        self.finish_scene()
