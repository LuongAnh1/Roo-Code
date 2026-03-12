from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService
import os

# VỊ TRÍ KHÓA CỨNG (Sử dụng hệ tọa độ chuẩn 9:16)
POS_TITLE = UP * 4.2      
POS_CENTER = UP * 0.5 
POS_LEFT = LEFT * 2.2 + UP * 0.5
POS_RIGHT = RIGHT * 2.2 + UP * 0.5
POS_TOP_FOCUS = UP * 2.0   # Vùng tập trung phía trên
POS_BOTTOM_FOCUS = DOWN * 3.0 # Vùng tập trung phía dưới
POS_SUBTITLE = DOWN * 4.5  # Vùng phụ đề

# KỸ NĂNG DI CHUYỂN CHUẨN (MOTION SKILLS)
def skill_pop_in(obj):
    """Hiệu ứng xuất hiện nảy (Juicy) chuẩn TikTok"""
    return FadeIn(obj, scale=0.5, shift=UP*0.2), rate_functions.ease_out_back

def skill_slide_up(obj):
    """Hiệu ứng trượt từ dưới lên chuyên nghiệp"""
    return FadeIn(obj, shift=UP*1.5), rate_functions.smooth

# ==========================================
# 1. CẤU HÌNH CỐ ĐỊNH (DO NOT CHANGE)
# ==========================================
config.pixel_height = 1920
config.pixel_width = 1080
config.frame_height = 16.0
config.frame_width = 9.0

# BẢNG MÀU THƯƠNG HIỆU
FAMI_BLUE = "#005BAA"
FAMI_CYAN = "#45C4D9"
ACCENT = "#fffa65"
DANGER = "#ff4d4d"
SUCCESS = "#00e676"
TEXT_COLOR = WHITE

# ==========================================
# 2. CLASS CƠ SỞ (BASE SCENE)
# ==========================================
class FaMIBaseScene(VoiceoverScene):
    def setup(self):
        super().setup()
        # Setup giọng đọc mặc định
        self.set_speech_service(GTTSService(lang="vi"))
        
        # Chèn Logo FaMI cố định
        logo_path = "assets/fami_logo.png"
        if os.path.exists(logo_path):
            self.logo = ImageMobject(logo_path).scale_to_fit_width(2.5).to_edge(UP, buff=0.8)
            self.add_foreground_mobject(self.logo)
        else:
            self.logo = Text("FaMI 1956", font_size=30, color=FAMI_BLUE, weight=BOLD).to_edge(UP, buff=0.8)
            self.add_foreground_mobject(self.logo)
            
        # Vùng chứa Subtitle cố định (Y = -4.5)
        self.subtitle_obj = Text("", font="Segoe UI", font_size=35, color=WHITE, weight=BOLD)
        self.subtitle_obj.move_to(DOWN * 4.5)
        self.add_foreground_mobject(self.subtitle_obj)

    # --- CÁC SKILLS (HÀM TIỆN ÍCH) ---
    
    def update_subtitle(self, text):
        """Skill: Cập nhật phụ đề khớp với thoại"""
        self.subtitle_obj.become(
            Text(text, font="Segoe UI", font_size=35, color=WHITE, weight=BOLD)
            .move_to(DOWN * 4.5).scale_to_fit_width(8.0)
        )

    def finish_scene(self):
        """Skill: Kết thúc scene an toàn"""
        self.wait(1)

    def create_title(self, line1, line2=""):
        """Khóa cứng Tiêu đề tại POS_TITLE"""
        title = Paragraph(line1, line2, font="Segoe UI", font_size=45, weight=BOLD, color=WHITE, alignment="center")
        title.move_to(POS_TITLE) 
        return title

    def arrange_comparison(self, obj_left, obj_right, buff=1.0):
        """Skill: Khóa cứng bố cục So sánh (Trái - Phải)"""
        obj_left.move_to(POS_LEFT)
        obj_right.move_to(POS_RIGHT)
        return VGroup(obj_left, obj_right)