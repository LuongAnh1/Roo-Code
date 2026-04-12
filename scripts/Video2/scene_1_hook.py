import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from skills.fami_lib import *
from skills.fami_assets_helper import load_svg_icon
from skills.fami_effects import animate_pop_in

class Scene1_Hook(FaMIBaseScene):
    def construct(self):
        title = self.create_title("DỰ ĐOÁN GIÁ NHÀ", "VỚI HỒI QUY TUYẾN TÍNH")
        
        # ==========================================
        # 🎨 VÙNG SÁNG TẠO (CREATIVE ZONE)
        # ==========================================
        
        # Biểu tượng căn nhà (trái)
        house_icon = load_svg_icon("Hoi_Quy_TT/Hook/house.svg")
        house_icon.scale_to_fit_width(2.0)
        house_icon.set_stroke(width=10)
        apply_fami_gradient(house_icon)
        area_text = Text("50m²", font="Segoe UI", font_size=40, weight=BOLD, color=SUCCESS)
        area_text.next_to(house_icon, DOWN, buff=0.5)
        house_group = VGroup(house_icon, area_text).move_to(LEFT * 2.0 + UP * 0.5)
        
        # Biểu tượng giá tiền (phải)
        money_icon = Text("?", font="Segoe UI", font_size=120, color=FAMI_CYAN)
        price_text = Text("Giá tiền", font="Segoe UI", font_size=40, color=YELLOW)
        price_text.next_to(money_icon, DOWN, buff=0.5)
        money_group = VGroup(money_icon, price_text).move_to(RIGHT * 2.0 + UP * 0.5)
        
        # Mũi tên kết nối
        arrow = Arrow(house_group.get_right(), money_group.get_left(), buff=0.3, color=WHITE)
        
        # Đảm bảo ko tràn màn hình (9:16)
        main_group = VGroup(house_group, arrow, money_group)
        if main_group.width > 7.5:
            main_group.scale_to_fit_width(7.5)

        # ==========================================
        # 🎬 ĐỒNG BỘ VOICEOVER CHUẨN
        # ==========================================
        with self.voiceover(text="Làm sao để dự đoán giá một căn nhà khi bạn chỉ biết diện tích của nó?") as tracker:
            self.update_subtitle("Làm sao để dự đoán giá một căn nhà khi bạn chỉ biết diện tích của nó?")
            self.play(Write(title), run_time=min(1.0, tracker.duration * 0.2))
            
            # Xuất hiện nhà và diện tích
            self.play(FadeIn(house_group, scale=0.5), run_time=tracker.duration * 0.3)
            
            # Xuất hiện mũi tên và dấu chấm hỏi (giá tiền)
            self.play(GrowArrow(arrow), run_time=tracker.duration * 0.2)
            self.play(FadeIn(money_group, scale=0.5), run_time=tracker.duration * 0.2)
            
            # Wiggle the question mark slightly
            self.play(Wiggle(money_icon, scale_value=1.2, rotation_angle=0.1 * PI), run_time=tracker.duration * 0.1)
            
        self.finish_scene()
