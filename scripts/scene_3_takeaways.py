import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from skills.fami_lib import *

class Scene3_Takeaways(FaMIBaseScene):
    def construct(self):
        # 1. KỊCH BẢN
        VO_TEXT = "Từ phương pháp của An, nếu muốn hiểu sâu hơn về cách các hệ thống lọc Spam hoạt động trong thực tế, bạn có thể tìm kiếm cụm từ khóa Naive Bayes Classifier là hệ thống lọc Spam lớn của Google"
        SEARCH_QUERY = "Naive Bayes Classifier"

        # 2. ĐỐI TƯỢNG
        title = self.create_title("TỪ KHÓA QUAN TRỌNG")
        
        # Thanh tìm kiếm
        search_bar = RoundedRectangle(corner_radius=0.2, height=1.2, width=8.0, color=WHITE).move_to(POS_TOP_FOCUS)
        magnifying_glass = SVGMobject("assets/magnifying_glass.svg").set(height=0.6).move_to(search_bar.get_left() + RIGHT * 0.5)
        search_group = VGroup(search_bar, magnifying_glass)

        # Kết quả tìm kiếm
        result_title = MarkupText(f'<u>Naive Bayes Classifier - Hệ thống lọc Spam của <span color="{SUCCESS}">Google</span></u>', font="Segoe UI", font_size=32)
        result_desc = Text("Naive Bayes là một thuật toán phân loại dựa trên định lý Bayes với giả định ngây thơ (naive) về tính độc lập giữa các đặc trưng...", font="Segoe UI", font_size=28)
        search_result_group = VGroup(result_title, result_desc).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(search_group, DOWN, buff=0.5)
        if search_result_group.width > 7.5:
            search_result_group.scale_to_fit_width(7.5)

        # 3. ANIMATION
        self.play(Write(title))
        self.play(FadeIn(search_group, shift=UP*0.5))

        with self.voiceover(text=VO_TEXT) as tracker:
            self.update_subtitle("Tìm kiếm ‘Naive Bayes Classifier’ để hiểu sâu hơn.")
            
            # Hiệu ứng gõ chữ chuẩn
            last_char = magnifying_glass
            current_buff = 0.2
            for char in SEARCH_QUERY:
                if char == " ":
                    current_buff = 0.2
                    continue
                
                new_char = Text(char, font="Segoe UI", font_size=40, color=TEXT_COLOR)
                new_char.next_to(last_char, RIGHT, buff=current_buff, aligned_edge=DOWN)
                new_char.match_y(search_bar)
                self.play(FadeIn(new_char, scale=0.8), run_time=0.08)
                last_char = new_char
                current_buff = 0.05
            
            # Chờ đến gần hết thoại để hiện kết quả
            self.wait(tracker.get_remaining_duration() - 1.5)
            self.play(FadeIn(search_result_group, shift=UP*0.5))

        self.finish_scene()
