from manim import *
import os

class Receiving(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        svg_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "Nhieu_Song", "receiving.svg"))
        self.icon = SVGMobject(svg_path).scale(1.3)
        self.add(self.icon)
        
        self.label = Text("Received:", font_size=24, weight=BOLD).next_to(self.icon, DOWN, buff=0.5).set_color(WHITE)
        self.add(self.label)
        
        self.current_seq_display = None
        
    def update_sequence(self, scene, orig_bits_str, recv_bits_str, run_time=0.3, scale_factor=1.0):
        new_display = VGroup()
        self.add(new_display)
        for k in range(len(recv_bits_str)):
            c = "#00FF00" if orig_bits_str[k] == recv_bits_str[k] else RED
            t = Text(recv_bits_str[k], font_size=32, weight=BOLD).set_color(c)
            new_display.add(t)
        new_display.arrange(RIGHT, buff=0.2)
        if scale_factor != 1.0:
            new_display.scale(scale_factor)
        new_display.next_to(self.label, DOWN, buff=0.5 * scale_factor)
        
        anims = []
        if self.current_seq_display:
            anims.append(FadeOut(self.current_seq_display, shift=DOWN))
            self.remove(self.current_seq_display)
        
        self.current_seq_display = new_display
        anims.append(FadeIn(self.current_seq_display, shift=DOWN))
            
        scene.play(*anims, run_time=run_time)
