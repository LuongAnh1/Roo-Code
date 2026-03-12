from manim import *

def create_quote_box(text_str, author="", color=WHITE):
    """Tạo một hộp trích dẫn đẹp mắt"""
    content = Text(f'"{text_str}"', font="Segoe UI", font_size=32, italic=True)
    if content.width > 6:
        content.scale_to_fit_width(6)
        
    box = SurroundingRectangle(content, color=color, buff=0.5, corner_radius=0.2)
    
    if author:
        sign = Text(f"- {author}", font_size=24, color=color).next_to(box, DOWN, aligned_edge=RIGHT)
        return VGroup(box, content, sign)
    return VGroup(box, content)

def create_step_indicator(current_step, total_steps, label="Bước"):
    """Tạo chỉ báo tiến trình (Step 1/4)"""
    circles = VGroup(*[Circle(radius=0.2, color=GRAY) for _ in range(total_steps)]).arrange(RIGHT, buff=0.3)
    circles[current_step-1].set_color(YELLOW).set_fill(YELLOW, opacity=1)
    
    text = Text(f"{label} {current_step}/{total_steps}", font_size=28).next_to(circles, UP, buff=0.2)
    return VGroup(circles, text)

def create_pointer_callout(target_obj, text_str, direction=RIGHT):
    """Tạo chú thích có mũi tên chỉ vào vật thể"""
    label = Text(text_str, font_size=24, background_stroke_width=2)
    arrow = Arrow(start=label.get_edge_center(-direction), end=target_obj.get_center(), buff=0.1)
    return VGroup(label, arrow)