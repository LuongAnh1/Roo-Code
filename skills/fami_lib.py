from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService
import os

from manim.utils.color import ManimColor, interpolate_color # Dùng để tạo màu gradient tùy chỉnh nếu cần

from googletrans import Translator # Dùng để dịch text sang tiếng Anh nếu cần (ví dụ cho voiceover tiếng Anh)

# Khởi tạo Translator một lần duy nhất ở đầu file
translator = Translator()

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
FAMI_SUB = "#DFE858"
ACCENT = "#fffa65"
DANGER = "#ff4d4d"
SUCCESS = "#00e676"
TEXT_COLOR = WHITE

# --- ĐỔ MÀU ---

def apply_fami_gradient(mobject, colors=None):
    """
    Skill: Đổ màu Gradient cho Text, MathTex hoặc VGroup.
    Sử dụng màu thương hiệu mặc định nếu không truyền tham số.
    """
    if colors is None:
        colors = ["#56CCF2","#A8E063"] # Dải màu thương hiệu chuẩn
    
    # Lấy tất cả các thành phần con có chứa nét vẽ (glyphs/points)
    # family_members_with_points() quét cả ký tự trong Tex và chữ trong Text
    for submob in mobject.family_members_with_points():
        if len(submob.points) > 0:
            submob.set_color(colors)
    return mobject

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
    
    # def update_subtitle(self, text):
    #     """Skill: Cập nhật phụ đề khớp với thoại"""
    #     new_text = Text(text, font="Segoe UI", font_size=35, color=WHITE, weight=BOLD)
    #     if new_text.width > 8.0:
    #         new_text.scale_to_fit_width(8.0)
    #     new_text.move_to(DOWN * 4.5)
    #     self.subtitle_obj.become(new_text)

    def update_subtitle(self, vi_text, max_width=7.5):
        """
        Skill: Tự động dịch sang tiếng Anh và cập nhật phụ đề song ngữ.
        """
        # Tự động dịch
        try:
            en_text = translator.translate(vi_text, src='vi', dest='en').text
        except:
            en_text = "" # Nếu lỗi mạng thì để trống
        
        # 1. Tiếng Việt (Dòng chính)
        vi_sub = Paragraph(vi_text, font="Segoe UI", font_size=35, color=WHITE, alignment="center")
        
        # 2. Tiếng Anh (Dòng phụ - Nhỏ hơn, màu Cyan, in nghiêng)
        en_sub = Paragraph(en_text, font="Segoe UI", font_size=28, color=FAMI_SUB, slant=ITALIC, alignment="center")
        
        # 3. Gom nhóm và căn lề
        sub_group = VGroup(vi_sub, en_sub).arrange(DOWN, buff=0.1)
        
        # Ép khung
        if sub_group.width > max_width:
            sub_group.scale_to_fit_width(max_width)
            
        sub_group.move_to(DOWN * 3.8)
        self.subtitle_obj.become(sub_group)

    def finish_scene(self):
        """Skill: Kết thúc scene an toàn"""
        self.wait(1)

    def create_title(self, line1, line2="", apply_gradient=True):
        """
        Skill: Tạo tiêu đề chuẩn FaMI.
        - Tự động đổ màu Gradient nếu apply_gradient=True.
        - Vị trí luôn cố định dưới Logo.
        """
        if line2:
            title = Paragraph(line1, line2, font="Segoe UI", font_size=45, weight=BOLD, alignment="center")
        else:
            title = Text(line1, font="Segoe UI", font_size=45, weight=BOLD)
        
        # Đặt vị trí
        title.move_to(POS_TITLE)
        
        # Ép khung
        if title.width > 7.5:
            title.scale_to_fit_width(7.5)
            
        # Tự động áp dụng Gradient nếu được bật
        if apply_gradient:
            # Gọi lại skill apply_fami_gradient đã viết ở trên
            apply_fami_gradient(title)
            
        return title

    def arrange_comparison(self, obj_left, obj_right, buff=1.0):
        """Skill: Khóa cứng bố cục So sánh (Trái - Phải)"""
        obj_left.move_to(POS_LEFT)
        obj_right.move_to(POS_RIGHT)
        return VGroup(obj_left, obj_right)