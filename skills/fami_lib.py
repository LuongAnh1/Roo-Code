from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService
from googletrans import Translator
import os

# Khởi tạo Translator
translator = Translator()

# ==========================================================
# 1. HỆ TỌA ĐỘ KHÓA CỨNG (Đã nới rộng không gian nội dung)
# ==========================================================
POS_TITLE = UP * 5.8          # Đẩy cao hơn (từ 4.2 -> 5.8)
POS_TOP_FOCUS = UP * 3.2      # Nới rộng vùng trên
POS_CENTER = UP * 0.2         # Tâm điểm chính
POS_BOTTOM_FOCUS = DOWN * 2.5 # Hạ thấp vùng dưới
POS_SUBTITLE = DOWN * 3.8     # Vị trí phụ đề an toàn TikTok

# ==========================================
# 2. CẤU HÌNH & MÀU SẮC THƯƠNG HIỆU
# ==========================================
config.pixel_height, config.pixel_width = 1920, 1080
config.frame_height, config.frame_width = 16.0, 9.0

FAMI_BLUE = "#005BAA"
FAMI_CYAN = "#45C4D9"
FAMI_SUB = "#DFE858"
ACCENT = "#fffa65"
DANGER = "#ff4d4d"
SUCCESS = "#00e676"
TEXT_COLOR = WHITE

# --- SKILL: ĐỔ MÀU GRADIENT ---
def apply_fami_gradient(mobject, colors=None):
    if colors is None:
        colors = [FAMI_CYAN, FAMI_BLUE]
    for submob in mobject.family_members_with_points():
        if len(submob.points) > 0:
            submob.set_color(colors)
    return mobject

# ==========================================
# 3. CLASS CƠ SỞ (BASE SCENE)
# ==========================================
class FaMIBaseScene(VoiceoverScene):
    def setup(self):
        super().setup()
        self.set_speech_service(GTTSService(lang="vi"))
        
        # Logo FaMI (Đã thu nhỏ và đẩy cao)
        logo_path = "assets/fami_logo.png"
        if os.path.exists(logo_path):
            self.logo = ImageMobject(logo_path).scale_to_fit_width(1.6) # Thu nhỏ 2.5 -> 1.6
            self.logo.to_edge(UP, buff=0.4) # Đẩy sát lên (0.8 -> 0.4)
        else:
            self.logo = Text("FaMI 1956", font_size=25, color=FAMI_BLUE, weight=BOLD).to_edge(UP, buff=0.4)
        self.add_foreground_mobject(self.logo)
            
        # Khởi tạo vùng chứa Subtitle ẩn
        self.subtitle_obj = Text("", font="Segoe UI", font_size=35).move_to(POS_SUBTITLE)
        self.add_foreground_mobject(self.subtitle_obj)

    # --- HÀM KỸ NĂNG (SKILLS) ---
    
    def update_subtitle(self, vi_text):
        """Skill: Tự động dịch và hiển thị song ngữ"""
        try:
            en_text = translator.translate(vi_text, src='vi', dest='en').text
        except:
            en_text = ""
        
        vi = Paragraph(vi_text, font="Segoe UI", font_size=35, color=WHITE, weight=BOLD, alignment="center")
        en = Paragraph(en_text, font="Segoe UI", font_size=28, color=FAMI_SUB, slant=ITALIC, alignment="center")
        
        sub_group = VGroup(vi, en).arrange(DOWN, buff=0.1)
        if sub_group.width > 7.5:
            sub_group.scale_to_fit_width(7.5)
            
        sub_group.move_to(POS_SUBTITLE)
        self.subtitle_obj.become(sub_group)

    def create_title(self, line1, line2="", apply_gradient=True):
        """Skill: Tạo tiêu đề (Tự động Gradient & Đúng vị trí)"""
        if line2:
            title = Paragraph(line1, line2, font="Segoe UI", font_size=45, weight=BOLD, alignment="center")
        else:
            title = Text(line1, font="Segoe UI", font_size=45, weight=BOLD)
        
        # Định vị tiêu đề
        title.move_to(POS_TITLE)
        
        # Ép khung ngang
        if title.width > 7.5:
            title.scale_to_fit_width(7.5)
            
        # Áp dụng màu thương hiệu
        if apply_gradient:
            apply_fami_gradient(title)
        else:
            title.set_color(WHITE)
            
        return title

    def finish_scene(self):
        """Skill: Kết thúc scene an toàn"""
        self.wait(1)

    def arrange_comparison(self, obj_left, obj_right):
        """Skill: Khóa cứng bố cục Trái-Phải"""
        obj_left.move_to(POS_LEFT)
        obj_right.move_to(POS_RIGHT)
        return VGroup(obj_left, obj_right)

# KỸ NĂNG DI CHUYỂN (MOTION)
def skill_pop_in(obj):
    return FadeIn(obj, scale=0.5, shift=UP*0.2), rate_functions.ease_out_back

def skill_slide_up(obj):
    return FadeIn(obj, shift=UP*1.5), rate_functions.smooth