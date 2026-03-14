import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from skills.fami_lib import *
from skills.fami_assets_helper import *
from skills.fami_effects import *

class Scene2_MainBody(FaMIBaseScene):
    def construct(self):
        title = self.create_title("ĐỊNH LÝ BAYES", "TRONG THỰC TẾ")
        
        # ==========================================
        # 🎨 PHẦN 0: CÔNG THỨC BAYES
        # ==========================================
        bayes_formula = MathTex(r"P(A|B) = \frac{P(B|A)P(A)}{P(B)}")
        bayes_formula.scale(2.0)
        if bayes_formula.width > 7.5:
            bayes_formula.scale_to_fit_width(7.5)
        apply_fami_gradient(bayes_formula)
        
        # ==========================================
        # 🎨 PHẦN 1: ƯU & NHƯỢC ĐIỂM
        # ==========================================
        pro_box = RoundedRectangle(height=2.5, width=7.0, color=SUCCESS, fill_opacity=0.1)
        pro_title = Text("Ưu điểm:", font="Segoe UI", font_size=40, color=SUCCESS, weight=BOLD)
        
        check_1 = SVGMobject("assets/check.svg").set_color(SUCCESS).set_stroke(width=5).set_height(0.4)
        pro_1_text = Text("Học từ dữ liệu mới", font="Segoe UI", font_size=35)
        pro_1 = VGroup(check_1, pro_1_text).arrange(RIGHT, buff=0.3)
        
        check_2 = SVGMobject("assets/check.svg").set_color(SUCCESS).set_stroke(width=5).set_height(0.4)
        pro_2_text = Text("Giảm đánh nhầm & Tốc độ nhanh", font="Segoe UI", font_size=35)
        pro_2 = VGroup(check_2, pro_2_text).arrange(RIGHT, buff=0.3)
        
        pro_list = VGroup(pro_1, pro_2).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        pro_content = VGroup(pro_title, pro_list).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        pro_box.surround(pro_content, buff=0.4)
        pro_group = VGroup(pro_box, pro_content)
        pro_group.move_to(UP * 1.5)
        
        con_box = RoundedRectangle(height=1.5, width=7.0, color=DANGER, fill_opacity=0.1)
        con_title = Text("Hạn chế:", font="Segoe UI", font_size=40, color=DANGER, weight=BOLD)
        
        x_icon = SVGMobject("assets/x.svg").set_color(DANGER).set_stroke(width=5).set_height(0.4)
        con_1_text = Text("Spam ngày càng tinh vi", font="Segoe UI", font_size=35)
        con_1 = VGroup(x_icon, con_1_text).arrange(RIGHT, buff=0.3)
        
        con_content = VGroup(con_title, con_1).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        con_box.surround(con_content, buff=0.4)
        con_group = VGroup(con_box, con_content)
        con_group.next_to(pro_group, DOWN, buff=0.5, aligned_edge=LEFT)

        # Hình ảnh minh họa cho Ưu điểm (sẽ hiện ở khoảng trống bên dưới)
        pro_illustration_1 = SVGMobject("assets/robot.svg").set_color(SUCCESS).set_stroke(width=5).set_height(1.5).move_to(DOWN * 1.5 + LEFT * 1.5)
        pro_illustration_2 = SVGMobject("assets/chart-line.svg").set_color(SUCCESS).set_stroke(width=5).set_height(1.5).move_to(DOWN * 1.5 + RIGHT * 1.5)
        pro_illustrations = VGroup(pro_illustration_1, pro_illustration_2)

        part_1_group = VGroup(pro_group, con_group)
        if part_1_group.width > 7.5:
            part_1_group.scale_to_fit_width(7.5)

        # ==========================================
        # 🎨 PHẦN 2: VÍ DỤ SPAM
        # ==========================================
        free_text = Text('"free"', font="Segoe UI", font_size=60, color=FAMI_CYAN, weight=BOLD)
        free_text.move_to(UP * 1.5)
        
        var_1 = Text("fr33", font="Segoe UI", font_size=50, color=DANGER)
        var_2 = Text("f.r.e.e", font="Segoe UI", font_size=50, color=DANGER)
        var_3 = Text("fr€€", font="Segoe UI", font_size=50, color=DANGER)
        
        variants = VGroup(var_1, var_2, var_3).arrange(RIGHT, buff=0.8)
        variants.move_to(DOWN * 1.5)
        
        arrows = VGroup(
            Arrow(free_text.get_bottom(), var_1.get_top(), color=WHITE, buff=0.2),
            Arrow(free_text.get_bottom(), var_2.get_top(), color=WHITE, buff=0.2),
            Arrow(free_text.get_bottom(), var_3.get_top(), color=WHITE, buff=0.2)
        )
        
        part_2_group = VGroup(free_text, variants, arrows)
        if part_2_group.width > 7.5:
            part_2_group.scale_to_fit_width(7.5)

        # ==========================================
        # 🎬 ĐỒNG BỘ VOICEOVER CHUẨN
        # ==========================================
        with self.voiceover(text="Qua câu chuyện này, ta thấy rằng Định lý Bayes không chỉ là công thức lý thuyết mà còn được ứng dụng trực tiếp trong đời sống.") as tracker:
            self.update_subtitle("Qua câu chuyện này, ta thấy rằng Định lý Bayes...")
            self.play(Write(title), run_time=min(1.5, tracker.duration * 0.3))
            self.play(Write(bayes_formula), run_time=min(1.5, tracker.duration * 0.4))
            
        with self.voiceover(text="Về ưu điểm, đây không phải thuật toán tĩnh, nó có khả năng học từ dữ liệu mới, giảm thiểu việc đánh nhầm email quan trọng thành Spam cùng tốc độ tính toán nhanh.") as tracker:
            self.update_subtitle("Về ưu điểm, nó có khả năng học từ dữ liệu mới...")
            self.play(FadeOut(bayes_formula, shift=UP*0.5), run_time=min(0.5, tracker.duration * 0.1))
            self.play(FadeIn(pro_box), FadeIn(pro_title), run_time=min(0.5, tracker.duration * 0.1))
            self.play(FadeIn(pro_1, shift=RIGHT*0.5), FadeIn(pro_illustration_1, shift=UP*0.5), run_time=min(1.0, tracker.duration * 0.3))
            self.play(FadeIn(pro_2, shift=RIGHT*0.5), FadeIn(pro_illustration_2, shift=UP*0.5), run_time=min(1.0, tracker.duration * 0.3))
            
        with self.voiceover(text="Về hạn chế thì Spam ngày nay ngày càng tinh vi.") as tracker:
            self.update_subtitle("Về hạn chế thì Spam ngày nay ngày càng tinh vi.")
            self.play(FadeOut(pro_illustrations, shift=DOWN*0.5), run_time=min(0.5, tracker.duration * 0.1))
            self.play(FadeIn(con_box), FadeIn(con_title), run_time=min(0.5, tracker.duration * 0.1))
            self.play(FadeIn(con_1, shift=RIGHT*0.5), run_time=min(1.0, tracker.duration * 0.4))
            
        with self.voiceover(text="Thay vì viết “free”, kẻ gửi có thể viết “fr33”; “f.r.e.e”; “fr€€” làm hệ thống dựa trên từ khóa khó nhận diện.") as tracker:
            self.update_subtitle('Thay vì viết "free", kẻ gửi có thể viết "fr33"...')
            
            # Xóa part 1, hiện part 2
            self.play(FadeOut(part_1_group), run_time=min(0.5, tracker.duration * 0.1))
            
            self.play(Write(free_text), run_time=min(0.8, tracker.duration * 0.2))
            
            self.play(GrowArrow(arrows[0]), FadeIn(var_1, shift=DOWN*0.2), run_time=min(0.5, tracker.duration * 0.15))
            self.play(GrowArrow(arrows[1]), FadeIn(var_2, shift=DOWN*0.2), run_time=min(0.5, tracker.duration * 0.15))
            self.play(GrowArrow(arrows[2]), FadeIn(var_3, shift=DOWN*0.2), run_time=min(0.5, tracker.duration * 0.15))
            
        self.finish_scene()
