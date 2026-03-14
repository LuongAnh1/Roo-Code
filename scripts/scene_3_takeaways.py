import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from skills.fami_lib import *
from skills.fami_assets_helper import *
from skills.fami_effects import *

class Scene3_Takeaways(FaMIBaseScene):
    def construct(self):
        title = self.create_title("TỪ KHÓA", "TÌM KIẾM")
        
        # 🎨 VÙNG SÁNG TẠO: 
        google_icon = SVGMobject("assets/google.svg").set_color(WHITE).set_stroke(width=5).set_height(1.5).move_to(UP * 2.0)
        
        # Search bar
        search_box = RoundedRectangle(height=1.2, width=7.0, corner_radius=0.6, color=WHITE, fill_color=BLACK, fill_opacity=0.5)
        search_box.move_to(ORIGIN)
        
        search_icon = SVGMobject("assets/search.svg").set_color(WHITE).set_stroke(width=5).set_height(0.6)
        search_icon.move_to(search_box.get_left() + RIGHT * 0.6)
        
        # Điểm mốc để gõ chữ
        typing_start_ref = Dot(search_icon.get_right() + RIGHT * 0.1, fill_opacity=0)
        self.add(typing_start_ref)
        
        keyword = "Naive Bayes Classifier"

        # 🎬 ĐỒNG BỘ VOICEOVER CHUẨN
        with self.voiceover(text="Từ phương pháp của An, nếu muốn hiểu sâu hơn về cách các hệ thống lọc Spam hoạt động trong thực tế, bạn có thể tìm kiếm cụm từ khóa Naive Bayes Classifier là hệ thống lọc Spam lớn của Google") as tracker:
            self.update_subtitle("...bạn có thể tìm kiếm cụm từ khóa Naive Bayes Classifier...")
            self.play(Write(title), run_time=min(1.0, tracker.duration * 0.1))
            
            pop_in_anim, pop_in_rate = skill_pop_in(google_icon)
            self.play(pop_in_anim, rate_func=pop_in_rate, run_time=min(0.5, tracker.duration * 0.1))
            
            self.play(Create(search_box), FadeIn(search_icon), run_time=min(1.0, tracker.duration * 0.15))
            
            # Hiệu ứng gõ chữ khóa trục Y
            last_char = typing_start_ref
            current_buff = 0.15
            
            # Tính thời gian gõ mỗi chữ
            total_typing_time = min(3.0, tracker.duration * 0.4)
            time_per_char = total_typing_time / len(keyword)
            
            for i, char in enumerate(keyword):
                if char == " ":
                    current_buff = 0.15
                    continue
                
                new_char = Text(char, font="Segoe UI", font_size=35, weight=BOLD, color=WHITE)
                
                new_char.next_to(last_char, RIGHT, buff=current_buff, aligned_edge=DOWN)
                new_char.match_y(typing_start_ref) # KHÓA CHẾT TRỤC Y THEO VẬT THỂ MỐC
                
                self.play(FadeIn(new_char), run_time=time_per_char)
                last_char = new_char
                current_buff = 0.05

        self.finish_scene()
