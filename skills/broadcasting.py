from manim import *
import os

from skills.bit import BitSequence

class Broadcasting(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        svg_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "Nhieu_Song", "broadcasting.svg"))
        self.icon = SVGMobject(svg_path).scale(1.3).set_color(GOLD_B)
        self.add(self.icon)
        
        self.label = Text("Sent:", font_size=24, weight=BOLD).next_to(self.icon, DOWN, buff=0.5).set_color(WHITE)
        self.add(self.label)
        
        self.current_seq_display = None
        self.prev_seq_display = None
        self.current_scale_factor = 1.0
        
    def update_sequence(self, scene, new_seq_str, run_time=0.3, scale_factor=1.0):
        new_display = BitSequence(sequence=new_seq_str, color="#00FF00", font_size=32, scale_factor=scale_factor)
        new_display.next_to(self.label, DOWN, buff=0.5 * scale_factor)
        self.add(new_display)
        
        if self.current_seq_display:
            animations = []
            if self.prev_seq_display:
                animations.append(FadeOut(self.prev_seq_display))
                self.remove(self.prev_seq_display)
            
            self.prev_seq_display = self.current_seq_display
            self.current_seq_display = new_display
            
            animations.append(FadeIn(self.current_seq_display))
            
            if self.current_scale_factor != scale_factor:
                relative_scale = scale_factor / self.current_scale_factor
                animations.append(
                    self.prev_seq_display.animate.scale(relative_scale).next_to(self.current_seq_display, DOWN, buff=0.3 * scale_factor).set_opacity(0.3)
                )
            else:
                animations.append(
                    self.prev_seq_display.animate.next_to(self.current_seq_display, DOWN, buff=0.3 * scale_factor).set_opacity(0.3)
                )
            
            self.current_scale_factor = scale_factor
            
            scene.play(*animations, run_time=run_time)
        else:
            self.current_seq_display = new_display
            self.current_scale_factor = scale_factor
            scene.play(FadeIn(self.current_seq_display), run_time=run_time)

