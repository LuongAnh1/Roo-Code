import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from skills.fami_lib import *
from skills.fami_effects import animate_pop_in

class Scene3_Takeaways(FaMIBaseScene):
    def construct(self):
        title = self.create_title("TỪ KHÓA QUAN TRỌNG", "TÌM HÀM TỐI ƯU")
        
        # ==========================================
        # 🎨 VÙNG SÁNG TẠO (CREATIVE ZONE)
        # ==========================================
        
        # Tạo hàm trợ giúp vẽ Box
        def create_keyword_box(text, y_pos):
            box = RoundedRectangle(width=6.5, height=1.2, corner_radius=0.3, color=FAMI_CYAN, fill_opacity=0.1)
            label = MarkupText(text, font="Segoe UI", font_size=28, justify=True).move_to(box)
            if label.width > 6.0:
                label.scale_to_fit_width(6.0)
            group = VGroup(box, label).move_to(UP * y_pos)
            return group

        box1 = create_keyword_box("1. <span color='#00FF00'>Ordinary Least Squares (OLS)</span>\n(Bình phương tối thiểu)", 2.0)
        box2 = create_keyword_box("2. <span color='#00FF00'>Cost Function</span>\n(Hàm mất mát)", 0.0)
        box3 = create_keyword_box("3. <span color='#00FF00'>Gradient Descent</span>\n(Thuật toán giảm dốc)", -2.0)
        
        # ==========================================
        # 🎬 ĐỒNG BỘ VOICEOVER CHUẨN
        # ==========================================
        with self.voiceover(text="Và để tìm ra hàm tối ưu đó, bạn hãy tìm kiếm các từ khóa này ngay đó là:") as tracker:
            self.update_subtitle("Và để tìm ra hàm tối ưu đó, bạn hãy tìm kiếm các từ khóa này ngay đó là:")
            self.play(Write(title), run_time=min(1.0, tracker.duration * 0.4))
            
        with self.voiceover(text="Bình phương tối thiểu") as tracker:
            self.update_subtitle("Bình phương tối thiểu")
            self.play(animate_pop_in(box1), run_time=tracker.duration * 0.8)
            
        with self.voiceover(text="Hàm mất mát") as tracker:
            self.update_subtitle("Hàm mất mát")
            self.play(animate_pop_in(box2), run_time=tracker.duration * 0.8)
            
        with self.voiceover(text="Và Thuật toán giảm dốc") as tracker:
            self.update_subtitle("Và Thuật toán giảm dốc")
            self.play(animate_pop_in(box3), run_time=tracker.duration * 0.8)

        self.finish_scene()
