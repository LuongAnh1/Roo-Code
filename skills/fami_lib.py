from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService
from deep_translator import GoogleTranslator
import os

# Khởi tạo Translator
translator = GoogleTranslator(source='vi', target='en')

# ==========================================================
# 1. HỆ TỌA ĐỘ KHÓA CỨNG (Đã nới rộng không gian nội dung)
# ==========================================================
POS_TITLE = UP * 5.8          # Đẩy cao hơn (từ 4.2 -> 5.8)
POS_TOP_FOCUS = UP * 3.2      # Nới rộng vùng trên
POS_CENTER = UP * 0.2         # Tâm điểm chính
POS_BOTTOM_FOCUS = DOWN * 2.5 # Hạ thấp vùng dưới
POS_SUBTITLE = DOWN * 5     # Vị trí phụ đề an toàn TikTok
POS_LEFT = LEFT * 2         # Vị trí bố cục Trái
POS_RIGHT = RIGHT * 2       # Vị trí bố cục Phải

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
            self.logo = ImageMobject(logo_path).scale_to_fit_width(1.2) # Thu nhỏ 2.5 -> 1.6
            self.logo.to_edge(UP, buff=0.4) # Đẩy sát lên (0.8 -> 0.4)
        else:
            self.logo = Text("FaMI 1956", font_size=25, color=FAMI_BLUE, weight=BOLD).to_edge(UP, buff=0.4)
        self.add_foreground_mobject(self.logo)
            
        # Khởi tạo vùng chứa Subtitle ẩn
        self.subtitle_obj = Text("", font="Segoe UI", font_size=35).move_to(POS_SUBTITLE)
        self.add_foreground_mobject(self.subtitle_obj)

    # --- HÀM KỸ NĂNG (SKILLS) ---
    
    def update_subtitle(self, vi_text, style="default"):
        """
        Skill: Hiển thị phụ đề song ngữ (Việt - Anh) với nhiều style khác nhau.
        Styles: 'default', 'neon', 'banner', 'minimal', 'cinema'
        """
        # 1. Dịch thuật (Đã sửa lại cú pháp chuẩn của deep_translator)
        try:
            en_text = translator.translate(vi_text)
        except:
            en_text = ""

        en = Paragraph(en_text, font="Arial", font_size=22, color=WHITE, weight=BOLD, alignment="center")
        
        # Tiếng Việt ở dưới: màu vàng, chữ nhỏ hơn một chút, in nghiêng (hoặc bỏ slant=ITALIC nếu không muốn nghiêng)
        vi = Paragraph(vi_text, font="Arial", font_size=18, color=FAMI_SUB, slant=ITALIC, alignment="center")
        
        # Gộp nhóm và sắp xếp: Đưa biến 'en' lên trước 'vi' để tiếng Anh nằm ở trên
        text_group = VGroup(en, vi).arrange(DOWN, buff=0.15)
        
        if text_group.width > 8:
            text_group.scale_to_fit_width(8)

        # 3. Xử lý các Style khác nhau
        full_sub = VGroup()

        if style == "neon":
            vi.set_color(WHITE).set_stroke(FAMI_CYAN, width=2, background=True)
            en.set_color(FAMI_SUB).set_stroke(YELLOW_D, width=1, background=True)
            glow = text_group.copy().set_stroke(FAMI_CYAN, width=8, opacity=0.2)
            full_sub = VGroup(glow, text_group)

        elif style == "banner":
            bg_rect = Rectangle(
                width=config.frame_width, 
                height=text_group.height + 0.6,
                fill_color=FAMI_BLUE,
                fill_opacity=0.9,
                stroke_width=0
            )
            line_top = Line(LEFT, RIGHT, color=FAMI_CYAN, stroke_width=2).scale_to_fit_width(config.frame_width)
            line_bottom = line_top.copy().next_to(bg_rect, DOWN, buff=0)
            line_top.next_to(bg_rect, UP, buff=0)
            full_sub = VGroup(bg_rect, line_top, line_bottom, text_group)

        elif style == "minimal":
            shadow = text_group.copy().set_color(BLACK).shift(0.05 * DOWN + 0.05 * RIGHT).set_opacity(0.5)
            full_sub = VGroup(shadow, text_group)

        elif style == "cinema":
            sub_bg = RoundedRectangle(
                corner_radius=0.3, 
                width=text_group.width + 0.8,
                height=text_group.height + 0.5,
                fill_color="#000000",
                fill_opacity=0.7,
                stroke_width=1,
                stroke_color=GRAY_A
            )
            full_sub = VGroup(sub_bg, text_group)

        else: # style == "default"
            sub_bg = RoundedRectangle(
                corner_radius=0.1,
                width=text_group.width + 0.6,
                height=text_group.height + 0.4,
                fill_color="#1A1A1A",
                fill_opacity=0.8,
                stroke_width=0.5,
                stroke_color=FAMI_CYAN
            )
            full_sub = VGroup(sub_bg, text_group)

        # 4. Cập nhật vị trí và hiển thị
        full_sub.move_to(POS_SUBTITLE)
        self.subtitle_obj.become(full_sub)

    # --- SKILL: TẠO TIÊU ĐỀ ---

    # Skill: Tạo tiêu đề (bản 1)
    def create_title(self, line1, line2="", apply_gradient=True):
        """Skill: Tạo tiêu đề (Tự động Gradient & Đúng vị trí)"""
        if line2:
            # Tách thành 2 đối tượng Text riêng biệt để dễ kiểm soát khoảng cách
            t1 = Text(line1, font="Segoe UI", font_size=45, weight=BOLD)
            t2 = Text(line2, font="Segoe UI", font_size=45, weight=BOLD)
            
            # Dùng arrange(DOWN, buff=...) để chỉnh khoảng cách. 
            # Bạn có thể tăng buff lên 0.4 hoặc 0.5 nếu muốn giãn ra thêm nữa.
            title = VGroup(t1, t2).arrange(DOWN, buff=0.05) 
        else:
            title = Text(line1, font="Segoe UI", font_size=45, weight=BOLD)
        
        # Định vị tiêu đề
        title.move_to(POS_TITLE)
        
        # Ép khung ngang để không bị tràn màn hình
        if title.width > 8.0: # Nới lên 8.0 cho video dọc để chữ to hơn chút
            title.scale_to_fit_width(8.0)
            
        # Áp dụng màu thương hiệu
        if apply_gradient:
            apply_fami_gradient(title)
        else:
            title.set_color(WHITE)
            
        return title

    # Skill: Tạo tiêu đề (bản 2 - Tech Future)
    def create_tech_title(self, line1, line2=""):
        """Tiêu đề phong cách HUD/Công nghệ - Fix lỗi đè Logo"""
        # 1. Tạo text
        t1 = Text(line1, font="Segoe UI", font_size=42, weight=BOLD, color=FAMI_CYAN)
        if line2:
            t2 = Text(line2, font="Segoe UI", font_size=38, weight=BOLD, color=WHITE)
            title_grp = VGroup(t1, t2).arrange(DOWN, buff=0.2)
        else:
            title_grp = t1
            
        # 2. Tạo khung bao quanh trước khi di chuyển vào vị trí
        # buff=0.3 thay vì 0.4 để khung gọn gàng hơn
        box = SurroundingRectangle(title_grp, color=FAMI_CYAN, buff=0.3, stroke_width=2)
        
        # 3. Tạo 4 góc
        corners = VGroup(*[
            Line(box.get_corner(curr) + direction * 0.25, box.get_corner(curr), color=FAMI_CYAN, stroke_width=4)
            for curr, direction in zip([UL, UR, DL, DR], [DR, DL, UR, UL])
        ])
        
        # Gộp tất cả lại thành một khối thống nhất
        full_title_block = VGroup(box, corners, title_grp)
        
        # 4. Đưa toàn bộ khối về vị trí POS_TITLE 
        # (Lúc này POS_TITLE sẽ là tâm của cả cái khung, không phải tâm của dòng chữ)
        full_title_block.move_to(POS_TITLE)
        
        # Kiểm tra nếu khung vẫn quá to, bóp nhỏ lại theo chiều ngang
        if full_title_block.width > 6.8:
            full_title_block.scale_to_fit_width(6.8)
            
        return full_title_block
    
    # Skill: Tạo tiêu đề (bản 3 - Minimalist Gradient) 
    def create_minimal_title(self, line1, line2=""):
        """Tiêu đề tối giản: Gradient mượt, có gạch chân, không đè Logo"""
        # 1. Tạo Text: Dòng 1 to hơn dòng 2 để tạo sự sang trọng (Hierachy)
        t1 = Text(line1, font="Segoe UI", font_size=45, weight=BOLD)
        
        if line2:
            # Dòng 2 nhỏ hơn một chút (38) để tổng thể khối không quá cao
            t2 = Text(line2, font="Segoe UI", font_size=38, weight=BOLD)
            text_block = VGroup(t1, t2).arrange(DOWN, buff=0.15)
        else:
            text_block = t1
            
        # 2. Tạo đường gạch chân (Underline) 
        # Độ dài đường kẻ bằng chiều rộng chữ + một chút lề (0.4)
        underline = Line(LEFT, RIGHT, stroke_width=5).scale_to_fit_width(text_block.width + 0.4)
        underline.next_to(text_block, DOWN, buff=0.2)
        
        # 3. Gộp tất cả lại thành một khối trước khi đổ màu và di chuyển
        full_title = VGroup(text_block, underline)
        
        # 4. Áp dụng Gradient cho toàn bộ khối (bao gồm cả đường gạch chân)
        # Điều này giúp màu sắc chuyển đều từ chữ xuống đường kẻ rất đẹp
        apply_fami_gradient(full_title)
        
        # 5. Đưa về vị trí POS_TITLE (Nhớ dùng POS_TITLE = UP * 5.0 như mình gợi ý ở trên)
        full_title.move_to(POS_TITLE)
        
        # 6. Ép khung ngang để chắc chắn không tràn màn hình điện thoại
        if full_title.width > 8.2:
            full_title.scale_to_fit_width(8.2)
            
        return full_title
    
    # Skill: Tạo tiêu đề (bản 4 - Social Education)
    def create_social_title(self, line1, line2="", highlight_word=""):
        """Tiêu đề Social: Fix lỗi weight=BLACK"""
        # Dùng MarkupText để an toàn nhất với tiếng Việt và highlight
        if highlight_word and highlight_word in line1:
            styled_line1 = line1.replace(highlight_word, f'<span foreground="{ACCENT}">{highlight_word}</span>')
        else:
            styled_line1 = line1

        t1 = MarkupText(styled_line1, font="Segoe UI", font_size=45, weight=BOLD, color=WHITE)
        
        if line2:
            # Dòng 2 dùng Text bình thường cũng được, nhưng weight phải là "BLACK" hoặc BOLD
            t2 = Text(line2, font="Segoe UI", font_size=40, weight=BOLD, color=WHITE)
            bg2 = BackgroundRectangle(t2, color=FAMI_BLUE, fill_opacity=1, buff=0.12)
            line2_grp = VGroup(bg2, t2)
            full_title = VGroup(t1, line2_grp).arrange(DOWN, buff=0.2)
        else:
            full_title = VGroup(t1)
            
        full_title.move_to(POS_TITLE)
        if full_title.width > 8.2:
            full_title.scale_to_fit_width(8.2)
            
        return full_title

    def finish_scene(self):
        """Skill: Kết thúc scene an toàn"""
        self.wait(1)

    def arrange_comparison(self, obj_left, obj_right, buff=0.5):
        """Dịch chuyển mỗi đối tượng ra xa tâm một khoảng buff/2"""
        obj_left.move_to(POS_LEFT + LEFT * (buff / 2))
        obj_right.move_to(POS_RIGHT + RIGHT * (buff / 2))
        return VGroup(obj_left, obj_right)

# KỸ NĂNG DI CHUYỂN (MOTION)
def skill_pop_in(obj):
    return FadeIn(obj, scale=0.5, shift=UP*0.2), rate_functions.ease_out_back

def skill_slide_up(obj):
    return FadeIn(obj, shift=UP*1.5), rate_functions.smooth