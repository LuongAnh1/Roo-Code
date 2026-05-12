import os, sys
import numpy as np
from PIL import Image

import os
import sys
sys_lib = sys

import subprocess
import ctypes
import numpy as np
import math
from scipy import stats

PROJECT_ROOT = '/Users/doanvinhnhan/Roo-Code'

if os.getcwd() != PROJECT_ROOT:
    os.chdir(PROJECT_ROOT)

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

# Import custom libraries
from skills.fami_lib import *
from skills.fami_assets_helper import *
from skills.fami_effects import *
from skills.bit import BitSequence
from skills.broadcasting import Broadcasting
from skills.receiving import Receiving

config.tex_template = TexTemplate()
config.tex_template.add_to_preamble(r"\usepackage[utf8]{vietnam}")
config.tex_template.add_to_preamble(r"\usepackage{amsmath}")
config.tex_template.add_to_preamble(r"\usepackage{amssymb}")
config.tex_template.add_to_preamble(r"\usepackage{enumitem}")
config.tex_template.add_to_preamble(r"\usepackage{xcolor}")


math_tex_template = TexTemplate()
math_tex_template.add_to_preamble(r"\usepackage{amsmath}")
math_tex_template.add_to_preamble(r"\usepackage{amssymb}")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# HELPER UTILITIES dùng chung toàn bộ video
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

IMG_PATH   = "/Users/doanvinhnhan/Roo-Code/assets/Monalisa.jpg"
MANIM_H    = 4.5
IMAGE_SHIFT = UP * 0.5


def load_image():
    pil_img = Image.open(IMG_PATH)
    return pil_img, pil_img.size

def get_image_pixels(pil_img, rows, cols):
    """Lấy mảng pixel 2D (L mode) bằng PIL resize Box (thực sự lấy từ ảnh)."""
    pil_gray = pil_img.convert('L')
    small = pil_gray.resize((cols, rows), Image.Resampling.BOX)
    return np.array(small)

def get_image_channel_values(pil_img, channel_idx, rows, cols):
    """Lấy mảng giá trị của 1 kênh màu R/G/B bằng PIL resize Box."""
    channel_pil = pil_img.split()[channel_idx]
    small = channel_pil.resize((cols, rows), Image.Resampling.BOX)
    return np.array(small)

def make_bracket(target, direction=LEFT):
    brace = Brace(target, direction=direction)
    return brace


