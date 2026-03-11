from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService
import os
import math

# ==========================================================
# 1. CẤU HÌNH GLOBAL (BẮT BUỘC CHO TIKTOK/SHORTS 9:16)
# ==========================================================
config.pixel_height = 1920
config.pixel_width = 1080
config.frame_height = 16.0
config.frame_width = 9.0

# BẢNG MÀU THƯƠNG HIỆU (Lấy từ Logo FaMI)
FAMI_BLUE = "#005BAA"   # Xanh dương đậm
FAMI_CYAN = "#45C4D9"   # Xanh ngọc/Cyan
ACCENT = "#fffa65"      # Vàng (Dùng để highlight)
DANGER = "#ff4d4d"      # Đỏ (Cảnh báo/Sai)
SUCCESS = "#00e676"     # Xanh lục (Đúng/Thành công)
TEXT_COLOR = "#ffffff"

# ==========================================================
# 2. CLASS CƠ SỞ (BASE CLASS) - ĐÃ CÓ TRONG THƯ VIỆN, KHÔNG CẦN VIẾT LẠI
# ==========================================================
class FaMIBaseScene(VoiceoverScene):
    def setup(self):
        """Hàm này tự động chạy trước mọi hàm construct() của các Scene con"""
        super().setup()
        
        # 1. Tự động setup Giọng đọc
        self.set_speech_service(GTTSService(lang="vi"))
        
        # 2. Tự động chèn Logo FaMI
        try:
            self.logo = ImageMobject("assets/fami_logo.png")
            self.logo.scale_to_fit_width(2.5) 
            self.logo.to_edge(UP, buff=0.5) 
            self.add_foreground_mobject(self.logo) 
        except FileNotFoundError:
            self.logo = Text("FaMI 1956", font_size=30, color=FAMI_BLUE, weight=BOLD)
            self.logo.to_edge(UP, buff=0.5)
            self.add_foreground_mobject(self.logo)
            
        # 3. VÙNG CHỨA SUBTITLE (PHỤ ĐỀ) TỰ ĐỘNG
        self.subtitle = Text("", font="Segoe UI", font_size=35, color=WHITE, weight=BOLD)
        self.subtitle.move_to(DOWN * 4.5) # Vị trí an toàn cho phụ đề
        self.add_foreground_mobject(self.subtitle)

    def update_subtitle(self, text):
        """Hàm dùng để cập nhật chữ phụ đề chạy bên dưới"""
        new_subtitle = Text(text, font="Segoe UI", font_size=35, color=WHITE, weight=BOLD)
        new_subtitle.move_to(DOWN * 4.5)
        if new_subtitle.width > config.frame_width - 1:
            new_subtitle.scale_to_fit_width(config.frame_width - 1)
        self.subtitle.become(new_subtitle)

# ==========================================================
# 3. CÁC PHÂN CẢNH (SCENES)
# ==========================================================

class Scene1_Hook(FaMIBaseScene):
    def construct(self):
        # 1. TIÊU ĐỀ
        title = Paragraph(
            "Làm sao để phân loại", 
            "Email Spam?", 
            font="Segoe UI", 
            font_size=60, 
            weight=BOLD,
            color=TEXT_COLOR,
            alignment="center"
        )
        title.next_to(self.logo, DOWN, buff=0.8)
        envelope = Rectangle(width=3, height=2, color=WHITE, stroke_width=5)
        spam_text = Text("SPAM", font="Segoe UI", font_size=48, color=DANGER, weight=BOLD)
        normal_text = Text("NORMAL", font="Segoe UI", font_size=48, color=SUCCESS, weight=BOLD)
        
        content_group = VGroup(spam_text, envelope, normal_text).arrange(RIGHT, buff=1)
        if content_group.width > 8:
            content_group.scale_to_fit_width(8)
        content_group.next_to(title, DOWN, buff=1.0)

        # 3. MŨI TÊN
        # Phải tạo sau khi content_group đã được định vị
        arrow_spam = Arrow(envelope.get_left(), spam_text.get_right(), color=DANGER, buff=0.2)
        arrow_normal = Arrow(envelope.get_right(), normal_text.get_left(), color=SUCCESS, buff=0.2)

        # 4. HOẠT ẢNH & ĐỒNG BỘ GIỌNG NÓI
        voiceover_text = "Làm sao để phân loại Email Spam?"
        
        with self.voiceover(text=voiceover_text) as tracker:
            self.update_subtitle(voiceover_text)
            
            # Animation
            self.play(
                Write(title), 
                run_time=tracker.duration * 0.3
            )
            self.play(
                FadeIn(content_group, shift=UP*0.5), 
                run_time=tracker.duration * 0.3
            )
            self.play(
                GrowArrow(arrow_spam),
                GrowArrow(arrow_normal),
                run_time=tracker.duration * 0.4
            )
        
        self.wait(1)

