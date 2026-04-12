from manim import *

_bit_cache = {}

class BitSequence(VGroup):
    def __init__(self, sequence="101100101", color=BLACK, font_size=36, scale_factor=1.0, **kwargs):
        super().__init__(**kwargs)
        self.bits_str = sequence
        text_group = VGroup()
        for bit_char in sequence:
            key = (bit_char, font_size)
            if key not in _bit_cache:
                _bit_cache[key] = Text(bit_char, font_size=font_size, weight=BOLD)
            t = _bit_cache[key].copy()
            text_group.add(t)
        text_group.arrange(RIGHT, buff=0.2)
        self.add(text_group)
        self.set_color(color)
        if scale_factor != 1.0:
            self.scale(scale_factor)

    def stream_to(self, scene, target_mobject, run_time_speed=1.6):
        """
        Di chuyển chuỗi bit đến một tọa độ thiết bị với tốc độ cho trước
        """
        scene.play(
            self.animate.next_to(target_mobject, LEFT),
            run_time=run_time_speed,
            rate_func=linear
        )
