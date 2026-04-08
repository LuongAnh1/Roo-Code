import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from skills.fami_lib import *
from skills.fami_effects import animate_pop_in
from skills.fami_assets_helper import load_svg_icon

class Scene4_CTA(FaMIBaseScene):
    def construct(self):
        title = self.create_title("ỨNG DỤNG THỰC TẾ", "TÍNH TOÁN SNR")
        
        # ==========================================
        # 🎨 VÙNG SÁNG TẠO CÂU HỎI (CREATIVE QUESTION ZONE)
        # ==========================================
        
        # 1. Truyền tin (BEP)
        tower_left = load_svg_icon("assets/Hoi_Quy_TT/CTA/Signal Tower.svg").scale_to_fit_width(1.5).move_to(LEFT * 3.0 + UP * 2.0)
        tower_left.set_stroke(width=6)
        
        tower_right = load_svg_icon("assets/Hoi_Quy_TT/CTA/Retro Radio.svg").scale_to_fit_width(1.5).move_to(RIGHT * 3.0 + UP * 2.0)
        tower_right.set_stroke(width=6)
        
        bit_stream = Text("101001", font="Consolas", color=FAMI_CYAN).move_to(UP * 1.5)
        arrow_bep = Arrow(tower_left.get_right(), tower_right.get_left(), buff=0.1, color=GRAY)
        
        bep_text = Text("BEP", font="Segoe UI", font_size=36, weight=BOLD, color=YELLOW).next_to(bit_stream, UP)
        
        transmission_group = VGroup(tower_left, tower_right, arrow_bep, bit_stream, bep_text)
        
        # 2. SNR
        snr_text = Text("SNR", font="Segoe UI", font_size=60, weight=BOLD, color=SUCCESS).move_to(UP * 0.0)
        arrow_to_snr = Arrow(bep_text.get_bottom() + DOWN * 1.0, snr_text.get_top(), buff=0.1)
        
        # 3. Hồi quy tuyến tính + OLS
        solution_box = RoundedRectangle(width=6.0, height=1.0, corner_radius=0.2, color=FAMI_CYAN, fill_opacity=0.2)
        solution_text = Text("Hồi quy tuyến tính + OLS", font="Segoe UI", font_size=32).move_to(solution_box)
        apply_fami_gradient(solution_text)
        solution_group = VGroup(solution_box, solution_text).move_to(DOWN * 1.5)
        arrow_to_solution = Arrow(snr_text.get_bottom(), solution_group.get_top(), buff=0.1)

        # ==========================================
        # 🔒 VÙNG KHÓA CỨNG CTA (LOCKED CTA ZONE)
        # ==========================================
        # Lời kêu gọi (Luôn ở vùng an toàn Y = -3.0)
        cta_box = RoundedRectangle(height=1.0, width=6.5, color=FAMI_CYAN)
        cta_text = Text("Xem video tiếp theo về SNR!", font="Segoe UI", font_size=30).move_to(cta_box)
        cta_group = VGroup(cta_box, cta_text).move_to(DOWN * 1.5)
        cta_arrow = Arrow(cta_group.get_bottom(), cta_group.get_bottom() + DOWN * 1.0, color=SUCCESS)

        # ==========================================
        # 🎬 ĐỒNG BỘ VOICEOVER CHUẨN
        # ==========================================
        with self.voiceover(text="Ở video trước chúng ta đã nói đến BEP dùng để kiểm tra độ chính xác của dữ liệu truyền đi.") as tracker:
            self.update_subtitle("Ở video trước chúng ta đã nói đến BEP dùng để kiểm tra độ chính xác của dữ liệu truyền đi.")
            self.play(Write(title), run_time=min(1.0, tracker.duration * 0.1))
            self.play(FadeIn(tower_left, tower_right), GrowArrow(arrow_bep), run_time=tracker.duration * 0.3)
            self.play(Write(bit_stream), run_time=tracker.duration * 0.2)
            self.play(animate_pop_in(bep_text), run_time=tracker.duration * 0.2)
            
        with self.voiceover(text="Và có 1 thứ liên quan mật thiết đến BEP đó là SNR dùng để xác định chất lượng môi trường.") as tracker:
            self.update_subtitle("Và có 1 thứ liên quan mật thiết đến BEP đó là SNR dùng để xác định chất lượng môi trường.")
            self.play(GrowArrow(arrow_to_snr), run_time=tracker.duration * 0.2)
            self.play(animate_pop_in(snr_text), run_time=tracker.duration * 0.6)
            
        with self.voiceover(text="Về cách xác định thì chúng ta sẽ dùng Hồi quy tuyến tính + OLS.") as tracker:
            self.update_subtitle("Về cách xác định thì chúng ta sẽ dùng Hồi quy tuyến tính + OLS.")
            self.play(GrowArrow(arrow_to_solution), run_time=tracker.duration * 0.2)
            self.play(FadeIn(solution_group, shift=UP*0.5), run_time=tracker.duration * 0.6)
            
        with self.voiceover(text="Vậy chúng ta sẽ thực hiện như nào, hãy xem video tiếp theo về SNR nhé!") as tracker:
            self.update_subtitle("Vậy chúng ta sẽ thực hiện như nào, hãy xem video tiếp theo về SNR nhé!")
            
            # Hỏi chấm nảy lên
            self.play(FadeOut(transmission_group, snr_text, arrow_to_snr, arrow_to_solution, solution_group))
            question_mark = Text("?", font="Segoe UI", font_size=120, color=YELLOW).move_to(UP * 0.5)
            self.play(animate_pop_in(question_mark), run_time=tracker.duration * 0.3)
            
            # Luôn hiện nút CTA ở cuối
            self.play(FadeIn(cta_group, shift = UP*2.0), GrowArrow(cta_arrow), run_time=tracker.duration * 0.4)

        self.finish_scene()
