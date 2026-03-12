"""
Module: fami_assets_helper.py
Module chuyên dụng để lấy, sắp xếp các icon SVG từ thư mục /assets/
"""

import os

# Cố định đường dẫn để Agent không tìm lung tung
ASSETS_DIR = "./assets/"

def load_svg_icon(icon_name, size=1.0, color="#FFFFFF"):
    """
    Tải một icon .svg từ folder assets và thiết lập màu sắc, kích thước.
    
    Args:
        icon_name (str): Tên file, ví dụ "google.svg", "math-plus.svg", "robot.svg".
        size (float): Tỷ lệ kích thước (Mặc định 1.0).
        color (str): Đổi màu cho icon (vì các icon được setup dể đổi màu).
        
    Returns:
        SVGMobject: Đối tượng hình ảnh có thể đưa vào Video.
    """
    # file_path = os.path.join(ASSETS_DIR, icon_name)
    # if not os.path.exists(file_path):
    #     raise FileNotFoundError(f"Missing icon: {icon_name} in {ASSETS_DIR}")
    
    # icon = SVGMobject(file_path)
    # icon.scale(size)
    # icon.set_color(color)
    # return icon
    pass

def create_icon_with_text(icon_name, text_str, spacing=0.5):
    """
    Tạo một nhóm (Group) gồm 1 Icon nằm bên trái và 1 dòng chữ nằm bên phải.
    Rất hữu ích để tạo tiêu đề, danh sách (List).
    
    Args:
        icon_name (str): Tên file svg.
        text_str (str): Nội dung chữ.
        
    Returns:
        VGroup: Cụm Icon + Text.
    """
    # icon = load_svg_icon(icon_name, size=0.5)
    # text = Text(text_str, font_size=24)
    # text.next_to(icon, RIGHT, buff=spacing)
    # return VGroup(icon, text)
    pass