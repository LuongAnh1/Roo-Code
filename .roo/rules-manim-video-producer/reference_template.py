from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService
import os
import zlib # Cần thiết cho một số tính năng hash của Manim

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

# ==========================================================
# 2. CLASS CƠ SỞ (BASE CLASS) - BÍ QUYẾT GIỮ LOGO & SUBTITLE
# TUYỆT ĐỐI KHÔNG SỬA CLASS NÀY. Các Scene khác phải kế thừa từ đây.
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
            self.logo.to_edge(UP, buff=0.8) 
            self.add_foreground_mobject(self.logo) 
        except FileNotFoundError:
            self.logo = Text("FaMI 1956", font_size=30, color=FAMI_BLUE, weight=BOLD)
            self.logo.to_edge(UP, buff=0.8)
            self.add_foreground_mobject(self.logo)
            
        # 3. VÙNG CHỨA SUBTITLE (PHỤ ĐỀ) TỰ ĐỘNG
        self.subtitle = Text("", font="Segoe UI", font_size=35, color=WHITE, weight=BOLD)
        self.subtitle.move_to(DOWN * 4.5) # Vị trí vàng, không bị che bởi UI TikTok
        self.add_foreground_mobject(self.subtitle)

    def update_subtitle(self, text):
        """Hàm dùng để cập nhật chữ phụ đề chạy bên dưới"""
        self.subtitle.become(
            Text(text, font="Segoe UI", font_size=35, color=WHITE, weight=BOLD)
            .move_to(DOWN * 4.5)
            .scale_to_fit_width(8.0) # Ép không tràn viền
        )

# ==========================================================
# 3. CÁC PHÂN CẢNH (SCENES)
# Agent LƯU Ý: Phải kế thừa từ `FaMIBaseScene` thay vì `VoiceoverScene`
# ==========================================================

class Scene1_Hook(FaMIBaseScene):
    def construct(self):
        # 1. TIÊU ĐỀ (Có weight=BOLD ở TRONG hàm Paragraph)
        title = Paragraph(
            "Làm sao để phân loại", 
            "Email Spam?", 
            font="Segoe UI", 
            font_size=45, 
            weight=BOLD, # Đặt ở đây là chuẩn
            color=WHITE,
            alignment="center"
        )
        title.next_to(self.logo, DOWN, buff=0.8)

        # 2. ĐỐI TƯỢNG CHÍNH
        envelope = Rectangle(width=2, height=1.5, color=WHITE)
        spam_text = Text("SPAM", font="Segoe UI", font_size=36, color=DANGER)
        normal_text = Text("NORMAL", font="Segoe UI", font_size=36, color=SUCCESS)
        
        content_group = VGroup(spam_text, envelope, normal_text).arrange(RIGHT, buff=0.5)
        if content_group.width > 7.0:
            content_group.scale_to_fit_width(7.0)
        content_group.next_to(title, DOWN, buff=1.5)

        # 3. MŨI TÊN
        arrow_spam = Arrow(envelope.get_left(), spam_text.get_right(), color=DANGER, buff=0.1)
        arrow_normal = Arrow(envelope.get_right(), normal_text.get_left(), color=SUCCESS, buff=0.1)

        # 4. HOẠT ẢNH & ĐỒNG BỘ GIỌNG NÓI CHUẨN XÁC
        text_audio = "Làm sao để phân loại Email Spam?"
        
        with self.voiceover(text=text_audio) as tracker:
            self.update_subtitle(text_audio) # Bật phụ đề
            
            # Chia tỉ lệ chạy Animation dựa trên biến thực tế của Scene
            # Đoạn 1: Hiện tiêu đề (chiếm 40% thời gian)
            self.play(Write(title), run_time=tracker.duration * 0.4)
            
            # Đoạn 2: Hiện Email và chữ (chiếm 30% thời gian)
            self.play(FadeIn(content_group, shift=UP*0.5), run_time=tracker.duration * 0.3)
            
            # Đoạn 3: Bắn mũi tên ra (chiếm 30% thời gian còn lại)
            self.play(
                GrowArrow(arrow_spam), 
                GrowArrow(arrow_normal), 
                run_time=tracker.duration * 0.3
            )
            
            # Lưu ý: Khi ra khỏi khối 'with', Manim sẽ tự động chờ nếu âm thanh chưa dứt.
            # Không cần dùng self.wait(tracker.get_remaining_duration()) để tránh lỗi chờ kép.

        self.wait(1)

class Scene2_MainBody(FaMIBaseScene):
    def construct(self):
        pass