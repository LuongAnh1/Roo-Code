from manim import *

class TestSeparation(Scene):
    def construct(self):
        formula = MathTex(
            r"\mathbb{V}\text{isual } \mathbb{P}\text{roof of } \sum_{n=1}^{\infty} \frac{1}{2^n}",
            font_size=80
        )

        all_glyphs = [m for m in formula.family_members_with_points() if isinstance(m, VMobject)]
        
        # Định nghĩa dải màu bạn muốn đổ cho mỗi chữ
        gradient_colors = [BLUE, GREEN, YELLOW]

        for glyph in all_glyphs:
            # Thủ thuật: Đổ dải màu vào TỪNG nét vẽ đơn lẻ.
            # set_color với list [C1, C2, C3] sẽ trải đều màu 
            # từ trái sang phải lên chính ký tự đó.
            glyph.set_color(gradient_colors)

        self.add(formula)
        self.wait(5)