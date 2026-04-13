"""
Module: fami_assets_helper.py
Module chuyên dụng để lấy, sắp xếp các icon SVG từ thư mục /assets/
"""

import os
from manim import *

# Cố định đường dẫn để Agent không tìm lung tung
ASSETS_DIR = "./assets/"

def load_svg_icon(icon_name, size=1.0, color=None):
    """
    Tải một icon .svg từ folder assets và thiết lập màu sắc, kích thước.
    
    Args:
        icon_name (str): Tên file.
        size (float): Tỷ lệ kích thước (Mặc định 1.0).
        color (str): Đổi màu cho icon (Nếu None sẽ giữ màu gốc của svg).
        
    Returns:
        SVGMobject: Đối tượng hình ảnh có thể đưa vào Video.
    """
    if not os.path.exists(icon_name):
        # Thử tìm trong ASSETS_DIR nếu icon_name không phải đường dẫn tuyệt đối/đầy đủ
        file_path = os.path.join(ASSETS_DIR, icon_name)
    else:
        file_path = icon_name
        
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Missing icon: {icon_name} or {file_path}")
    
    icon = SVGMobject(file_path)
    icon.scale(size)
    if color is not None:
        icon.set_color(color)
    return icon

def create_icon_with_text(icon_name, text_str, spacing=0.5):
    """
    Tạo một nhóm (Group) gồm 1 Icon nằm bên trái và 1 dòng chữ nằm bên phải.
    """
    icon = load_svg_icon(icon_name, size=0.5)
    text = Text(text_str, font_size=24)
    text.next_to(icon, RIGHT, buff=spacing)
    return VGroup(icon, text)
