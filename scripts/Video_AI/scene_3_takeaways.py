import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from skills.fami_lib import *
from skills.fami_effects import *

class Scene3_Takeaways(FaMIBaseScene):
    def construct(self):
        title = self.create_title("5 TỪ KHÓA", "QUAN TRỌNG")
        
        keywords = [
            "1. Convolution Layer",
            "2. Affine Transformation",
            "3. Spatial Transformer Networks (STN)",
            "4. Data Augmentation",
            "5. Normalization Layer"
        ]
        
        cards = VGroup()
        for kw in keywords:
            # Tạo hiệu ứng thẻ Flashcard với viền đậm Gradient và nền trong nhạt
            card_bg = RoundedRectangle(width=7.0, height=0.9, corner_radius=0.15, fill_color=BLACK, fill_opacity=0.2, stroke_color=WHITE, stroke_width=5)
            apply_fami_gradient(card_bg)
            
            # Tô màu vàng phần số đếm "1.", "2.", ... để nổi bật
            if "." in kw:
                parts = kw.split(".", 1)
                formatted_kw = f'<span foreground="{ACCENT}">{parts[0]}.</span> {parts[1]}'
            else:
                formatted_kw = kw
                
            text = MarkupText(formatted_kw, font="Segoe UI", font_size=28, weight=BOLD, color=WHITE).move_to(card_bg)
            
            # Ép khung chữ nếu quá dài
            if text.width > card_bg.width * 0.9:
                text.scale_to_fit_width(card_bg.width * 0.9)
                
            card = VGroup(card_bg, text)
            cards.add(card)
        
        cards.arrange(DOWN, buff=0.3)
        cards.move_to(ORIGIN)
        
        # Đưa khối cards nhích lên một chút nếu bị gần phụ đề
        if cards.get_bottom()[1] < -3.0:
            cards.shift(UP * 0.5)

        # ==========================================
        # 🎬 ĐỒNG BỘ VOICEOVER CHUẨN
        # ==========================================
        with self.voiceover(text="Và đừng quên lưu lại các từ khóa này để tìm hiểu sâu hơn nhé!") as tracker:
            self.update_subtitle("Và đừng quên lưu lại các từ khóa này để tìm hiểu sâu hơn nhé!")
            
            self.play(Write(title), run_time=min(0.5, tracker.duration * 0.2))
            
            # Bắn lần lượt từng thẻ (Flashcard pop-in)
            self.play(
                LaggedStart(
                    *[FadeIn(card, shift=UP*0.5, scale=0.8) for card in cards],
                    lag_ratio=0.15
                ),
                run_time=min(2.0, tracker.duration * 0.7)
            )
            
            # Highlight thẻ ở lại trên màn hình
            self.play(
                LaggedStart(
                    *[Indicate(card, color=ACCENT) for card in cards],
                    lag_ratio=0.1
                ),
                run_time=min(1.5, tracker.duration * 0.1)
            )
            
        self.finish_scene()
