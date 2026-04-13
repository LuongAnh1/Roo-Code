import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from skills.fami_lib import *
from skills.fami_assets_helper import *

class Scene2_MainBody(FaMIBaseScene):
    def construct(self):
        title = self.create_title("CÔNG THỨC CHỐT HẠ", "ĐO LƯỜNG KÊNH TRUYỀN")
        
        # Mobjects for equation
        xuc_xac = load_svg_icon("assets/Nhieu_Song/Main Body/xuc-xac.svg")
        if xuc_xac:
            xuc_xac.set_stroke(width=4)
            xuc_xac.scale(0.8)
            
        dau_cong = load_svg_icon("assets/Nhieu_Song/Main Body/daucong-xu-bieudo.svg")
        if dau_cong:
            dau_cong.set_stroke(width=4)
            dau_cong.scale(0.8)
            
        luat_so_lon = load_svg_icon("assets/Nhieu_Song/Main Body/law-of-large-numbers.svg")
        if luat_so_lon:
            luat_so_lon.set_stroke(width=4)
            luat_so_lon.scale(0.8)
            
        equation = VGroup()
        if xuc_xac: equation.add(xuc_xac)
        if dau_cong: equation.add(dau_cong)
        if luat_so_lon: equation.add(luat_so_lon)
        
        equation.arrange(RIGHT, buff=0.4).move_to(UP * 1.0)
        if equation.width > 7.5:
            equation.scale_to_fit_width(7.5)
            equation.move_to(UP * 1.0)
            
        # Result Mobject
        ber_result = load_svg_icon("assets/Nhieu_Song/Main Body/ber-result.svg")
        if ber_result:
            ber_result.set_stroke(width=4)
            ber_result.scale(1.5).move_to(ORIGIN)

        with self.voiceover(text="Tóm lại, công thức chốt hạ để đo lường kênh truyền chính là:") as tracker:
            self.update_subtitle("Tóm lại, công thức chốt hạ để đo lường kênh truyền chính là:")
            self.play(Write(title), run_time=min(1.5, tracker.duration * 0.8))
            
        with self.voiceover(text="Mô phỏng Monte Carlo,") as tracker:
            self.update_subtitle("Mô phỏng Monte Carlo,")
            if xuc_xac:
                anim, r_func = skill_pop_in(xuc_xac)
                self.play(anim, rate_func=r_func, run_time=min(0.8, tracker.duration * 0.8))
                
        with self.voiceover(text="cộng với phân phối Bernoulli, Nhị thức") as tracker:
            self.update_subtitle("cộng với phân phối Bernoulli, Nhị thức")
            if dau_cong:
                anim, r_func = skill_pop_in(dau_cong)
                self.play(anim, rate_func=r_func, run_time=min(0.8, tracker.duration * 0.8))
                
        with self.voiceover(text="và Luật số lớn!") as tracker:
            self.update_subtitle("và Luật số lớn!")
            if luat_so_lon:
                anim, r_func = skill_pop_in(luat_so_lon)
                self.play(anim, rate_func=r_func, run_time=min(0.8, tracker.duration * 0.8))

        with self.voiceover(text="Kết quả? Ta ước lượng được chính xác Xác suất lỗi bit - BER!") as tracker:
            self.update_subtitle("Kết quả? Ta ước lượng được chính xác Xác suất lỗi bit - BER!")
            # Hội tụ phương trình
            if len(equation) > 0 and ber_result:
                self.play(
                    equation.animate.scale(0.1).move_to(ORIGIN),
                    run_time=min(0.5, tracker.duration * 0.2)
                )
                self.play(
                    ReplacementTransform(equation, ber_result),
                    run_time=min(1.0, tracker.duration * 0.4)
                )
                self.play(
                    Wiggle(ber_result, scale_value=1.1),
                    run_time=min(1.0, tracker.duration * 0.2)
                )

        self.finish_scene()