class Scene2_MainBody(FaMIBaseScene):
    def construct(self):
        # Lời thoại
        voiceover_text_part1 = "Qua câu chuyện này, ta thấy rằng Định lý Bayes không chỉ là công thức lý thuyết mà còn được ứng dụng trực tiếp trong đời sống."
        voiceover_text_part2 = "Về ưu điểm, đây không phải thuật toán tĩnh, nó có khả năng học từ dữ liệu mới, giảm thiểu việc đánh nhầm email quan trọng thành Spam cùng tốc độ tính toán nhanh"
        voiceover_text_part3 = "Về hạn chế thì Spam ngày nay ngày càng tinh vi."
        voiceover_text_part4 = "Thay vì viết “free”, kẻ gửi có thể viết “fr33”; “f.r.e.e”; “fr€€” làm hệ thống dựa trên từ khóa khó nhận diện."

        # Tiêu đề chung
        title = Text("Ứng dụng của Định lý Bayes", font="Segoe UI", weight=BOLD, font_size=48, color=FAMI_CYAN)
        title.next_to(self.logo, DOWN, buff=0.8)

        # --- Định nghĩa Mobjects trước ---
        pros_title = Text("Ưu điểm", font="Segoe UI", weight=BOLD, font_size=40, color=SUCCESS)
        pro_list = VGroup(
            Text("• Học từ dữ liệu mới", font="Segoe UI", font_size=36, color=TEXT_COLOR),
            Text("• Giảm thiểu sai sót", font="Segoe UI", font_size=36, color=TEXT_COLOR),
            Text("• Tốc độ nhanh", font="Segoe UI", font_size=36, color=TEXT_COLOR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        pros_group = VGroup(pros_title, pro_list).arrange(DOWN, aligned_edge=LEFT, buff=0.5)

        cons_title = Text("Hạn chế", font="Segoe UI", weight=BOLD, font_size=40, color=DANGER)
        cons_list = VGroup(
            Text("Spam ngày càng tinh vi", font="Segoe UI", font_size=36, color=TEXT_COLOR),
            Text("Biến tấu từ khóa: free -> fr33, fr€€", font="Segoe UI", font_size=36, color=TEXT_COLOR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        cons_group = VGroup(cons_title, cons_list).arrange(DOWN, aligned_edge=LEFT, buff=0.5)

        features_group = VGroup(pros_group, cons_group).arrange(DOWN, buff=1.0, aligned_edge=LEFT)
        features_group.next_to(title, DOWN, buff=0.8)

        # --- Animation ---
        with self.voiceover(text=voiceover_text_part1) as tracker:
            self.update_subtitle("Định lý Bayes trong ứng dụng đời sống.")
            self.play(Write(title), run_time=1.5)

        with self.voiceover(text=voiceover_text_part2) as tracker:
            self.update_subtitle("Ưu điểm: Học từ dữ liệu mới, giảm sai sót, nhanh.")
            self.play(FadeIn(pros_group, shift=UP*0.3), run_time=1.5)

        with self.voiceover(text=voiceover_text_part3 + " " + voiceover_text_part4) as tracker:
            self.update_subtitle("Hạn chế: Spam tinh vi, biến tấu từ khóa.")
            self.play(FadeIn(cons_group, shift=UP*0.3), run_time=1.5)

        self.wait(1)




class Scene3_Takeaways(FaMIBaseScene):
    def construct(self):
        voiceover_text = "Từ phương pháp của An, nếu muốn hiểu sâu hơn về cách các hệ thống lọc Spam hoạt động trong thực tế, bạn có thể tìm kiếm cụm từ khóa Naive Bayes Classifier là hệ thống lọc Spam lớn của Google"

        # --- Mobjects ---
        search_bar = RoundedRectangle(corner_radius=0.3, height=1.2, width=8, color=WHITE)
        search_bar.next_to(self.logo, DOWN, buff=2.5)

        magnifying_glass = SVGMobject("assets/magnifying_glass.svg").scale(0.4)
        magnifying_glass.move_to(search_bar.get_left() + RIGHT * 0.6)

        search_text_str = "Naive Bayes Classifier"

        # --- Animation ---
        with self.voiceover(text=voiceover_text) as tracker:
            self.update_subtitle("Để hiểu sâu hơn, hãy tìm...")
            self.play(Create(search_bar), FadeIn(magnifying_glass), run_time=1.5)
            
            self.update_subtitle("...cụm từ khóa Naive Bayes Classifier.")
            # Typing effect
            last_char = magnifying_glass
            current_buff = 0.3
            for i, char_str in enumerate(search_text_str):
                if char_str == ' ':
                    current_buff = 0.2
                    continue
                new_char = Text(char_str, font="Segoe UI", font_size=40, color=TEXT_COLOR)
                new_char.next_to(last_char, RIGHT, buff=current_buff)
                new_char.match_y(search_bar)
                self.play(FadeIn(new_char), run_time=0.08)
                last_char = new_char
                current_buff = 0.08

        self.wait(1)

class Scene4_CTA(FaMIBaseScene):
    def construct(self):
        voiceover_text = "Câu hỏi cuối video dành cho bạn đó là phải xử lý như nào nếu kẻ Spam cố tình viết free thành fr€€?"

        # 1. Sử dụng MarkupText thay vì Text
        # MarkupText dùng thẻ <span> để tô màu cực chuẩn
        question = MarkupText(
            f'Xử lý “<span color="{ACCENT}">fr€€</span>” như thế nào?', 
            font="Segoe UI", 
            font_size=42, 
            weight=BOLD
        )
        question.next_to(self.logo, DOWN, buff=1.5)

        cta_box = RoundedRectangle(corner_radius=0.2, height=1.2, width=7, color=FAMI_CYAN)
        cta_text = Text("Comment câu trả lời!", font="Segoe UI", font_size=36, color=WHITE)
        cta_group = VGroup(cta_box, cta_text).center().shift(DOWN * 2)
        cta_text.move_to(cta_box.get_center())

        with self.voiceover(text=voiceover_text) as tracker:
            self.update_subtitle("Câu hỏi dành cho bạn...")
            self.play(Write(question), run_time=1.5)
            
            # Hiệu ứng nhấn mạnh toàn bộ câu hỏi thay vì tìm ký tự lỗi
            self.play(Indicate(question), run_time=1.0)
            
            self.update_subtitle("Hãy comment câu trả lời của bạn!")
            self.play(
                FadeIn(cta_group, scale=0.5, shift=UP*0.5), 
                rate_func=rate_functions.ease_out_back, 
                run_time=1.0
            )

        self.wait(1)
