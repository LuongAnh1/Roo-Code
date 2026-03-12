"""
Module: fami_math_graph.py
Cung cấp các hàm hỗ trợ vẽ đồ thị, hệ trục tọa độ và hình học.
Agent có thể import các hàm từ đây để không phải tự viết lại logic toán học phức tạp.
"""

# Giả định import từ thư viện gốc (Ví dụ: Manim)
# from manim import * 
# from fami_lib import *

def create_standard_axes(x_range=[-5, 5, 1], y_range=[-5, 5, 1], width=10, height=6):
    """
    Tạo một hệ trục tọa độ (Axes) chuẩn, có sẵn mũi tên và số.
    
    Args:
        x_range (list): [min, max, step] cho trục Ox.
        y_range (list): [min, max, step] cho trục Oy.
        width (float): Chiều rộng của trục trên màn hình.
        height (float): Chiều cao của trục trên màn hình.
        
    Returns:
        Axes object: Đối tượng hệ trục tọa độ đã được thiết lập sẵn.
    """
    # Pseudo-code / Manim logic
    # axes = Axes(x_range=x_range, y_range=y_range, x_length=width, y_length=height)
    # axes.add_coordinates()
    # return axes
    pass

def plot_custom_function(axes, func, color="#FF0000", stroke_width=3):
    """
    Vẽ đường cong đồ thị từ một phương trình toán học trên hệ trục có sẵn.
    
    Args:
        axes (Axes): Hệ trục tọa độ được tạo từ create_standard_axes().
        func (callable): Hàm lambda, ví dụ: lambda x: x**2
        color (str): Mã màu hex của đường đồ thị.
        
    Returns:
        VGroup/Mobject: Đường cong đồ thị (Graph curve).
    """
    # graph = axes.plot(func, color=color, stroke_width=stroke_width)
    # return graph
    pass

def create_geometric_polygon(*points, color="#00FF00", fill_opacity=0.3):
    """
    Vẽ một đa giác (Tam giác, hình vuông...) dựa trên các tọa độ điểm.
    
    Args:
        *points: Các tuple tọa độ, ví dụ (0,0), (2,0), (1,2)
        color (str): Màu viền.
        fill_opacity (float): Độ đậm nhạt của màu nền (0 đến 1).
        
    Returns:
        Polygon object.
    """
    # poly = Polygon(*points, color=color, fill_opacity=fill_opacity)
    # return poly
    pass