def heat_color(frac):
    """0→dark blue, 0.5→yellow, 1→bright white."""
    frac = max(0.0, min(1.0, frac))
    if frac < 0.5:
        t = frac * 2
        return rgb_to_color([t, t, 0.8*(1-t)])
    else:
        t = (frac - 0.5) * 2
        return rgb_to_color([0.8 + 0.2*t, 0.8 + 0.2*t, t])


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PHẦN 1: Pixel
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class BirthOfPixelScript(FaMIBaseScene): 
    def construct(self):
        # --------------------------------------------------
        # 1. TẢI ẢNH VÀ XỬ LÝ KÍCH THƯỚC
        # --------------------------------------------------
        img_path = "/Users/doanvinhnhan/Roo-Code/assets/Monalisa.jpg"
        
        try:
            pil_img = Image.open(img_path)
        except Exception as e:
            print(f"Lỗi tải ảnh: {e}")
            return

        img_w, img_h = pil_img.size
        aspect_ratio = img_w / img_h
        
        manim_h = 5.0 
        manim_w = manim_h * aspect_ratio
        image_shift = UP * 0.8

        pil_gray = pil_img.convert('L')
        arr_gray = np.array(pil_gray) 
        
        gray_mob = ImageMobject(pil_gray)
        gray_mob.height = manim_h
        gray_mob.shift(image_shift)

        # --------------------------------------------------
        # 2. CÁC HÀM XỬ LÝ LƯỚI VÀ CHIA TÁCH
        # --------------------------------------------------
        def get_pixel_grid_2d(rows, cols):
            grid_2d = []
            cell_h_px = img_h / rows
            cell_w_px = img_w / cols
            rect_h = manim_h / rows
            rect_w = manim_w / cols
            
            # Lấy mảng pixel thực sự từ ảnh
            pixel_data = get_image_pixels(pil_img, rows, cols)
            
            for i in range(rows):
                row_list = []
                for j in range(cols):
                    val = int(pixel_data[i, j])
                    
                    rect = Rectangle(width=rect_w, height=rect_h)
                    rect.set_fill(color=rgb_to_color([val, val, val]), opacity=1)
                    
                    stroke_w = 1.5 if max(rows, cols) <= 16 else (0.5 if max(rows, cols) <= 32 else 0)
                    rect.set_stroke(GRAY, width=stroke_w)
                    
                    x = -manim_w/2 + (j + 0.5) * rect_w
                    y = manim_h/2 - (i + 0.5) * rect_h
                    rect.move_to(RIGHT * x + UP * y + image_shift)
                    row_list.append(rect)
                grid_2d.append(row_list)
            return grid_2d

        def flatten_2d(grid_2d):
            return VGroup(*[item for row in grid_2d for item in row])

        def subdivide_anim(old_2d, new_2d):
            anims = []
            old_rows, old_cols = len(old_2d), len(old_2d[0])
            for i in range(old_rows):
                for j in range(old_cols):
                    parent_cell = old_2d[i][j]
                    children_group = VGroup(
                        new_2d[2*i][2*j], new_2d[2*i][2*j+1],
                        new_2d[2*i+1][2*j], new_2d[2*i+1][2*j+1]
                    )
                    anims.append(ReplacementTransform(parent_cell, children_group))
            return AnimationGroup(*anims)

        def create_pixel_image(rows, cols):
            small = pil_gray.resize((cols, rows), Image.Resampling.BOX)
            pixelated = small.resize((img_w, img_h), Image.Resampling.NEAREST)
            mob = ImageMobject(pixelated)
            mob.height = manim_h
            mob.shift(image_shift) 
            return mob

        # --------------------------------------------------
        # 3. KỊCH BẢN KẾT HỢP VOICEOVER & SUB
        # --------------------------------------------------
        
        title = self.create_title("Bức ảnh trong máy tính thực chất là gì?")
        
        # Tạo khung ảnh ảo (.PNG & .JPG)
        generic_frame = Rectangle(width=5, height=4, color=WHITE).shift(image_shift)
        mountain = Polygon(
            generic_frame.get_corner(DL),
            generic_frame.get_bottom() + UP*2,
            generic_frame.get_corner(DR),
            color=GRAY, fill_opacity=0.3
        )
        sun = Circle(radius=0.5, color=YELLOW, fill_opacity=0.8).move_to(generic_frame.get_corner(UR) + DL*1.2)
        generic_pic = VGroup(generic_frame, mountain, sun)
        
        png_text = Text(".PNG", font_size=40, color=BLUE).move_to(generic_frame.get_center() + LEFT*1.2)
        jpg_text = Text(".JPG", font_size=40, color=ORANGE).move_to(generic_frame.get_center() + RIGHT*1.2)

        # [ĐOẠN 1: HOOK]
        with self.voiceover(text="Có lẽ bạn đã biết các bức ảnh kỹ thuật số, thực ra là các pixel, nhưng bạn có thực sự hiểu các pixel là gì?") as tracker:
            self.update_subtitle("Có lẽ bạn đã biết các bức ảnh kỹ thuật số,\nthực ra là các pixel, nhưng bạn có thực sự hiểu pixel là gì?")
            self.play(Write(title), Create(generic_pic), Write(png_text), Write(jpg_text))

        with self.voiceover(text="Tại sao lại có thể chuyển từ hình ảnh từ thế giới thực trở thành các bức ảnh nằm trong máy tính? Các file J P G, P N G thực ra là gì?") as tracker:
            self.update_subtitle("Tại sao có thể đưa hình ảnh từ thế giới thực vào máy tính?\nCác file JPG, PNG thực ra là gì?")
            self.play(Indicate(png_text), Indicate(jpg_text))

        with self.voiceover(text="Trong video này, tôi sẽ giải thích cho các bạn về các khái niệm này! Đầu tiên, ta cùng tìm hiểu định nghĩa cơ bản nhất của một hình ảnh kỹ thuật số.") as tracker:
            self.update_subtitle("Trong video này, tôi sẽ giải thích về các khái niệm này!\nĐầu tiên, hãy tìm hiểu định nghĩa cơ bản của hình ảnh kỹ thuật số.")
            self.play(FadeOut(generic_pic, png_text, jpg_text, title))
        
        # [ĐOẠN 2: ĐỊNH NGHĨA VẬT LÝ VÀ HÀM SỐ]
        func_text = Text("f(x, y)", font_size=40, slant=ITALIC).next_to(gray_mob, RIGHT, buff=0.5)
        func_arrow = Arrow(gray_mob.get_right(), func_text.get_left(), buff=0.2, color=YELLOW)
        
        # Tạo trục x, y bám sát viền ảnh
        axes_origin = gray_mob.get_corner(DL)
        x_axis = Line(axes_origin, axes_origin + RIGHT*(manim_w + 0.5), color=BLUE).add_tip()
        y_axis = Line(axes_origin, axes_origin + UP*(manim_h + 0.5), color=RED).add_tip()
        
        x_label = Text("x", font_size=32, slant=ITALIC).next_to(x_axis.get_end(), DOWN)
        y_label = Text("y", font_size=32, slant=ITALIC).next_to(y_axis.get_end(), LEFT)
        axes_group = VGroup(x_axis, y_axis, x_label, y_label)

        with self.voiceover(text="Một hình ảnh ở không gian vật lý có thể được định nghĩa là một hàm số f(x,y) trong đó x và y là các tọa độ không gian liên tục trong thế giới thực, giá trị của hàm số tại x,y được gọi là cường độ ánh sáng hay mức xám.") as tracker:
            self.update_subtitle("Hình ảnh vật lý được định nghĩa là hàm số f(x,y),\nvới x, y là các tọa độ không gian liên tục.")
            
            self.play(FadeIn(gray_mob))
            self.play(Create(axes_group), run_time=1)
            self.play(Write(func_text), Create(func_arrow))
            
            # Lưu lại trạng thái ảnh gốc để khôi phục sau khi Zoom
            gray_mob.save_state()
            self.bring_to_front(gray_mob) 
                        
        # [ĐOẠN 3: XẤP XỈ RỜI RẠC]
        discrete_text = Text("Xấp xỉ bằng tập hợp hữu hạn rời rạc", font_size=24, color=RED_B).next_to(gray_mob, DOWN, buff=0.4)
        
        with self.voiceover(text="Và ta đều biết, máy tính chỉ có thể lưu trữ các tập hợp hữu hạn. Do nguyên nhân đó, ta xấp xỉ không gian x,y và hàm số f(x,y) bằng các đại lượng rời rạc, cách đều nhau và hữu hạn.") as tracker:
            self.update_subtitle("Máy tính chỉ lưu trữ tập hợp hữu hạn.\nDo đó ta xấp xỉ hàm số bằng đại lượng rời rạc, hữu hạn.")
            
            self.play(Restore(gray_mob), run_time=1.5) 
            self.play(FadeOut(axes_group, func_arrow, func_text)) 
            self.play(Write(discrete_text))

        with self.voiceover(text="Hàm số không gian liên tục - Hình ảnh vật lý này từ đó chuyển đổi thành Hàm số rời rạc - một hình ảnh kỹ thuật số.") as tracker:
            self.update_subtitle("Hàm số không gian liên tục từ đó chuyển đổi thành\nHàm số rời rạc - một hình ảnh kỹ thuật số.")

        with self.voiceover(text="Và magic bắt đầu ở đây, quá trình chuyển đổi từ liên tục sang rời rạc này được thực hiện thông qua hai bước cốt lõi:") as tracker:
            self.update_subtitle("Magic bắt đầu ở đây, quá trình chuyển đổi từ 'liên tục'\nsang 'rời rạc' được thực hiện qua hai bước cốt lõi:")
            self.play(FadeOut(discrete_text))

        # [ĐOẠN 4: LẤY MẪU & LƯỢNG TỬ HÓA]
        step1_title = Text("1. Lấy mẫu - Sự ra đời của Pixel", font_size=32, color=YELLOW).next_to(gray_mob, DOWN, buff=0.5)
        grid_lines = NumberPlane(
            x_range=[-manim_w/2, manim_w/2, manim_w/8], y_range=[-manim_h/2, manim_h/2, manim_h/8],
            background_line_style={"stroke_color": WHITE, "stroke_width": 2, "stroke_opacity": 0.8}
        ).move_to(gray_mob.get_center())

        with self.voiceover(text="1. Lấy mẫu - Sự ra đời của Pixel: Hãy tưởng tượng bạn đặt một tấm lưới lên trên bức ảnh vật lý thực tế.") as tracker:
            self.update_subtitle("1. Lấy mẫu: Tưởng tượng bạn đặt một tấm lưới\nlên trên bức ảnh vật lý thực tế.")
            self.play(Write(step1_title))
            self.play(Create(grid_lines), run_time=2)

        with self.voiceover(text="Mỗi ô vuông nhỏ trên tấm lưới đó sẽ đại diện cho một tọa độ không gian rời rạc. Ta gọi mỗi ô vuông này là một Pixel, viết tắt của Picture Element.") as tracker:
            self.update_subtitle("Mỗi ô vuông nhỏ đại diện cho một tọa độ không gian rời rạc.\nTa gọi mỗi ô vuông này là một Pixel.")

        step2_title = Text("2. Lượng tử hóa", font_size=32, color=YELLOW)
        matrix_desc = Text("Ma trận 2 chiều chứa số nguyên (0 - 255)", font_size=24, color=GREEN_C)
        step2_group = VGroup(step2_title, matrix_desc).arrange(DOWN, buff=0.2).next_to(gray_mob, DOWN, buff=0.4)
        
        grid_8x8 = get_pixel_grid_2d(8, 8)
        vgroup_8x8 = flatten_2d(grid_8x8)
        
        numbers_group = VGroup()
        for row in grid_8x8:
            for rect in row:
                color_rgb = color_to_rgb(rect.get_fill_color())
                val = int(color_rgb[0] * 255)
                num_text = Text(str(val), font_size=16)
                num_text.set_color(BLACK if val > 127 else WHITE)
                num_text.move_to(rect.get_center())
                numbers_group.add(num_text)
                
        left_bracket = Text("[", font_size=180, weight=BOLD).next_to(vgroup_8x8, LEFT, buff=0.1)
        right_bracket = Text("]", font_size=180, weight=BOLD).next_to(vgroup_8x8, RIGHT, buff=0.1)

        with self.voiceover(text="2. Lượng tử hóa: Ta thực hiện gán một số nguyên đại diện cho cường độ tại pixel đó, thông thường nằm trong khoảng 0 đến 255.") as tracker:
            self.update_subtitle("2. Lượng tử hóa: Ta gán một số nguyên đại diện\ncho cường độ tại pixel đó (0 - 255).")
            self.play(ReplacementTransform(step1_title, step2_group[0]))
            self.play(FadeOut(gray_mob), FadeOut(grid_lines), FadeIn(vgroup_8x8))
            self.play(FadeIn(numbers_group))

        with self.voiceover(text="Vậy là một bức ảnh đen trắng trong máy tính, thực chất chỉ là một ma trận 2 chiều chứa các con số 0 đến 255.") as tracker:
            self.update_subtitle("Vậy là một bức ảnh trong máy tính thực chất chỉ là\nmột ma trận 2 chiều chứa các con số 0 đến 255.")
            self.play(Write(left_bracket), Write(right_bracket), FadeIn(step2_group[1]))

        # [ĐOẠN 5: ĐỘ PHÂN GIẢI]
        res_title = Text("Độ phân giải (Resolution)", font_size=32, color=YELLOW)
        res_desc = Text("Lưới càng nhỏ, pixel càng nhiều -> Xấp xỉ càng sát thực tế", font_size=24, color=WHITE)
        res_group = VGroup(res_title, res_desc).arrange(DOWN, buff=0.2).next_to(vgroup_8x8, DOWN, buff=0.4)
        
        grid_16x16 = get_pixel_grid_2d(16, 16)
        grid_32x32 = get_pixel_grid_2d(32, 32)

        with self.voiceover(text="Và nếu bạn tăng số ô chia lưới lên, lưới càng được chia nhỏ, số lượng pixel càng nhiều, thì bức ảnh kỹ thuật số càng chi tiết và xấp xỉ càng sát với hình ảnh trong thế giới thực.") as tracker:
            self.update_subtitle("Nếu tăng số ô chia lưới, số lượng pixel càng nhiều,\nthì bức ảnh càng chi tiết và sát với thực tế.")
            self.play(
                ReplacementTransform(step2_group, res_group),
                FadeOut(numbers_group), FadeOut(left_bracket), FadeOut(right_bracket)
            )
            self.play(subdivide_anim(grid_8x8, grid_16x16), run_time=1.5)
            self.play(subdivide_anim(grid_16x16, grid_32x32), run_time=1.5)

        with self.voiceover(text="Đó chính là lý do ta gọi số lượng ô chiều ngang và chiều dọc là độ phân giải.") as tracker:
            self.update_subtitle("Đó chính là lý do ta gọi số lượng ô chiều ngang\nvà chiều dọc là Độ phân giải.")
            img_64x64 = create_pixel_image(64, 64)
            vgroup_32x32 = flatten_2d(grid_32x32)
            self.play(FadeOut(vgroup_32x32), FadeIn(img_64x64), run_time=0.5)
            
            current_img_mob = img_64x64
            max_res = min(img_w // 2, img_h // 2)
            curr_val = 128
            
            while curr_val <= max_res:
                next_img_mob = create_pixel_image(curr_val, curr_val)
                self.play(FadeIn(next_img_mob), run_time=0.3)
                self.remove(current_img_mob)
                current_img_mob = next_img_mob
                curr_val *= 2
                
            if curr_val / 2 != max_res:
                final_img_mob = create_pixel_image(max_res, max_res)
                self.play(FadeIn(final_img_mob), run_time=0.3)
                self.remove(current_img_mob)
                current_img_mob = final_img_mob
                
            self.play(
                FadeOut(current_img_mob), FadeOut(res_group), FadeOut(step1_title),
                run_time=1.0
            )

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PHẦN 2: RGB TENSOR & DỮ LIỆU
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━



# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PHẦN 2: RGB TENSOR – MA TRẬN CHỒNG TRỰC TIẾP LÊN MONALISA
# Layout: Ảnh nhỏ bên trái, 3 kênh R/G/B chồng lên ảnh, công thức bên phải
# Vùng Y: -3.5 đến +4.0 (tuyệt đối không vượt)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class RGBTensorScene(FaMIBaseScene):
    """
    Phần 2: Minh họa cấu trúc Tensor RGB trực tiếp trên ảnh Monalisa.
    Chiến lược: Ảnh ở trung tâm-trái, 3 ma trận kênh màu hiện ra xếp chồng
    lên ảnh theo hiệu ứng 3D giả, công thức tensor ở bên phải/dưới.
    """

    def construct(self):
        pil_img, (img_w, img_h) = load_image()
        arr_rgb = np.array(pil_img.convert('RGB'))

        # ── Constants ────────────────────────────────────────────────────────
        # Ảnh Monalisa thu nhỏ đặt bên trái, cao 4.5 units trong golden zone
        IMG_H      = 4.2   # chiều cao ảnh trong Manim units
        IMG_ASPECT = img_w / img_h
        IMG_W      = IMG_H * IMG_ASPECT
        IMG_POS    = LEFT * 2.0 + UP * 0.3  # tâm ảnh (Y=0.3, nằm trong golden zone)

        # Ma trận 8×8 overlay đặt chồng lên ảnh
        ROWS, COLS = 8, 8
        CELL_H     = IMG_H / ROWS
        CELL_W     = IMG_W / COLS

        # ── Tiêu đề ──────────────────────────────────────────────────────────
        title = self.create_title("PHẦN 2: THÊM MÀU SẮC", "RGB Tensor")

        # ── Chuẩn bị hàm hỗ trợ tạo lưới Grid giống Phần 1 ───────────────────
        from PIL import Image as PILImage
        
        def create_grid_2d(cols, rows, channel_idx=None, target_w=IMG_W, target_h=IMG_H, center_pos=IMG_POS, fill_opacity=1.0, stroke_opacity=1.0):
            grid_2d = []
            rect_h = target_h / rows
            rect_w = target_w / cols
            
            if channel_idx == -1:
                small_pil = pil_img.resize((cols, rows), PILImage.Resampling.BOX)
                pixel_data = np.array(small_pil)
            elif channel_idx is None:
                pixel_data = get_image_pixels(pil_img, rows, cols)
            else:
                pixel_data = get_image_channel_values(pil_img, channel_idx, rows, cols)
                
            for i in range(rows):
                row_list = []
                for j in range(cols):
                    if channel_idx == -1:
                        r, g, b = pixel_data[i, j]
                        color = rgb_to_color([r, g, b])
                    elif channel_idx is None:
                        val = int(pixel_data[i, j])
                        color = rgb_to_color([val, val, val])
                    else:
                        val = int(pixel_data[i, j])
                        color_arr = [0, 0, 0]
                        color_arr[channel_idx] = val
                        color = rgb_to_color(color_arr)
                        
                    rect = Rectangle(width=rect_w, height=rect_h)
                    rect.set_fill(color=color, opacity=fill_opacity)
                    
                    stroke_w = 1.5 if max(rows, cols) <= 16 else (0.5 if max(rows, cols) <= 32 else 0)
                    if channel_idx is not None and channel_idx != -1:
                        rect.set_stroke(WHITE, width=0.3, opacity=0.6 * stroke_opacity)
                    else:
                        rect.set_stroke(GRAY, width=stroke_w, opacity=stroke_opacity)
                        
                    x = -target_w/2 + (j + 0.5) * rect_w
                    y = target_h/2 - (i + 0.5) * rect_h
                    rect.move_to(center_pos + RIGHT * x + UP * y)
                    row_list.append(rect)
                grid_2d.append(row_list)
            return grid_2d

        def flatten_2d(grid_2d):
            return VGroup(*[item for row in grid_2d for item in row])

        def subdivide_anim(old_2d, new_2d):
            anims = []
            old_rows, old_cols = len(old_2d), len(old_2d[0])
            for i in range(old_rows):
                for j in range(old_cols):
                    parent_cell = old_2d[i][j]
                    children_group = VGroup(
                        new_2d[2*i][2*j], new_2d[2*i][2*j+1],
                        new_2d[2*i+1][2*j], new_2d[2*i+1][2*j+1]
                    )
                    anims.append(ReplacementTransform(parent_cell, children_group))
            return AnimationGroup(*anims)

        # ── Chuẩn bị ảnh Manim ───────────────────────────────────────────────
        mono_grid = create_grid_2d(COLS, ROWS, channel_idx=None)
        mono_mob = flatten_2d(mono_grid)

        with self.voiceover("Tiếp theo, ta sẽ cùng đi phủ màu cho hình ảnh này.") as tr:
            self.update_subtitle("Tiếp theo, ta sẽ phủ màu cho hình ảnh này.")
            self.play(Write(title), FadeIn(mono_mob), run_time=min(1.5, tr.duration * 0.8))

        # ── Hàm tạo lưới ô màu cho 1 kênh, xếp chồng lên vị trí ảnh ────────
        def make_overlay_channel(channel_idx, offset_3d):
            grid_2d = create_grid_2d(COLS, ROWS, channel_idx, fill_opacity=0.85)
            cells = flatten_2d(grid_2d)
            cells.shift(offset_3d)
            
            nums = VGroup()
            if channel_idx == 0:
                pixel_data = get_image_channel_values(pil_img, channel_idx, ROWS, COLS)
                for i in range(ROWS):
                    for j in range(COLS):
                        val = int(pixel_data[i, j])
                        rect = grid_2d[i][j]
                        t = Text(str(val), font_size=6, color=WHITE if val < 160 else BLACK)
                        t.move_to(rect.get_center())
                        nums.add(t)

            return cells, nums

        # Tạo 3 lớp kênh màu với offset 3D giả
        STACK = np.array([0.22, -0.14, 0])   # shift mỗi lớp
        R_cells, R_nums = make_overlay_channel(0, STACK * 2)
        G_cells, G_nums = make_overlay_channel(1, STACK * 1)
        B_cells, B_nums = make_overlay_channel(2, STACK * 0)

        # ── Nhãn kênh màu ────────────────────────────────────────────────────
        label_R = Text("R", font_size=32, color=RED,   weight=BOLD)
        label_G = Text("G", font_size=32, color=GREEN, weight=BOLD)
        label_B = Text("B", font_size=32, color=BLUE,  weight=BOLD)
        label_R.next_to(R_cells, UP, buff=0.15)
        label_G.next_to(G_cells, UP, buff=0.15)
        label_B.next_to(B_cells, UP, buff=0.15)

        # Brace cho chiều sâu
        all_channels = VGroup(R_cells, G_cells, B_cells)
        depth_brace = Brace(all_channels, RIGHT, color=WHITE, buff=0.1)
        depth_label = Text("Depth=3", font_size=18, color=WHITE)
        depth_brace.put_at_tip(depth_label)

        # ── Công thức Tensor ở bên phải ──────────────────────────────────────
        RIGHT_X = RIGHT * 3.0
        tensor_eq = MathTex(
            r"\mathbf{T} \in \mathbb{R}^{H \times W \times 3}",
            font_size=30, color=FAMI_CYAN, tex_template=math_tex_template
        ).move_to(RIGHT_X + UP * 1.8)

        channel_eqs = VGroup(
            MathTex(r"T[:,:,0] = \mathbf{R}", font_size=22, color=RED,   tex_template=math_tex_template),
            MathTex(r"T[:,:,1] = \mathbf{G}", font_size=22, color=GREEN, tex_template=math_tex_template),
            MathTex(r"T[:,:,2] = \mathbf{B}", font_size=22, color=BLUE,  tex_template=math_tex_template),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        channel_eqs.next_to(tensor_eq, DOWN, buff=0.4)

        # Giới hạn nhóm công thức không vượt quá bên phải
        formula_group = VGroup(tensor_eq, channel_eqs)
        if formula_group.width > 3.5:
            formula_group.scale_to_fit_width(3.5)
        formula_group.move_to(RIGHT * 3.2 + UP * 0.8)

        # Kiểm tra không vượt khung Y
        if formula_group.get_top()[1] > 3.8:
            formula_group.shift(DOWN * (formula_group.get_top()[1] - 3.8))
        if formula_group.get_bottom()[1] < -3.3:
            formula_group.scale_to_fit_height(7.1)
            formula_group.move_to(RIGHT * 3.2)

        # ── KỊCH BẢN ANIMATION ───────────────────────────────────────────────

        with self.voiceover(
            "Về mặt toán học, thay vì một ma trận 2 chiều đơn lẻ, "
            "một bức ảnh màu là một cấu trúc dữ liệu ba chiều – một Tensor."
        ) as tr:
            self.update_subtitle("Ảnh màu là cấu trúc dữ liệu ba chiều – một Tensor.")
            # Lớp B xuất hiện đầu tiên (layer nền)
            self.play(FadeIn(B_cells), Write(label_B), run_time=min(1.0, tr.duration * 0.5))
            self.play(Write(tensor_eq), run_time=min(0.8, tr.duration * 0.3))

        with self.voiceover(
            "Nó bao gồm 3 ma trận xếp chồng lên nhau tương ứng với "
            "ba kênh màu Đỏ, Xanh lục và Xanh lam – không gian màu RGB."
        ) as tr:
            self.update_subtitle("3 ma trận xếp chồng: kênh Đỏ, Xanh lục, Xanh lam – RGB.")
            # Lần lượt xuất hiện từng kênh với hiệu ứng xếp chồng
            self.play(FadeIn(G_cells), Write(label_G),
                      Write(channel_eqs[2]), run_time=min(1.0, tr.duration * 0.3))
            self.play(FadeIn(R_cells), Write(label_R),
                      Write(channel_eqs[1]), Write(channel_eqs[0]),
                      run_time=min(1.0, tr.duration * 0.3))
            self.play(Create(depth_brace), Write(depth_label), run_time=min(0.8, tr.duration * 0.2))

        # ── Hiện số lên kênh R (minh họa giá trị ma trận) ────────────────────
        with self.voiceover(
            "Sự phối hợp cường độ của 3 kênh này tại cùng một tọa độ x,y "
            "đánh lừa tế bào hình nón trong mắt bạn, tạo ra hàng triệu màu sắc."
        ) as tr:
            self.update_subtitle("Phối hợp R+G+B tại (x,y) đánh lừa mắt người,\ntạo hàng triệu màu sắc.")
            self.play(FadeIn(R_nums), run_time=min(0.8, tr.duration * 0.3))
            # Highlight một ô ví dụ
            example_cell = R_cells[3 * COLS + 3]   # ô (3,3) của kênh R
            hl = SurroundingRectangle(example_cell, color=YELLOW, buff=0.03, stroke_width=2)
            self.play(Create(hl), run_time=min(0.5, tr.duration * 0.2))
            self.play(FadeOut(hl), run_time=0.3)

        # ── Chuyển sang ảnh màu đầy đủ ───────────────────────────────────────
        color_grid_8x8 = create_grid_2d(COLS, ROWS, channel_idx=-1)
        color_mob = flatten_2d(color_grid_8x8)

        # Kết hợp 3 kênh → ảnh màu
        combined_label = Text("Kết hợp → Ảnh màu đầy đủ!", font_size=24, color=SUCCESS)
        combined_label.next_to(color_mob, DOWN, buff=0.25)
        if combined_label.get_bottom()[1] < -3.4:
            combined_label.move_to(IMG_POS + DOWN * (IMG_H/2 - 0.3))

        with self.voiceover(
            "Khối dữ liệu ba chiều này gọi là Tensor – "
            "nền tảng của mọi ảnh màu kỹ thuật số."
        ) as tr:
            self.update_subtitle("Khối 3 chiều này là Tensor –\nnền tảng của mọi ảnh màu kỹ thuật số.")
            self.play(
                FadeOut(R_cells), FadeOut(G_cells), FadeOut(B_cells),
                FadeOut(R_nums), FadeOut(depth_brace), FadeOut(depth_label),
                FadeOut(label_R), FadeOut(label_G), FadeOut(label_B),
                FadeOut(mono_mob),
                run_time=0.8
            )
            self.play(FadeIn(color_mob), run_time=min(1.0, tr.duration * 0.4))
            self.play(Write(combined_label), run_time=min(0.8, tr.duration * 0.3))

        # ── Tách thành 4 ma trận và tăng độ phân giải ────────────────────────
        with self.voiceover(
            "Nhưng nếu chúng ta nhìn kỹ hơn, ta sẽ thấy rằng các ma trận thực chất "
            "vẫn lưu trữ độc lập. Bây giờ, hãy xem điều gì xảy ra khi độ phân giải tăng lên."
        ) as tr:
            self.update_subtitle("Nhìn kỹ hơn, các ma trận vẫn lưu trữ độc lập.\nHãy xem điều gì xảy ra khi độ phân giải tăng lên.")
            
            # FadeOut combined_label TRƯỚC
            self.play(FadeOut(combined_label), run_time=0.3)
            
            # Tách color_mob và sinh ra R_mob, G_mob, B_mob
            target_h = 2.0
            target_w = target_h * (IMG_W / IMG_H)
            
            C_grid_8 = create_grid_2d(COLS, ROWS, -1, target_w, target_h, DOWN * 1.5)
            R_grid_8 = create_grid_2d(COLS, ROWS, 0, target_w, target_h, DOWN * 1.5)
            G_grid_8 = create_grid_2d(COLS, ROWS, 1, target_w, target_h, DOWN * 1.5)
            B_grid_8 = create_grid_2d(COLS, ROWS, 2, target_w, target_h, DOWN * 1.5)
            
            C_mob_8 = flatten_2d(C_grid_8)
            R_mob_8 = flatten_2d(R_grid_8)
            G_mob_8 = flatten_2d(G_grid_8)
            B_mob_8 = flatten_2d(B_grid_8)
            
            # Thay thế color_mob bằng phiên bản nhỏ
            self.play(ReplacementTransform(color_mob, C_mob_8), run_time=0.6)
            
            # Khởi tạo R, G, B từ C
            self.add(R_mob_8, G_mob_8, B_mob_8)
            
            self.play(
                R_mob_8.animate.move_to(UP * 1.2 + LEFT * 3.5),
                G_mob_8.animate.move_to(UP * 1.2),
                B_mob_8.animate.move_to(UP * 1.2 + RIGHT * 3.5),
                run_time=min(1.0, tr.duration * 0.3)
            )
            
            # Thêm mũi tên hướng vào ảnh dưới
            arrow_R = Arrow(R_mob_8.get_bottom(), C_mob_8.get_left() + UP*0.5, buff=0.1, color=WHITE)
            arrow_G = Arrow(G_mob_8.get_bottom(), C_mob_8.get_top(), buff=0.1, color=WHITE)
            arrow_B = Arrow(B_mob_8.get_bottom(), C_mob_8.get_right() + UP*0.5, buff=0.1, color=WHITE)
            arrows = VGroup(arrow_R, arrow_G, arrow_B)
            
            self.play(Create(arrows), run_time=0.5)
            
            # Tăng độ phân giải dần dần 8 -> 16 -> 32
            resolutions = [16, 32]
            current_grids = [R_grid_8, G_grid_8, B_grid_8, C_grid_8]
            current_mobs = [R_mob_8, G_mob_8, B_mob_8, C_mob_8]
            
            for res in resolutions:
                new_R = create_grid_2d(res, res, 0, target_w, target_h, current_mobs[0].get_center())
                new_G = create_grid_2d(res, res, 1, target_w, target_h, current_mobs[1].get_center())
                new_B = create_grid_2d(res, res, 2, target_w, target_h, current_mobs[2].get_center())
                new_C = create_grid_2d(res, res, -1, target_w, target_h, current_mobs[3].get_center())
                
                new_grids = [new_R, new_G, new_B, new_C]
                
                self.play(
                    subdivide_anim(current_grids[0], new_grids[0]),
                    subdivide_anim(current_grids[1], new_grids[1]),
                    subdivide_anim(current_grids[2], new_grids[2]),
                    subdivide_anim(current_grids[3], new_grids[3]),
                    run_time=min(0.8, tr.duration * 0.2)
                )
                current_grids = new_grids
                current_mobs = [flatten_2d(g) for g in new_grids]
                
            # Cuối cùng là độ phân giải thật (sử dụng ImageMobject để tránh lag cho 64+)
            def get_full_res_channel(channel_idx):
                channel_arr = np.zeros_like(arr_rgb)
                channel_arr[:, :, channel_idx] = arr_rgb[:, :, channel_idx]
                pil_channel = PILImage.fromarray(channel_arr, mode='RGB')
                return ImageMobject(pil_channel)
            
            final_R = get_full_res_channel(0).set_height(target_h).move_to(current_mobs[0].get_center())
            final_G = get_full_res_channel(1).set_height(target_h).move_to(current_mobs[1].get_center())
            final_B = get_full_res_channel(2).set_height(target_h).move_to(current_mobs[2].get_center())
            final_C = ImageMobject(pil_img).set_height(target_h).move_to(current_mobs[3].get_center())
            
            final_mobs = [final_R, final_G, final_B, final_C]
            
            self.play(
                *[FadeOut(m) for m in current_mobs],
                *[FadeIn(m) for m in final_mobs],
                run_time=min(0.8, tr.duration * 0.2)
            )
            
            R_mob, G_mob, B_mob, color_mob = final_mobs
            arrows_group = arrows

        # ── Phần dữ liệu thô và giải pháp nén ───────────────────────────────
        self.play(
            FadeOut(color_mob), FadeOut(R_mob), FadeOut(G_mob), FadeOut(B_mob),
            FadeOut(formula_group), FadeOut(arrows_group),
            run_time=0.6
        )

        # Layout vùng tính toán: 3 dòng, mỗi dòng 1 công thức/số
        W_VAL, H_VAL = 2880, 1800
        raw_MB_display = 47.0

        size_formula = MathTex(
            r"2880 \times 1800 \times 3 = 15{,}552{,}000 \approx 47 \text{ MB}",
            font_size=26,
            tex_template=math_tex_template
        ).move_to(UP * 2.2)
        if size_formula.width > 8.0:
            size_formula.scale_to_fit_width(8.0)

        counter_label = Text("Kích thước ảnh đơn:", font_size=24, color=GRAY_A)
        counter_val   = DecimalNumber(0, num_decimal_places=1, font_size=48, color=GREEN_C)
        counter_unit  = Text(" MB", font_size=36, color=GREEN_C)
        counter_row   = VGroup(counter_val, counter_unit).arrange(RIGHT, buff=0.05)
        counter_block = VGroup(counter_label, counter_row).arrange(DOWN, buff=0.15)
        counter_block.next_to(size_formula, DOWN, buff=0.4)

        video_warn = Text(
            "1 giây video 60fps  ≈  2.75 GB  🔥",
            font_size=26, color=RED
        )
        video_warn.next_to(counter_block, DOWN, buff=0.35)
        if video_warn.get_bottom()[1] < -3.3:
            video_warn.next_to(counter_block, DOWN, buff=0.2)

        full_block = VGroup(size_formula, counter_block, video_warn)
        if full_block.get_bottom()[1] < -3.4:
            full_block.scale_to_fit_height(6.5)
            full_block.move_to(UP * 0.3)

        with self.voiceover(
            "Tuy nhiên, nếu giữ nguyên một bức ảnh độ phân giải 2880 nhân 1800 "
            "ở dạng ma trận RGB nguyên bản, nó đã có kích thước xấp xỉ 47MB."
        ) as tr:
            self.update_subtitle("Ảnh 2880×1800 RGB nguyên bản ≈ 47 MB.")
            self.play(Write(size_formula), run_time=min(1.2, tr.duration * 0.4))
            self.play(FadeIn(counter_block), run_time=min(0.6, tr.duration * 0.2))
            self.play(
                counter_val.animate.set_value(raw_MB_display),
                UpdateFromFunc(counter_val,
                    lambda m: m.set_color(
                        RED if m.get_value() > 30 else
                        YELLOW if m.get_value() > 15 else GREEN_C
                    )
                ),
                run_time=min(1.8, tr.duration * 0.4)
            )

        with self.voiceover(
            "Tức là một video 60fps dài một giây với độ phân giải này "
            "sẽ nặng gần 3GB. Thật khủng khiếp!"
        ) as tr:
            self.update_subtitle("Video 60fps × 1 giây ≈ 2.75 GB.\nThật khủng khiếp!")
            self.play(Write(video_warn), run_time=min(0.8, tr.duration * 0.3))
            self.play(Indicate(video_warn, scale_factor=1.1, color=RED), run_time=0.5)
            self.play(Indicate(video_warn, scale_factor=1.1, color=RED), run_time=0.5)

        # ── Giải pháp JPG & PNG ───────────────────────────────────────────────
        solution_title = Text("Giải pháp: JPG & PNG", font_size=34, color=YELLOW, weight=BOLD)
        solution_title.move_to(UP * 1.0)

        jpg_box  = RoundedRectangle(width=2.8, height=1.4, corner_radius=0.2,
                                    color=ORANGE, fill_color=ORANGE, fill_opacity=0.12)
        jpg_lbl  = Text("JPG\nNén tổn hao", font_size=22, color=ORANGE)
        jpg_lbl.move_to(jpg_box.get_center())
        jpg_grp  = VGroup(jpg_box, jpg_lbl)

        png_box  = RoundedRectangle(width=2.8, height=1.4, corner_radius=0.2,
                                    color=FAMI_CYAN, fill_color=FAMI_CYAN, fill_opacity=0.12)
        png_lbl  = Text("PNG\nKhông tổn hao", font_size=22, color=FAMI_CYAN)
        png_lbl.move_to(png_box.get_center())
        png_grp  = VGroup(png_box, png_lbl)

        vs_txt   = Text("VS", font_size=32, color=GRAY_A, weight=BOLD)
        formats_row = VGroup(jpg_grp, vs_txt, png_grp).arrange(RIGHT, buff=0.6)
        formats_row.next_to(solution_title, DOWN, buff=0.5)
        if formats_row.get_bottom()[1] < -3.4:
            formats_row.next_to(solution_title, DOWN, buff=0.3)

        combined_group = VGroup(solution_title, formats_row)
        if combined_group.get_bottom()[1] < -3.4:
            combined_group.scale_to_fit_height(
                3.4 + combined_group.get_top()[1] - combined_group.get_bottom()[1]
            )
            combined_group.move_to(UP * 0.2)

        with self.voiceover(
            "Đó là lý do các tiêu chuẩn nén ảnh như J P G và P N G ra đời. "
            "Chúng đại diện cho hai trường phái toán học hoàn toàn trái ngược nhau!"
        ) as tr:
            self.update_subtitle("JPG và PNG – hai trường phái toán học\nhoàn toàn trái ngược nhau!")
            self.play(
                FadeOut(size_formula, counter_block, video_warn),
                Write(solution_title),
                run_time=min(0.8, tr.duration * 0.2)
            )
            self.play(FadeIn(jpg_grp), Write(vs_txt), FadeIn(png_grp),
                      run_time=min(1.0, tr.duration * 0.4))
            self.play(Indicate(jpg_grp, color=ORANGE), Indicate(png_grp, color=FAMI_CYAN),
                      run_time=min(0.8, tr.duration * 0.2))

        self.play(*[FadeOut(m) for m in self.mobjects])


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PHẦN 3: JPG – TRỰC TIẾP TRÊN MONALISA: YCbCr SPLIT + DCT + QUANTIZATION
# Layout: Ảnh Monalisa bên trái/giữa, biểu diễn trực quan trên ảnh
# Tất cả Y: -3.5 đến +4.0
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class JPGScene(FaMIBaseScene):
    """
    Phần 3: Minh họa nén JPG trực tiếp trên ảnh Monalisa.
    - YCbCr: Tách 3 phiên bản ảnh (Y/Cb/Cr) xếp cạnh nhau
    - DCT: Zoom vào 1 khối 8×8 của ảnh, biến đổi sang miền tần số
    - Quantization: Flash các số 0 trên heatmap
    - MSE: So sánh trực quan ảnh gốc vs ảnh nén trên Monalisa
    """

    def construct(self):
        pil_img, (img_w, img_h) = load_image()
        arr_gray = np.array(pil_img.convert('L'), dtype=float)
        arr_rgb  = np.array(pil_img.convert('RGB'))

        # ── Tiêu đề ──────────────────────────────────────────────────────────
        title = self.create_title("PHẦN 3: JPG", "Bậc thầy đánh lừa thị giác")

        with self.voiceover("Đầu tiên là J P G – đại diện cho cơ chế nén tổn hao.") as tr:
            self.update_subtitle("JPG – đại diện cho cơ chế nén tổn hao (lossy compression).")
            self.play(Write(title), run_time=min(1.2, tr.duration * 0.8))

        # ━━ 3A: TÁCH KÊNH YCbCr TRỰC TIẾP TRÊN 3 PHIÊN BẢN ẢNH ━━━━━━━━━━━━

        # Tính 3 kênh YCbCr từ ảnh gốc
        R = arr_rgb[:, :, 0].astype(float)
        G = arr_rgb[:, :, 1].astype(float)
        B = arr_rgb[:, :, 2].astype(float)

        Y_ch  = np.clip(0.257*R + 0.504*G + 0.098*B + 16,  0, 255).astype(np.uint8)
        Cb_ch = np.clip(-0.148*R - 0.291*G + 0.439*B + 128, 0, 255).astype(np.uint8)
        Cr_ch = np.clip(0.439*R - 0.368*G - 0.071*B + 128,  0, 255).astype(np.uint8)

        from PIL import Image as PILImage

        # Tạo ảnh PIL cho từng kênh (hiển thị grayscale để nhìn rõ)
        pil_Y  = PILImage.fromarray(Y_ch,  mode='L')
        pil_Cb = PILImage.fromarray(Cb_ch, mode='L')
        pil_Cr = PILImage.fromarray(Cr_ch, mode='L')

        # Kích thước ảnh nhỏ hơn để vừa 3 cái ngang nhau
        IMG_SM_H = 3.4
        IMG_SM_W = IMG_SM_H * (img_w / img_h)

        # Kiểm tra tổng chiều rộng 3 ảnh + gap
        total_w_3 = IMG_SM_W * 3 + 0.4 * 2
        if total_w_3 > 8.2:
            scale_factor = 8.2 / total_w_3
            IMG_SM_H *= scale_factor
            IMG_SM_W *= scale_factor

        GAP = 0.3
        IMGS_Y_POS = UP * 0.4  # tâm Y của 3 ảnh

        mob_Y  = ImageMobject(pil_Y)
        mob_Cb = ImageMobject(pil_Cb)
        mob_Cr = ImageMobject(pil_Cr)
        for mob in [mob_Y, mob_Cb, mob_Cr]:
            mob.height = IMG_SM_H

        mob_Y.move_to(LEFT  * (IMG_SM_W + GAP) + IMGS_Y_POS)
        mob_Cb.move_to(ORIGIN + IMGS_Y_POS)
        mob_Cr.move_to(RIGHT * (IMG_SM_W + GAP) + IMGS_Y_POS)

        # Nhãn kênh
        lbl_Y  = Text("Y (Luma)",  font_size=20, color=GRAY_A).next_to(mob_Y,  UP, buff=0.15)
        lbl_Cb = Text("Cb (Sắc xanh)", font_size=18, color="#4488FF").next_to(mob_Cb, UP, buff=0.15)
        lbl_Cr = Text("Cr (Sắc đỏ)",  font_size=18, color="#FF4488").next_to(mob_Cr, UP, buff=0.15)

        # Khung cho từng kênh
        frame_Y  = SurroundingRectangle(mob_Y,  color=GRAY_A, buff=0.05, stroke_width=1.5)
        frame_Cb = SurroundingRectangle(mob_Cb, color="#4488FF", buff=0.05, stroke_width=1.5)
        frame_Cr = SurroundingRectangle(mob_Cr, color="#FF4488", buff=0.05, stroke_width=1.5)

        # Phương trình YCbCr bên dưới ảnh
        eq_Y = MathTex(
            r"Y = 0.257R + 0.504G + 0.098B + 16",
            font_size=20, color=GRAY_A, tex_template=math_tex_template
        )
        eq_Cb = MathTex(
            r"Cb = -0.148R - 0.291G + 0.439B + 128",
            font_size=20, color="#4488FF", tex_template=math_tex_template
        )
        eq_Cr = MathTex(
            r"Cr = 0.439R - 0.368G - 0.071B + 128",
            font_size=20, color="#FF4488", tex_template=math_tex_template
        )
        eq_group = VGroup(eq_Y, eq_Cb, eq_Cr).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        # Đặt dưới các ảnh, kiểm tra không vượt -3.4
        eq_group.next_to(Group(mob_Y, mob_Cb, mob_Cr), DOWN, buff=0.25)
        if eq_group.get_bottom()[1] < -3.4:
            eq_group.move_to(DOWN * 2.8)
        if eq_group.width > 8.5:
            eq_group.scale_to_fit_width(8.5)

        # ── Ảnh gốc xuất hiện, tách thành 3 kênh ───────────────────────────
        pil_color_small = pil_img.resize(
            (max(1, int(img_w * IMG_SM_H / img_h)), max(1, int(IMG_SM_H * 100))),
            PILImage.Resampling.LANCZOS
        )
        mob_orig_center = ImageMobject(pil_img)
        mob_orig_center.height = IMG_SM_H
        mob_orig_center.move_to(IMGS_Y_POS)

        with self.voiceover(
            "Thuật toán này dựa trên một lỗ hổng sinh lý của mắt người: "
            "Võng mạc cực kỳ nhạy cảm với độ sáng, nhưng lại kém nhận diện chi tiết màu sắc nhỏ."
        ) as tr:
            self.update_subtitle("Mắt người nhạy với độ sáng,\nnhưng kém nhận diện chi tiết màu sắc nhỏ.")
            self.play(FadeIn(mob_orig_center), run_time=min(1.0, tr.duration * 0.3))

        with self.voiceover(
            "J P G bóc tách không gian RGB sang không gian màu YCbCr "
            "bằng hệ phương trình ma trận tuyến tính."
        ) as tr:
            self.update_subtitle("JPG chuyển RGB → YCbCr bằng hệ phương trình tuyến tính.")
            # Bùng nổ ảnh gốc thành 3 kênh
            self.play(
                ReplacementTransform(mob_orig_center.copy(), mob_Y),
                ReplacementTransform(mob_orig_center.copy(), mob_Cb),
                ReplacementTransform(mob_orig_center, mob_Cr),
                run_time=min(1.5, tr.duration * 0.45)
            )
            self.play(
                Create(frame_Y), Write(lbl_Y),
                Create(frame_Cb), Write(lbl_Cb),
                Create(frame_Cr), Write(lbl_Cr),
                run_time=min(0.8, tr.duration * 0.25)
            )
            self.play(Write(eq_group), run_time=min(1.0, tr.duration * 0.3))

        # Loại bỏ 50% dữ liệu Cb, Cr (Chroma subsampling)
        strike_Cb = Line(mob_Cb.get_corner(UL), mob_Cb.get_corner(DR),
                         color=RED, stroke_width=4)
        strike_Cr = Line(mob_Cr.get_corner(UL), mob_Cr.get_corner(DR),
                         color=RED, stroke_width=4)
        discard_lbl = Text("Loại bỏ 50% sắc độ!", font_size=22, color=RED, weight=BOLD)
        # Đặt giữa Cb và Cr
        discard_lbl.move_to((mob_Cb.get_center() + mob_Cr.get_center()) / 2 + DOWN * 0.5)
        if discard_lbl.get_bottom()[1] < -3.4:
            discard_lbl.move_to((mob_Cb.get_center() + mob_Cr.get_center()) / 2)

        with self.voiceover(
            "Lớp cường độ sáng Y được giữ lại gần như nguyên vẹn, "
            "còn dữ liệu ở hai lớp sắc độ Cb và Cr bị hệ thống thẳng tay loại bỏ đi một nửa."
        ) as tr:
            self.update_subtitle("Lớp Y giữ nguyên.\nCb và Cr bị loại bỏ 50% dữ liệu sắc độ!")
            self.play(
                mob_Y.animate.set_opacity(1.0),
                mob_Cb.animate.set_opacity(0.35),
                mob_Cr.animate.set_opacity(0.35),
                run_time=min(1.0, tr.duration * 0.4)
            )
            self.play(
                Create(strike_Cb), Create(strike_Cr),
                run_time=min(0.8, tr.duration * 0.3)
            )
            self.play(Write(discard_lbl), run_time=min(0.6, tr.duration * 0.2))

        self.play(*[FadeOut(m) for m in self.mobjects if m is not title])

        # ━━ 3B: DCT – ZOOM VÀO KHỐI 8×8 THỰC TẾ CỦA MONALISA ━━━━━━━━━━━━━━

        # Lấy khối 8×8 từ vùng mặt (trung tâm ảnh)
        cy, cx = arr_gray.shape[0]//2, arr_gray.shape[1]//2
        block_orig = arr_gray[cy-4:cy+4, cx-4:cx+4].copy()
        from scipy.fft import dctn
        block_dct = dctn(block_orig - 128, norm='ortho')

        # ── Thumbnail ảnh bên trái với hộp zoom vào khối 8×8 ────────────────
        THUMB_H  = 3.6
        THUMB_W  = THUMB_H * (img_w / img_h)
        THUMB_POS = LEFT * 3.0 + UP * 0.3

        thumb_mob = ImageMobject(pil_img)
        thumb_mob.height = THUMB_H
        thumb_mob.move_to(THUMB_POS)
        thumb_label = Text("Monalisa", font_size=18, color=GRAY_A).next_to(thumb_mob, DOWN, buff=0.1)

        # Ô vuông highlight khối 8×8 trên ảnh thực
        block_frac_y = 0.5 - 4/arr_gray.shape[0]
        block_frac_x = 0.5 - 4/arr_gray.shape[1]
        block_size_y = 8 / arr_gray.shape[0] * THUMB_H
        block_size_x = 8 / arr_gray.shape[1] * THUMB_W
        zoom_box = Rectangle(
            width=block_size_x, height=block_size_y,
            color=YELLOW, stroke_width=2
        )
        zoom_box.move_to(THUMB_POS)  # trung tâm ảnh = trung tâm khối

        zoom_arrow = Arrow(
            zoom_box.get_right(), zoom_box.get_right() + RIGHT * 0.8,
            buff=0.05, color=YELLOW, stroke_width=2
        )

        # ── Hàm tạo lưới 8×8 ─────────────────────────────────────────────────
        CELL = 0.56

        def make_8x8_grid(values_2d, colormap_fn=None, font_sz=11,
                          label_color_fn=None, num_fmt="d"):
            cells = VGroup()
            nums  = VGroup()
            vmin, vmax = values_2d.min(), values_2d.max()
            span = max(vmax - vmin, 1e-9)
            for i in range(8):
                for j in range(8):
                    v = float(values_2d[i, j])
                    frac = (v - vmin) / span
                    if colormap_fn:
                        fc = colormap_fn(frac)
                    else:
                        fc = rgb_to_color([frac, frac, frac])
                    rect = Rectangle(width=CELL, height=CELL)
                    rect.set_fill(fc, opacity=1)
                    rect.set_stroke(color="#333333", width=0.4)
                    rect.move_to(RIGHT * (j - 3.5) * CELL + UP * (3.5 - i) * CELL)
                    cells.add(rect)
                    s = str(int(round(v))) if num_fmt == "d" else f"{v:.0f}"
                    lc = WHITE
                    if label_color_fn:
                        lc = label_color_fn(v)
                    t = Text(s, font_size=font_sz, color=lc)
                    t.move_to(rect.get_center())
                    nums.add(t)
            return cells, nums

        spatial_cells, spatial_nums = make_8x8_grid(
            block_orig,
            colormap_fn=lambda f: rgb_to_color([f, f, f]),
            label_color_fn=lambda v: BLACK if v > 128 else WHITE,
            font_sz=11
        )
        spatial_group = VGroup(spatial_cells, spatial_nums)
        GRID_POS = RIGHT * 0.6 + UP * 0.3
        spatial_group.move_to(GRID_POS)
        spatial_title = Text("Miền không gian f(x,y)", font_size=19, color=WHITE)
        spatial_title.next_to(spatial_cells, UP, buff=0.18)

        # Công thức DCT
        dct_formula = MathTex(
            r"F(u,v)=\alpha(u)\alpha(v)\!\sum_{x}\!\sum_{y}"
            r"f(x,y)\cos\!\left[\tfrac{(2x+1)u\pi}{16}\right]\!"
            r"\cos\!\left[\tfrac{(2y+1)v\pi}{16}\right]",
            font_size=18, tex_template=math_tex_template
        )
        dct_formula.next_to(spatial_group, DOWN, buff=0.3)
        if dct_formula.width > 5.5:
            dct_formula.scale_to_fit_width(5.5)
        if dct_formula.get_bottom()[1] < -3.3:
            dct_formula.next_to(spatial_group, DOWN, buff=0.15)

        dct_arrow = Arrow(
            spatial_cells.get_right() + RIGHT * 0.1,
            spatial_cells.get_right() + RIGHT * 1.0,
            buff=0.05, color=YELLOW, stroke_width=3
        )
        dct_arrow_label = Text("DCT", font_size=20, color=YELLOW, weight=BOLD)
        dct_arrow_label.next_to(dct_arrow, UP, buff=0.08)

        # Lưới tần số (heatmap)
        freq_cells, freq_nums = make_8x8_grid(
            block_dct,
            colormap_fn=heat_color,
            label_color_fn=lambda v: BLACK if abs(v) < 50 else WHITE,
            font_sz=9
        )
        freq_group = VGroup(freq_cells, freq_nums)
        freq_group.move_to(GRID_POS + RIGHT * 3.2)
        freq_title = Text("Miền tần số F(u,v)", font_size=19, color=YELLOW)
        freq_title.next_to(freq_cells, UP, buff=0.18)

        # Đảm bảo không vượt vùng phải
        right_edge = freq_group.get_right()[0]
        if right_edge > 4.3:
            shift_amount = right_edge - 4.3
            spatial_group.shift(LEFT * shift_amount)
            spatial_title.shift(LEFT * shift_amount)
            dct_arrow.shift(LEFT * shift_amount)
            dct_arrow_label.shift(LEFT * shift_amount)
            freq_group.shift(LEFT * shift_amount)
            freq_title.shift(LEFT * shift_amount)

        with self.voiceover(
            "Bức ảnh sẽ được băm thành các khối ma trận nhỏ 8 nhân 8. "
            "Đây là một khối điển hình trong miền không gian."
        ) as tr:
            self.update_subtitle("Ảnh được băm thành các khối 8×8.\nĐây là một khối trong miền không gian.")
            self.play(FadeIn(thumb_mob), Write(thumb_label), run_time=min(0.8, tr.duration * 0.3))
            self.play(Create(zoom_box), GrowArrow(zoom_arrow), run_time=min(0.6, tr.duration * 0.25))
            self.play(FadeIn(spatial_cells), Write(spatial_title), run_time=min(0.8, tr.duration * 0.25))
            self.play(FadeIn(spatial_nums), run_time=min(0.5, tr.duration * 0.2))

        with self.voiceover(
            "Phương trình 2D-DCT sẽ chuyển đổi tín hiệu từ miền không gian "
            "sang miền phổ tần số F(u,v). Đây là cốt lõi sức mạnh của J P G."
        ) as tr:
            self.update_subtitle("2D-DCT chuyển tín hiệu từ miền không gian\nsang miền phổ tần số F(u,v).")
            self.play(Write(dct_formula), run_time=min(1.0, tr.duration * 0.3))
            self.play(GrowArrow(dct_arrow), Write(dct_arrow_label), run_time=min(0.6, tr.duration * 0.2))
            self.play(
                ReplacementTransform(spatial_cells.copy(), freq_cells),
                ReplacementTransform(spatial_nums.copy(), freq_nums),
                Write(freq_title),
                run_time=min(1.5, tr.duration * 0.4)
            )

        # Highlight tần số thấp/cao
        lo_highlight = SurroundingRectangle(
            VGroup(*[freq_cells[i*8+j] for i in range(3) for j in range(3)]),
            color=WHITE, buff=0.04, stroke_width=2
        )
        hi_highlight = SurroundingRectangle(
            VGroup(*[freq_cells[i*8+j] for i in range(5, 8) for j in range(5, 8)]),
            color=RED, buff=0.04, stroke_width=2
        )
        lo_lbl = Text("Năng lượng\nchính", font_size=14, color=WHITE)
        hi_lbl = Text("Nhiễu\nchi tiết", font_size=14, color=RED)
        lo_lbl.next_to(lo_highlight, LEFT, buff=0.1)
        hi_lbl.next_to(hi_highlight, RIGHT, buff=0.1)
        # Clamp nhãn vào vùng an toàn
        if lo_lbl.get_left()[0] < -4.4:
            lo_lbl.next_to(lo_highlight, DOWN, buff=0.08)
        if hi_lbl.get_right()[0] > 4.3:
            hi_lbl.next_to(hi_highlight, DOWN, buff=0.08)

        with self.voiceover(
            "Hiện tượng tuyệt mỹ gọi là Hội tụ năng lượng: "
            "Thông tin quan trọng nhất dồn về góc trên trái, "
            "còn các nhiễu hạt chi tiết nhỏ bị đẩy sang góc phải."
        ) as tr:
            self.update_subtitle("Hội tụ năng lượng: thông tin quan trọng ở góc trên trái,\nnhiễu hạt ở góc phải dưới.")
            self.play(Create(lo_highlight), Write(lo_lbl), run_time=min(0.7, tr.duration * 0.3))
            self.play(Create(hi_highlight), Write(hi_lbl), run_time=min(0.7, tr.duration * 0.3))
            self.play(
                Indicate(lo_highlight, scale_factor=1.05),
                Indicate(hi_highlight, scale_factor=1.05, color=RED),
                run_time=0.6
            )

        # ━━ 3C: LƯỢNG TỬ HÓA – MATRIX Q VÀ KẾT QUẢ ━━━━━━━━━━━━━━━━━━━━━━━━

        self.play(*[FadeOut(m) for m in self.mobjects if m is not title])

        Q_standard = np.array([
            [16, 11, 10, 16, 24,  40,  51,  61],
            [12, 12, 14, 19, 26,  58,  60,  55],
            [14, 13, 16, 24, 40,  57,  69,  56],
            [14, 17, 22, 29, 51,  87,  80,  62],
            [18, 22, 37, 56, 68, 109, 103,  77],
            [24, 35, 55, 64, 81, 104, 113,  92],
            [49, 64, 78, 87,103, 121, 120, 101],
            [72, 92, 95, 98,112, 100, 103,  99],
        ], dtype=float)

        block_quantized = np.round(block_dct / Q_standard).astype(int)
        from scipy.fft import idctn
        block_reconstructed = np.clip(
            idctn(block_quantized * Q_standard, norm='ortho') + 128, 0, 255
        )

        # Layout: 3 ma trận cạnh nhau: F(u,v) | ÷Q | kết quả
        CELL_SM = 0.48   # nhỏ hơn để vừa 3 lưới + ký hiệu

        def make_8x8_small(values_2d, colormap_fn=None, font_sz=9, label_color_fn=None):
            cells = VGroup()
            nums  = VGroup()
            vmin, vmax = values_2d.min(), values_2d.max()
            span = max(vmax - vmin, 1e-9)
            for i in range(8):
                for j in range(8):
                    v = float(values_2d[i, j])
                    frac = (v - vmin) / span
                    fc = colormap_fn(frac) if colormap_fn else rgb_to_color([frac]*3)
                    rect = Rectangle(width=CELL_SM, height=CELL_SM)
                    rect.set_fill(fc, opacity=1)
                    rect.set_stroke(color="#333333", width=0.3)
                    rect.move_to(RIGHT*(j-3.5)*CELL_SM + UP*(3.5-i)*CELL_SM)
                    cells.add(rect)
                    s = str(int(round(v)))
                    lc = WHITE if not label_color_fn else label_color_fn(v)
                    t = Text(s, font_size=font_sz, color=lc)
                    t.move_to(rect.get_center())
                    nums.add(t)
            return cells, nums

        # Lưới 1: Tần số F(u,v)
        fc1, fn1 = make_8x8_small(
            block_dct, colormap_fn=heat_color,
            label_color_fn=lambda v: BLACK if abs(v) < 50 else WHITE
        )
        g1 = VGroup(fc1, fn1)
        t1 = Text("F(u,v)", font_size=18, color=YELLOW)

        # Lưới 2: Ma trận Q
        fc2, fn2 = make_8x8_small(
            Q_standard,
            colormap_fn=lambda f: interpolate_color(DARK_BLUE, RED, f),
            label_color_fn=lambda v: WHITE
        )
        g2 = VGroup(fc2, fn2)
        t2 = Text("Ma trận Q", font_size=18, color=RED)

        # Lưới 3: Sau lượng tử hóa
        fc3, fn3 = make_8x8_small(
            block_quantized.astype(float),
            colormap_fn=lambda f: interpolate_color(DARK_BLUE, YELLOW, abs(2*f-1)),
            label_color_fn=lambda v: RED if v == 0 else WHITE
        )
        g3 = VGroup(fc3, fn3)
        t3 = Text("Kết quả", font_size=18, color=SUCCESS)

        # Ký hiệu toán học
        div_sign   = MathTex(r"\div", font_size=36, color=YELLOW,
                              tex_template=math_tex_template)
        round_sign = MathTex(r"\xrightarrow{\text{round}}", font_size=26, color=YELLOW,
                              tex_template=math_tex_template)

        # Sắp xếp hàng ngang: g1 ÷ g2 → g3
        grid_width = CELL_SM * 8
        spacing = 0.7
        g1.move_to(LEFT * (grid_width + spacing * 1.5))
        div_sign.move_to(LEFT * (grid_width / 2 + spacing / 2))
        g2.move_to(ORIGIN)
        round_sign.move_to(RIGHT * (grid_width / 2 + spacing / 2))
        g3.move_to(RIGHT * (grid_width + spacing * 1.5))

        # Kiểm tra vượt biên ngang
        row_group = VGroup(g1, div_sign, g2, round_sign, g3)
        if row_group.width > 8.8:
            row_group.scale_to_fit_width(8.8)

        # Đặt vào vùng vàng
        row_group.move_to(UP * 0.4)

        # Cập nhật vị trí tiêu đề ma trận
        t1.next_to(fc1, UP, buff=0.15)
        t2.next_to(fc2, UP, buff=0.15)
        t3.next_to(fc3, UP, buff=0.15)

        # Công thức lượng tử hóa
        quant_formula = MathTex(
            r"\hat{F}(u,v) = \text{round}\!\left(\frac{F(u,v)}{Q(u,v)}\right)",
            font_size=24, tex_template=math_tex_template
        )
        quant_formula.next_to(row_group, DOWN, buff=0.35)
        if quant_formula.get_bottom()[1] < -3.3:
            quant_formula.next_to(row_group, DOWN, buff=0.15)
        if quant_formula.width > 8.0:
            quant_formula.scale_to_fit_width(8.0)

        with self.voiceover(
            "Tiếp đó, J P G kích hoạt cỗ máy hủy diệt mang tên Lượng tử hóa: "
            "Lấy các hệ số tần số chia cho ma trận Q rồi làm tròn."
        ) as tr:
            self.update_subtitle("Lượng tử hóa: Chia F(u,v) cho ma trận Q rồi làm tròn.")
            self.play(Write(quant_formula), run_time=min(1.0, tr.duration * 0.3))
            self.play(FadeIn(fc1), FadeIn(fn1), Write(t1), run_time=min(0.8, tr.duration * 0.25))
            self.play(Write(div_sign), FadeIn(fc2), FadeIn(fn2), Write(t2),
                      run_time=min(0.8, tr.duration * 0.25))

        with self.voiceover(
            "Kết quả: hàng loạt dữ liệu tần số cao bị nghiền nát thành các số 0 tròn trĩnh. "
            "Chính chuỗi số 0 này giúp dung lượng file co ngót lại hàng chục lần."
        ) as tr:
            self.update_subtitle("Hàng loạt dữ liệu bị nghiền thành số 0.\nChuỗi số 0 dài giúp nén file hàng chục lần.")
            self.play(Write(round_sign), FadeIn(fc3), FadeIn(fn3), Write(t3),
                      run_time=min(1.0, tr.duration * 0.35))
            # Flash các ô bằng 0
            zero_rects = VGroup(*[
                fc3[i*8+j] for i in range(8) for j in range(8)
                if block_quantized[i, j] == 0
            ])
            if len(zero_rects) > 0:
                self.play(Flash(zero_rects, color=RED, line_length=0.08, flash_radius=0.12),
                          run_time=min(0.8, tr.duration * 0.25))

        # ━━ 3D: MSE – SO SÁNH ẢNH GỐC vs ẢNH NÉN TRỰC TIẾP TRÊN MONALISA ━━━

        self.play(*[FadeOut(m) for m in self.mobjects if m is not title])

        diff_block = block_orig - block_reconstructed
        mse_val    = float(np.mean(diff_block**2))

        # Tạo ảnh nén JPG mức chất lượng thấp để so sánh trực quan
        import io
        buf_low  = io.BytesIO()
        buf_high = io.BytesIO()
        pil_img.save(buf_low,  format='JPEG', quality=10)
        pil_img.save(buf_high, format='JPEG', quality=95)
        buf_low.seek(0);  buf_high.seek(0)
        pil_jpg_low  = PILImage.open(buf_low).copy()
        pil_jpg_high = PILImage.open(buf_high).copy()

        # Kích thước 2 ảnh cạnh nhau
        COMPARE_H = 3.8
        COMPARE_W = COMPARE_H * (img_w / img_h)
        total_compare = COMPARE_W * 2 + 0.5
        if total_compare > 8.5:
            scale_c = 8.5 / total_compare
            COMPARE_H *= scale_c
            COMPARE_W *= scale_c

        mob_orig_cmp = ImageMobject(pil_img)
        mob_jpg_low  = ImageMobject(pil_jpg_low)
        mob_orig_cmp.height = COMPARE_H
        mob_jpg_low.height  = COMPARE_H

        mob_orig_cmp.move_to(LEFT  * (COMPARE_W / 2 + 0.25) + UP * 0.3)
        mob_jpg_low.move_to(RIGHT  * (COMPARE_W / 2 + 0.25) + UP * 0.3)

        # Nhãn
        lbl_orig = Text("Ảnh gốc (47 MB)", font_size=18, color=WHITE)
        lbl_orig.next_to(mob_orig_cmp, DOWN, buff=0.12)
        lbl_jpg  = Text("JPG Q=10 (< 1 MB)", font_size=18, color=ORANGE)
        lbl_jpg.next_to(mob_jpg_low, DOWN, buff=0.12)

        # Khung
        frame_orig = SurroundingRectangle(mob_orig_cmp, color=WHITE, buff=0.05, stroke_width=1.5)
        frame_jpg  = SurroundingRectangle(mob_jpg_low,  color=ORANGE, buff=0.05, stroke_width=2)

        # MSE hiển thị bên dưới
        mse_eq = MathTex(
            r"MSE = \frac{1}{mn}\sum_{i,j}[I(i,j)-K(i,j)]^2 = " + f"{mse_val:.2f}",
            font_size=22, color=RED, tex_template=math_tex_template
        )
        mse_eq.next_to(Group(mob_orig_cmp, mob_jpg_low), DOWN, buff=0.35)
        if mse_eq.get_bottom()[1] < -3.3:
            mse_eq.next_to(Group(mob_orig_cmp, mob_jpg_low), DOWN, buff=0.15)
        if mse_eq.width > 8.5:
            mse_eq.scale_to_fit_width(8.5)

        with self.voiceover(
            "Để đo lường sự biến dạng này, khoa học sử dụng công thức "
            "Hệ số Sai số Trung bình Bình phương MSE giữa ảnh gốc và ảnh đã giải nén."
        ) as tr:
            self.update_subtitle("MSE đo lường sự biến dạng giữa ảnh gốc I\nvà ảnh giải nén K.")
            self.play(FadeIn(mob_orig_cmp), Create(frame_orig), Write(lbl_orig),
                      run_time=min(1.0, tr.duration * 0.3))
            self.play(FadeIn(mob_jpg_low), Create(frame_jpg), Write(lbl_jpg),
                      run_time=min(1.0, tr.duration * 0.3))
            self.play(Write(mse_eq), run_time=min(1.0, tr.duration * 0.3))

        with self.voiceover(
            "Đổi lại, dữ liệu bị mất vĩnh viễn – đó chính là bản chất của nén tổn hao."
        ) as tr:
            self.update_subtitle("Dữ liệu bị mất vĩnh viễn –\nbản chất của nén tổn hao (lossy).")
            self.play(Indicate(mse_eq, color=RED, scale_factor=1.1), run_time=0.6)
            self.play(Indicate(frame_jpg, color=RED), run_time=0.5)

        self.play(*[FadeOut(m) for m in self.mobjects])


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PHẦN 4: PNG – TRỰC TIẾP TRÊN MONALISA: DELTA FILTER + DEFLATE
# Layout: Ảnh Monalisa hiển thị dải pixel thực, delta values, LZ77, Huffman
# Tất cả Y: -3.5 đến +4.0
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class PNGScene(FaMIBaseScene):
    """
    Phần 4: Minh họa nén PNG trực tiếp trên ảnh Monalisa.
    - Predictive Filter: Zoom vào dải pixel thực của Monalisa, tính Delta
    - LZ77: Tìm chuỗi lặp trong delta values
    - Huffman: Cây mã hóa xác suất
    - Kết quả: So sánh ảnh gốc vs PNG lossless
    """

    def construct(self):
        pil_img, (img_w, img_h) = load_image()
        arr_gray = np.array(pil_img.convert('L'))

        from PIL import Image as PILImage

        # ── Tiêu đề ──────────────────────────────────────────────────────────
        title = self.create_title("PHẦN 4: PNG", "Sự hoàn mỹ của nén không tổn hao")

        with self.voiceover(
            "Nếu sự hao hụt của J P G là bản án tử đối với các bản vẽ kỹ thuật hay ảnh y khoa, "
            "thì P N G xuất hiện như một đấng cứu thế. P N G sử dụng cơ chế nén không tổn hao."
        ) as tr:
            self.update_subtitle("PNG – cơ chế nén không tổn hao (lossless).\nBảo toàn 100% dữ liệu.")
            self.play(Write(title), run_time=min(1.2, tr.duration * 0.8))

        # ━━ 4A: PREDICTIVE FILTER – DẢI PIXEL THỰC TỪ MONALISA ━━━━━━━━━━━━━

        # Lấy dải 12 pixels từ vùng bầu trời (đơn điệu) của ảnh
        sky_y = int(arr_gray.shape[0] * 0.12)
        sky_x = int(arr_gray.shape[1] * 0.3)
        NUM_PIX = 12
        # Lấy dải ngang từ vùng đơn điệu
        raw_slice = arr_gray[sky_y, sky_x:sky_x+NUM_PIX].astype(int)
        if len(raw_slice) < NUM_PIX:
            raw_slice = np.array([118, 120, 121, 119, 122, 120, 123, 121, 118, 122, 120, 119])
        pixel_vals = list(raw_slice[:NUM_PIX])

        # Thumbnail ảnh bên trái với highlight vùng lấy pixel
        THUMB_H = 3.8
        THUMB_W = THUMB_H * (img_w / img_h)
        THUMB_POS = LEFT * 2.8 + UP * 0.2

        thumb_mob = ImageMobject(pil_img)
        thumb_mob.height = THUMB_H
        thumb_mob.move_to(THUMB_POS)

        # Vùng highlight trên ảnh
        frac_y    = sky_y / arr_gray.shape[0]
        frac_x0   = sky_x / arr_gray.shape[1]
        frac_x1   = (sky_x + NUM_PIX) / arr_gray.shape[1]
        hi_h      = 8 / arr_gray.shape[0] * THUMB_H   # ~8 hàng
        hi_w      = (frac_x1 - frac_x0) * THUMB_W
        hi_y      = THUMB_POS[1] + THUMB_H/2 - frac_y * THUMB_H - hi_h/2
        hi_x      = THUMB_POS[0] - THUMB_W/2 + (frac_x0 + frac_x1)/2 * THUMB_W
        hl_rect   = Rectangle(width=hi_w, height=hi_h, color=YELLOW, stroke_width=2)
        hl_rect.set_fill(YELLOW, opacity=0.2)
        hl_rect.move_to([hi_x, hi_y, 0])

        # Dải pixel bên phải ảnh
        PXBOX_W   = 0.62
        PXBOX_H   = 0.62
        PX_START_X = RIGHT * 1.0 + UP * 1.6

        pixel_boxes  = VGroup()
        pixel_labels = VGroup()
        for j, v in enumerate(pixel_vals):
            brt = v / 255.0
            box = Rectangle(width=PXBOX_W, height=PXBOX_H)
            box.set_fill(rgb_to_color([brt, brt, brt]), opacity=1)
            box.set_stroke(WHITE, width=0.8)
            box.move_to(PX_START_X + RIGHT * j * (PXBOX_W + 0.04))
            pixel_boxes.add(box)
            t = Text(str(v), font_size=13,
                     color=BLACK if v > 130 else WHITE)
            t.move_to(box.get_center())
            pixel_labels.add(t)

        # Kiểm tra không vượt cạnh phải
        if pixel_boxes.get_right()[0] > 4.3:
            shift_left = pixel_boxes.get_right()[0] - 4.3
            pixel_boxes.shift(LEFT * shift_left)
            pixel_labels.shift(LEFT * shift_left)

        px_label = Text("Dải pixel thực từ Monalisa:", font_size=19, color=WHITE)
        px_label.next_to(pixel_boxes, UP, buff=0.2)

        # Mũi tên từ ảnh tới dải pixel
        arrow_to_pixels = Arrow(
            hl_rect.get_right(), pixel_boxes.get_left() + LEFT * 0.1,
            buff=0.1, color=YELLOW, stroke_width=2
        )

        with self.voiceover(
            "Thay vì dùng phương trình tần số và cắt xén dữ liệu, P N G "
            "phân tích cấu trúc bức ảnh bằng các Màng lọc nội suy dự báo."
        ) as tr:
            self.update_subtitle("PNG dùng Màng lọc nội suy dự báo\nthay vì cắt xén dữ liệu.")
            self.play(FadeIn(thumb_mob), run_time=min(0.8, tr.duration * 0.3))
            self.play(Create(hl_rect), GrowArrow(arrow_to_pixels),
                      run_time=min(0.8, tr.duration * 0.3))
            self.play(FadeIn(pixel_boxes), Write(px_label),
                      run_time=min(0.7, tr.duration * 0.25))
            self.play(FadeIn(pixel_labels), run_time=min(0.4, tr.duration * 0.15))

        # Tính Delta (SUB filter)
        deltas = [pixel_vals[0]] + [pixel_vals[j] - pixel_vals[j-1]
                                     for j in range(1, len(pixel_vals))]

        # Công thức Delta
        delta_formula = MathTex(
            r"\Delta(x,y) = f(x,y) - f_{\text{predict}}(x,y)",
            font_size=24, color=FAMI_CYAN, tex_template=math_tex_template
        )
        delta_formula.next_to(pixel_boxes, DOWN, buff=0.35)
        if delta_formula.width > 7.0:
            delta_formula.scale_to_fit_width(7.0)

        # Dải Delta bên dưới
        DBOX_W = PXBOX_W
        DBOX_H = PXBOX_H * 0.85
        delta_boxes_mob  = VGroup()
        delta_labels_mob = VGroup()
        delta_y_pos = delta_formula.get_bottom() + DOWN * 0.35

        for j, d in enumerate(deltas):
            fc = GREEN if d == 0 else (BLUE_C if d > 0 else RED_C)
            box = Rectangle(width=DBOX_W, height=DBOX_H)
            box.set_fill(fc, opacity=0.5 + 0.4 * min(abs(d)/10.0, 1.0))
            box.set_stroke(WHITE, width=0.6)
            # Dùng vị trí tương ứng với pixel phía trên
            box.move_to(pixel_boxes[j].get_center() + DOWN * (PXBOX_H + 0.35 + 0.4 + DBOX_H/2))
            delta_boxes_mob.add(box)
            sign = "+" if d > 0 else ""
            t = Text(f"{sign}{d}", font_size=12,
                     color=SUCCESS if d == 0 else WHITE)
            t.move_to(box.get_center())
            delta_labels_mob.add(t)

        delta_row_label = Text("Giá trị Δ (rất nhỏ!)", font_size=18, color=SUCCESS)
        delta_row_label.next_to(delta_boxes_mob, DOWN, buff=0.18)
        if delta_row_label.get_bottom()[1] < -3.4:
            delta_row_label.move_to(delta_boxes_mob.get_center() + DOWN * 0.2)

        with self.voiceover(
            "Nguyên lý của nó rất thanh lịch: Trong một mảng màu thực tế, "
            "các pixel nằm kề nhau thường có cường độ gần như bằng nhau."
        ) as tr:
            self.update_subtitle("Các pixel kề nhau trong vùng đơn điệu\nthường có cường độ gần bằng nhau.")
            self.play(Write(delta_formula), run_time=min(1.0, tr.duration * 0.5))

        with self.voiceover(
            "Thuật toán của P N G sẽ chạy phương trình phỏng đoán giá trị của pixel tiếp theo. "
            "Sau đó, hệ thống chỉ lưu trữ hiệu số vi phân Delta giữa giá trị thực tế "
            "và giá trị phỏng đoán."
        ) as tr:
            self.update_subtitle("PNG chỉ lưu trữ Δ = f(x,y) − f_predict(x,y),\nthay vì toàn bộ giá trị pixel.")
            # Lần lượt hiện từng delta box
            highlight_scan = SurroundingRectangle(pixel_boxes[0], color=YELLOW, buff=0.04)
            self.play(Create(highlight_scan), run_time=0.3)
            for j in range(len(pixel_vals)):
                self.play(
                    highlight_scan.animate.move_to(pixel_boxes[j].get_center()),
                    FadeIn(delta_boxes_mob[j]),
                    Write(delta_labels_mob[j]),
                    run_time=0.22
                )
            self.play(FadeOut(highlight_scan))
            self.play(Write(delta_row_label), run_time=min(0.5, tr.duration * 0.15))

        # ━━ 4B: DEFLATE – LZ77 + HUFFMAN ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        self.play(*[FadeOut(m) for m in self.mobjects if m is not title])

        deflate_title = Text("Bước 2: DEFLATE = LZ77 + Huffman",
                             font_size=26, color=FAMI_CYAN, weight=BOLD)
        deflate_title.move_to(UP * 3.2)
        if deflate_title.width > 8.5:
            deflate_title.scale_to_fit_width(8.5)

        # ── LZ77: Chuỗi lặp trong Delta ──────────────────────────────────────
        lz77_title = Text("LZ77: Tìm chuỗi lặp → thay bằng (offset, length)",
                          font_size=20, color=YELLOW)
        lz77_title.next_to(deflate_title, DOWN, buff=0.35)
        if lz77_title.width > 8.5:
            lz77_title.scale_to_fit_width(8.5)

        # Tái tạo dải delta để hiển thị LZ77
        demo_deltas = [118, 2, 1, -2, 3, -2, 3, -2, -3, 4, -2, -1]
        BXSZ = 0.58
        byte_boxes  = VGroup()
        byte_labels = VGroup()
        for j, d in enumerate(demo_deltas):
            fc = GREEN_C if abs(d) <= 2 else YELLOW_C
            box = Rectangle(width=BXSZ, height=BXSZ)
            box.set_fill(fc, opacity=0.35)
            box.set_stroke(WHITE, width=0.8)
            box.move_to(RIGHT * (j - 5.5) * (BXSZ + 0.04) + UP * 1.4)
            byte_boxes.add(box)
            sign = "+" if d > 0 else ""
            t = Text(f"{sign}{d}", font_size=13, color=WHITE)
            t.move_to(box.get_center())
            byte_labels.add(t)

        if byte_boxes.get_right()[0] > 4.3:
            shift_l = byte_boxes.get_right()[0] - 4.3
            byte_boxes.shift(LEFT * shift_l)
            byte_labels.shift(LEFT * shift_l)

        # Highlight chuỗi lặp: indices 4,5 → 6,7 → 9,10 đều là (+3,-2) hoặc (-2,+3)
        window_rect = SurroundingRectangle(
            VGroup(byte_boxes[4], byte_boxes[5]),
            color=ORANGE, buff=0.05, stroke_width=2
        )
        window_lbl = Text("Chuỗi gốc", font_size=14, color=ORANGE)
        window_lbl.next_to(window_rect, UP, buff=0.1)

        search_rect = SurroundingRectangle(
            VGroup(byte_boxes[6], byte_boxes[7]),
            color=RED, buff=0.05, stroke_width=2
        )
        search_lbl = Text("Lặp lại!", font_size=14, color=RED)
        search_lbl.next_to(search_rect, DOWN, buff=0.1)

        ref_arrow = CurvedArrow(
            byte_boxes[6].get_top() + UP*0.05,
            byte_boxes[4].get_top() + UP*0.05,
            color=ORANGE, angle=-PI/3, stroke_width=2
        )
        ref_text = Text("(offset=2, len=2)", font_size=16, color=ORANGE)
        ref_text.next_to(ref_arrow, UP, buff=0.1)
        if ref_text.get_top()[1] > 3.8:
            ref_text.next_to(ref_arrow, DOWN, buff=0.08)

        with self.voiceover(
            "Bước đầu tiên của DEFLATE là LZ77: tìm kiếm các chuỗi ký tự lặp lại "
            "trong luồng delta và thay thế bằng một cặp số nhỏ gọn: offset và length."
        ) as tr:
            self.update_subtitle("LZ77 tìm chuỗi lặp trong dữ liệu Delta,\nthay bằng (offset, length) cực kỳ gọn.")
            self.play(Write(deflate_title), run_time=min(0.8, tr.duration * 0.2))
            self.play(Write(lz77_title),   run_time=min(0.6, tr.duration * 0.2))
            self.play(FadeIn(byte_boxes), FadeIn(byte_labels),
                      run_time=min(0.8, tr.duration * 0.25))
            self.play(Create(window_rect), Write(window_lbl), run_time=min(0.5, tr.duration * 0.15))
            self.play(Create(search_rect), Write(search_lbl), run_time=min(0.5, tr.duration * 0.1))
            self.play(Create(ref_arrow), Write(ref_text), run_time=min(0.5, tr.duration * 0.1))

        # ── Huffman Tree ──────────────────────────────────────────────────────
        self.play(*[FadeOut(m) for m in [
            lz77_title, byte_boxes, byte_labels,
            window_rect, window_lbl, search_rect, search_lbl,
            ref_arrow, ref_text
        ]])

        huffman_title = Text("Huffman: Cây mã hóa xác suất",
                             font_size=24, color=YELLOW, weight=BOLD)
        huffman_title.next_to(deflate_title, DOWN, buff=0.3)
        if huffman_title.width > 8.5:
            huffman_title.scale_to_fit_width(8.5)

        # Tính tần suất từ deltas thực tế
        from collections import Counter
        freq_count  = Counter(deltas)
        freq_sorted = sorted(freq_count.items(), key=lambda x: -x[1])[:4]

        # Cây Huffman: root + 2 nút giữa + 4 lá
        # Tất cả trong vùng Y: -3.0 đến +2.8
        root_pos    = UP * 2.4
        mid_pos     = [LEFT * 2.2 + UP * 1.0, RIGHT * 2.2 + UP * 1.0]
        leaf_pos    = [
            LEFT * 3.5 + DOWN * 0.5, LEFT * 1.0 + DOWN * 0.5,
            RIGHT * 1.0 + DOWN * 0.5, RIGHT * 3.5 + DOWN * 0.5
        ]

        # Kiểm tra leaf_pos không vượt vùng dưới
        for lp in leaf_pos:
            if lp[1] < -3.3:
                lp[1] = -3.0

        node_root = Circle(radius=0.32, color=WHITE, fill_color="#1A1A2E", fill_opacity=0.9).move_to(root_pos)
        root_lbl  = Text("Root", font_size=13, color=WHITE).move_to(root_pos)

        mid_nodes = VGroup(*[
            Circle(radius=0.28, color=FAMI_CYAN, fill_color="#1A2A3A", fill_opacity=0.9).move_to(p)
            for p in mid_pos
        ])

        leaf_nodes = VGroup(*[
            Circle(radius=0.26, color=SUCCESS, fill_color="#0A2A1A", fill_opacity=0.9).move_to(p)
            for p in leaf_pos
        ])
        leaf_vals   = [freq_sorted[i][0] if i < len(freq_sorted) else 0
                       for i in range(4)]
        leaf_freqs  = [freq_sorted[i][1] if i < len(freq_sorted) else 0
                       for i in range(4)]
        leaf_labels = VGroup(*[
            Text(f"Δ={v}\n({f}×)", font_size=12, color=WHITE).move_to(p)
            for v, f, p in zip(leaf_vals, leaf_freqs, leaf_pos)
        ])

        # Cạnh cây
        tree_edges = VGroup()
        for mp in mid_pos:
            tree_edges.add(Line(root_pos, mp, color=GRAY_B, stroke_width=1.5))
        for i, lp in enumerate(leaf_pos):
            tree_edges.add(Line(mid_pos[i//2], lp, color=GRAY_B, stroke_width=1.5))

        # Mã bit
        bit_codes  = ["00", "01", "10", "11"]
        code_labels = VGroup(*[
            Text(bc, font_size=14, color=YELLOW).next_to(leaf_nodes[i], DOWN, buff=0.1)
            for i, bc in enumerate(bit_codes)
        ])
        # Đảm bảo code_labels không vượt -3.4
        for lbl in code_labels:
            if lbl.get_bottom()[1] < -3.4:
                lbl.shift(UP * (abs(lbl.get_bottom()[1]) - 3.4))

        branch_lbls = VGroup()
        for i, (mp, label_str) in enumerate(zip(mid_pos, ["0", "1"])):
            mid_pt = (np.array(root_pos) + np.array(mp)) / 2
            t = Text(label_str, font_size=15, color=FAMI_SUB)
            offset = LEFT * 0.25 if i == 0 else RIGHT * 0.25
            t.move_to(mid_pt + offset)
            branch_lbls.add(t)

        # Công thức nén cuối cùng
        compress_result = MathTex(
            r"\text{Co ngót } 25\% \sim 50\%  \;\; \text{Lossless} \;\; 100\%",
            font_size=22, color=SUCCESS, tex_template=math_tex_template
        )
        compress_result.next_to(VGroup(leaf_nodes, code_labels), DOWN, buff=0.35)
        if compress_result.get_bottom()[1] < -3.3:
            compress_result.next_to(VGroup(leaf_nodes, code_labels), DOWN, buff=0.15)
        if compress_result.width > 8.5:
            compress_result.scale_to_fit_width(8.5)

        with self.voiceover(
            "Bước thứ hai của DEFLATE là mã hóa Huffman: Xây dựng một cây nhị phân "
            "dựa trên tần suất xuất hiện của từng giá trị. "
            "Giá trị nào xuất hiện nhiều nhất sẽ được gán mã bit ngắn nhất."
        ) as tr:
            self.update_subtitle("Huffman: Giá trị xuất hiện nhiều → mã bit ngắn hơn.\nTối ưu hóa không gian lưu trữ.")
            self.play(Write(huffman_title), run_time=min(0.8, tr.duration * 0.2))
            self.play(Create(tree_edges),   run_time=min(0.8, tr.duration * 0.2))
            self.play(Create(node_root), Write(root_lbl), Write(branch_lbls),
                      run_time=min(0.7, tr.duration * 0.2))
            self.play(Create(mid_nodes),    run_time=min(0.5, tr.duration * 0.15))
            self.play(Create(leaf_nodes), Write(leaf_labels),
                      run_time=min(0.8, tr.duration * 0.15))
            self.play(Write(code_labels),   run_time=min(0.5, tr.duration * 0.1))

        # ━━ 4C: KẾT QUẢ – PNG LOSSLESS TRỰC TIẾP TRÊN MONALISA ━━━━━━━━━━━━━

        self.play(*[FadeOut(m) for m in self.mobjects if m is not title])

        # Tạo ảnh PNG và ảnh gốc để so sánh
        import io as _io
        buf_png = _io.BytesIO()
        pil_img.save(buf_png, format='PNG')
        buf_png.seek(0)
        pil_png_restored = PILImage.open(buf_png).copy()

        RESULT_H = 3.6
        RESULT_W = RESULT_H * (img_w / img_h)
        total_rw = RESULT_W * 2 + 0.5
        if total_rw > 8.5:
            sf = 8.5 / total_rw
            RESULT_H *= sf
            RESULT_W *= sf

        mob_raw = ImageMobject(pil_img)
        mob_png = ImageMobject(pil_png_restored)
        mob_raw.height = RESULT_H
        mob_png.height = RESULT_H
        mob_raw.move_to(LEFT  * (RESULT_W / 2 + 0.25) + UP * 0.5)
        mob_png.move_to(RIGHT * (RESULT_W / 2 + 0.25) + UP * 0.5)

        lbl_raw = Text("Dữ liệu thô\n~47 MB",    font_size=18, color=RED)
        lbl_png = Text("Sau nén PNG\n~8–12 MB",   font_size=18, color=FAMI_CYAN)
        lbl_raw.next_to(mob_raw, DOWN, buff=0.15)
        lbl_png.next_to(mob_png, DOWN, buff=0.15)

        frame_raw = SurroundingRectangle(mob_raw, color=RED,      buff=0.05, stroke_width=2)
        frame_png = SurroundingRectangle(mob_png, color=FAMI_CYAN, buff=0.05, stroke_width=2)

        checkmark = Text("✓ Không mất 1 bit nào!", font_size=22, color=SUCCESS, weight=BOLD)
        checkmark.next_to(Group(mob_raw, mob_png), DOWN, buff=0.15)
        if checkmark.get_bottom()[1] < -3.3:
            checkmark.move_to(DOWN * 2.9)
        checkmark_lbl = checkmark

        # Thanh so sánh kích thước file
        BAR_MAX = 5.5
        raw_bar = Rectangle(width=BAR_MAX, height=0.5,
                             fill_color=RED, fill_opacity=0.8, stroke_width=0)
        png_bar = Rectangle(width=BAR_MAX * 0.3, height=0.5,
                             fill_color=FAMI_CYAN, fill_opacity=0.8, stroke_width=0)

        raw_bar_lbl = Text("RAW: ~47 MB", font_size=18, color=RED)
        png_bar_lbl = Text("PNG: ~8 MB",  font_size=18, color=FAMI_CYAN)

        bars_group = VGroup(
            VGroup(raw_bar, raw_bar_lbl).arrange(RIGHT, buff=0.2),
            VGroup(png_bar, png_bar_lbl).arrange(RIGHT, buff=0.2),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        bars_group.next_to(Group(mob_raw, mob_png), DOWN, buff=0.1)
        if bars_group.get_bottom()[1] < -3.4:
            bars_group.scale_to_fit_height(3.4 + bars_group.get_top()[1])
            bars_group.align_to(DOWN * 3.4, DOWN)
        if bars_group.width > 8.5:
            bars_group.scale_to_fit_width(8.5)
        bars_group.move_to(DOWN * 2.5 + LEFT * 0.5)

        with self.voiceover(
            "Kết quả cuối cùng: Thuật toán P N G có thể co ngót kích thước tệp "
            "từ 25 đến 50 phần trăm mà không đánh rơi dù chỉ một hạt nhiễu nhỏ nhất, "
            "cho phép khôi phục hình ảnh với độ sắc nét tuyệt đối 100 phần trăm."
        ) as tr:
            self.update_subtitle("PNG co ngót 25–50% mà không mất\ndù chỉ một bit dữ liệu!")
            self.play(FadeIn(mob_raw), Create(frame_raw), Write(lbl_raw),
                      run_time=min(0.8, tr.duration * 0.2))
            self.play(FadeIn(mob_png), Create(frame_png), Write(lbl_png),
                      run_time=min(0.8, tr.duration * 0.2))
            # Hiệu ứng so sánh 2 ảnh
            self.play(Indicate(frame_png, scale_factor=1.02, color=SUCCESS),
                      run_time=min(0.6, tr.duration * 0.15))
            self.play(
                FadeIn(bars_group[0]), run_time=min(0.7, tr.duration * 0.2)
            )
            self.play(
                FadeIn(bars_group[1]), run_time=min(0.7, tr.duration * 0.2)
            )

        # Alpha channel
        self.play(
            FadeOut(mob_raw), FadeOut(frame_raw), FadeOut(lbl_raw),
            FadeOut(mob_png), FadeOut(frame_png), FadeOut(lbl_png),
            FadeOut(bars_group),
            run_time=0.6
        )

        checkerboard_group = VGroup()
        TILE = 0.35
        COLS_CB, ROWS_CB = 14, 6
        for row in range(ROWS_CB):
            for col in range(COLS_CB):
                color_cb = GRAY_D if (row + col) % 2 == 0 else WHITE
                t = Square(side_length=TILE)
                t.set_fill(color_cb, opacity=1)
                t.set_stroke(width=0)
                t.move_to(
                    RIGHT * (col - COLS_CB/2 + 0.5) * TILE +
                    UP * (row - ROWS_CB/2 + 0.5) * TILE +
                    UP * 0.5
                )
                checkerboard_group.add(t)

        # Kiểm tra checkerboard nằm trong vùng an toàn
        if checkerboard_group.get_bottom()[1] < -3.4:
            checkerboard_group.shift(UP * (abs(checkerboard_group.get_bottom()[1]) - 3.4))

        # Đặt ảnh Monalisa lên checkerboard (mô phỏng trong suốt)
        thumb_alpha = ImageMobject(pil_img)
        thumb_alpha.height = TILE * ROWS_CB
        thumb_alpha.move_to(checkerboard_group.get_center())
        thumb_alpha.set_opacity(0.75)  # mô phỏng alpha transparency

        alpha_label = Text("Alpha channel → Trong suốt!", font_size=22, color=FAMI_CYAN, weight=BOLD)
        alpha_label.next_to(checkerboard_group, DOWN, buff=0.2)
        if alpha_label.get_bottom()[1] < -3.4:
            alpha_label.move_to(checkerboard_group.get_bottom() + UP * 0.2)

        with self.voiceover(
            "PNG còn hỗ trợ kênh Alpha, cho phép tách nền trong suốt "
            "với độ sắc nét tuyệt đối, không viền mờ. "
            "Đây là lý do PNG không thể thiếu trong đồ họa thiết kế."
        ) as tr:
            self.update_subtitle("PNG hỗ trợ kênh Alpha – trong suốt với độ sắc nét\ntuyệt đối. Không thể thiếu trong đồ họa!")
            self.play(FadeIn(checkerboard_group), run_time=min(0.8, tr.duration * 0.3))
            self.play(FadeIn(thumb_alpha),         run_time=min(0.8, tr.duration * 0.3))
            self.play(Write(alpha_label),           run_time=min(0.6, tr.duration * 0.2))

        # ── Tổng kết cuối ─────────────────────────────────────────────────────
        self.play(
            FadeOut(checkerboard_group, thumb_alpha, alpha_label),
            run_time=0.6
        )

        summary = VGroup(
            Text("JPG  :  Nén tổn hao  |  Tỉ lệ nén cao  |  Mất data",
                 font_size=20, color=ORANGE),
            Text("PNG  :  Nén không tổn hao  |  Lossless  |  Alpha",
                 font_size=20, color=FAMI_CYAN),
            Text("Pixel = Ma trận  |  RGB Tensor  |  DCT  |  DEFLATE",
                 font_size=17, color=GRAY_A),
        ).arrange(DOWN, buff=0.35)
        summary.move_to(UP * 0.5)
        if summary.get_bottom()[1] < -3.3:
            summary.move_to(ORIGIN)
        if summary.width > 8.5:
            summary.scale_to_fit_width(8.5)

        with self.voiceover(
            "Tóm lại: J P G và P N G là hai trường phái hoàn toàn khác nhau "
            "phục vụ những mục tiêu khác nhau. "
            "Hiểu bản chất toán học phía sau giúp bạn lựa chọn định dạng phù hợp cho từng bài toán."
        ) as tr:
            self.update_subtitle("JPG và PNG phục vụ mục tiêu khác nhau.\nHiểu toán học giúp bạn chọn đúng định dạng!")
            self.play(Write(summary[0]), run_time=min(1.0, tr.duration * 0.3))
            self.play(Write(summary[1]), run_time=min(1.0, tr.duration * 0.3))
            self.play(Write(summary[2]), run_time=min(0.8, tr.duration * 0.2))

        self.wait(1.5)
        self.play(*[FadeOut(m) for m in self.mobjects])


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SCENE GỘP TOÀN BỘ PHẦN 2-3-4
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class FullVideo(FaMIBaseScene):
    """
    Ghép Phần 2, 3, 4 liên tiếp trong một Scene.
    Dùng để render liền mạch cùng với BirthOfPixelScript (Phần 1).
    """
    def construct(self):
        BirthOfPixelScript.construct(self)
        RGBTensorScene.construct(self)
        JPGScene.construct(self)
        PNGScene.construct(self)