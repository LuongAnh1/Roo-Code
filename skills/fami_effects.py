"""
Module: fami_effects.py
Cung cấp các animation làm sẵn giúp video sinh động hơn.
"""

def animate_pop_in(mobject, scale_factor=1.2, run_time=0.8):
    """
    Hiệu ứng "Nảy": Đối tượng phóng to lên một chút rồi thu về kích thước gốc.
    Dùng để nhấn mạnh khi một Icon hoặc Text mới xuất hiện.
    
    Args:
        mobject: Đối tượng cần tạo hiệu ứng.
        scale_factor (float): Độ phóng to tối đa trước khi thu nhỏ lại.
        
    Returns:
        Animation object (Dùng chung với self.play()).
    """
    # return Succession(
    #     mobject.animate.scale(scale_factor).set_run_time(run_time/2),
    #     mobject.animate.scale(1/scale_factor).set_run_time(run_time/2)
    # )
    pass

def animate_highlight_text(text_mobject, highlight_color="#FFFF00"):
    """
    Làm nổi bật một đoạn text bằng cách đổi màu và thêm viền sáng (glow).
    
    Args:
        text_mobject: Đối tượng chữ cần làm nổi bật.
        highlight_color: Màu sắc nổi bật (Mặc định vàng).
        
    Returns:
        Animation object.
    """
    # return text_mobject.animate.set_color(highlight_color).scale(1.1)
    pass

def animate_typewriter(text_str, font_size=36, run_time=2.0):
    """
    Hiệu ứng gõ chữ lách cách (Typewriter) cho một đoạn văn bản mới.
    
    Args:
        text_str (str): Nội dung chữ.
        run_time (float): Thời gian gõ (giây).
        
    Returns:
        Tuple (Text Mobject, Animation). Agent phải add Text Mobject vào scene.
    """
    # text_obj = Text(text_str, font_size=font_size)
    # animation = AddTextLetterByLetter(text_obj, run_time=run_time)
    # return text_obj, animation
    pass