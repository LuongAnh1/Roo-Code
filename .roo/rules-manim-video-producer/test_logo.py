from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService
import os

# ==========================================================
# CẤU HÌNH GLOBAL (9:16 TIKTOK/SHORTS)
# ==========================================================
config.pixel_height = 1920
config.pixel_width = 1080
config.frame_height = 16.0
config.frame_width = 9.0

# BẢNG MÀU THƯƠNG HIỆU FaMI
FAMI_BLUE = "#005BAA"
FAMI_CYAN = "#45C4D9"

# ==========================================================
# CLASS CƠ SỞ (Đóng dấu Logo tự động)
# ==========================================================
class FaMIBaseScene(VoiceoverScene):
    def setup(self):
        super().setup()
        self.set_speech_service(GTTSService(lang="vi"))
        
        # Đường dẫn tới file ảnh
        logo_path = "assets/fami_logo.png" 
        # Nếu bạn lưu là file jpg, hãy đổi thành "assets/fami_logo.jpg"
        
        # Kiểm tra xem có file ảnh chưa
        if os.path.exists(logo_path):
            self.logo = ImageMobject(logo_path)
            
            # ĐIỀU CHỈNH ĐỘ TO NHỎ CỦA LOGO Ở ĐÂY:
            # 2.5 là độ rộng tương đối (so với frame_width=9)
            self.logo.scale_to_fit_width(2.5) 
            
            # ĐIỀU CHỈNH KHOẢNG CÁCH SO VỚI MÉP TRÊN Ở ĐÂY:
            # buff=0.5 là cách mép trên nửa đơn vị. 
            # Nếu thấy sát quá, tăng lên buff=0.8 hoặc 1.0
            self.logo.to_edge(UP, buff=0.5) 
            
            self.add_foreground_mobject(self.logo)
        else:
            # Cảnh báo báo lỗi đỏ nếu không tìm thấy file ảnh
            self.logo = Text("KHÔNG TÌM THẤY ẢNH LOGO", color=RED, font_size=30)
            self.logo.to_edge(UP, buff=1.0)
            self.add_foreground_mobject(self.logo)

# ==========================================================
# SCENE TEST GIAO DIỆN
# ==========================================================
class TestLayout(FaMIBaseScene):
    def construct(self):
        # 1. TIÊU ĐỀ BÀI HỌC
        title = Text("BÀI 1: BỐ CỤC VIDEO FA MI", weight=BOLD, font="Segoe UI", font_size=45, color=FAMI_CYAN)
        # Ép tiêu đề phải nằm ngay dưới logo, cách một khoảng buff=0.8
        title.next_to(self.logo, DOWN, buff=0.8)

        # 2. KHU VỰC AN TOÀN CHO HOẠT ẢNH (MAIN STAGE)
        # Vẽ một khung viền đứt nét để bạn dễ hình dung giới hạn
        safe_zone_box = DashedVMobject(Rectangle(width=8.0, height=7.0, color=WHITE))
        safe_zone_box.next_to(title, DOWN, buff=1.0)
        
        box_text = Text("KHU VỰC AN TOÀN\n(Animation diễn ra ở đây)", font="Segoe UI", font_size=30)
        box_text.move_to(safe_zone_box.get_center())

        # 3. KÊU GỌI HÀNH ĐỘNG (Nằm dưới cùng)
        cta_text = Text("Nhớ Subscribe kênh nhé!", font="Segoe UI", font_size=35, color=YELLOW)
        cta_text.to_edge(DOWN, buff=2.0) # buff=2.0 để không bị che bởi Caption TikTok

        # 4. CHẠY HIỆU ỨNG THỬ NGHIỆM
        with self.voiceover(text="Chào mừng các bạn đến với kênh Fa mi 1956.") as tracker:
            self.play(Write(title), run_time=min(1.5, tracker.duration))
            
        with self.voiceover(text="Đây là khu vực an toàn để hiển thị các công thức toán học và hình khối.") as tracker:
            self.play(Create(safe_zone_box), FadeIn(box_text), run_time=tracker.duration)
            
        with self.voiceover(text="Và đây là dòng kêu gọi bình luận nằm ở dưới đáy màn hình.") as tracker:
            self.play(Write(cta_text), run_time=tracker.duration)

        self.wait(2)