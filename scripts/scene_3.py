import sys
import os
import math
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from skills.fami_lib import *

class Scene3_Takeaways(FaMIBaseScene):
    """
    Scene 3: Tóm tắt từ khóa
    - Thanh tìm kiếm Google
    - Typewriter effect for "Naive Bayes Classifier"
    """
    def construct(self):
        # 1. KHỞI TẠO ĐỐI TƯỢNG
        title = self.create_title("TỪ KHÓA TÌM KIẾM", "MỞ RỘNG")

        # Khởi tạo logo Google
        try:
            google_logo = SVGMobject("assets/google.svg")
            google_logo.set_width(3.0)
        except:
            # Fallback nếu không load được SVG
            google_logo = Text("Google", font="Segoe UI", font_size=60, color=WHITE)
        
        google_logo.next_to(title, DOWN, buff=1.0)

        # Khởi tạo thanh tìm kiếm
        search_bar = RoundedRectangle(corner_radius=0.5, color=WHITE, fill_color=BLACK, fill_opacity=0.8, width=7.0, height=1.2)
        search_bar.next_to(google_logo, DOWN, buff=0.8)

        # Icon Kính lúp ở bên trái thanh tìm kiếm làm mốc
        try:
            search_icon = SVGMobject("assets/search.svg", color=WHITE)
            search_icon.set_width(0.6)
        except:
            search_icon = Circle(radius=0.3, color=WHITE)
            
        # Đặt kính lúp ở mép trái bên trong thanh tìm kiếm
        search_icon.move_to(search_bar.get_left() + RIGHT * 0.6)
        
        # Mốc vô hình để căn chữ ngang với kính lúp
        reference_obj = search_icon

        main_content = VGroup(google_logo, search_bar, search_icon)
        # Đảm bảo nội dung không bị tràn
        if main_content.width > 7.5:
            main_content.scale_to_fit_width(7.5)

        # 2. KỊCH BẢN & ĐỒNG BỘ
        with self.voiceover(text="Từ phương pháp của An, nếu muốn hiểu sâu hơn về cách các hệ thống lọc Spam hoạt động trong thực tế, bạn có thể tìm kiếm cụm từ khóa Naive Bayes Classifier là hệ thống lọc Spam lớn của Google") as tracker:
            self.update_subtitle("Từ phương pháp của An, nếu muốn hiểu sâu hơn về cách các hệ thống lọc Spam hoạt động trong thực tế, bạn có thể tìm kiếm cụm từ khóa Naive Bayes Classifier là hệ thống lọc Spam lớn của Google")
            
            # Xuất hiện giao diện (25% thời lượng)
            self.play(
                Write(title),
                FadeIn(google_logo, shift=UP),
                FadeIn(search_bar),
                FadeIn(search_icon),
                run_time=min(2.0, tracker.duration * 0.25)
            )

            # Đợi một chút trong lúc voiceover dẫn dắt tới từ khóa
            self.wait(tracker.duration * 0.2)

            # Hiệu ứng gõ chữ (Typewriter) chiếm khoảng 30% thời gian (khoảng ~2.5s)
            text_str = "Naive Bayes Classifier"
            typing_duration = tracker.duration * 0.3
            time_per_char = typing_duration / len(text_str)
            
            last_char = reference_obj
            current_buff = 0.3 
            typed_chars = VGroup()
            
            for i, char in enumerate(text_str):
                if char == " ":
                    current_buff = 0.2 # Khoảng cách cho dấu cách
                    continue
                new_char = Text(char, font="Segoe UI", font_size=40, color=WHITE)
                new_char.next_to(last_char, RIGHT, buff=current_buff, aligned_edge=DOWN)
                new_char.match_y(reference_obj) # KHÓA CHẾT TRỤC Y THEO MỐC
                
                # Cảnh báo tràn thanh tìm kiếm (bảo vệ an toàn):
                if new_char.get_right()[0] > search_bar.get_right()[0] - 0.5:
                    break # Dừng gõ nếu tràn ra khỏi search bar

                self.play(FadeIn(new_char), run_time=min(0.08, time_per_char))
                typed_chars.add(new_char)
                last_char, current_buff = new_char, 0.05
            
            # Cuối cùng Wiggle nhẹ kính lúp như một hiệu ứng click tìm kiếm
            self.play(Wiggle(search_icon), run_time=tracker.duration * 0.05)

        # 3. KẾT THÚC
        self.wait(1)