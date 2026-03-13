# KHUÔN MẪU CODE (OPEN-ENDED BLUEPRINTS)

Bạn BẮT BUỘC phải dùng "Vỏ bao" (Import, Title, Voiceover) của các template này. Tuy nhiên, đối với phần **NỘI DUNG CHÍNH (MAIN STAGE)**, bạn được toàn quyền sáng tạo bằng sức mạnh của Manim. Đừng chỉ dùng Text khô khan!

## 1. TEMPLATE SCENE 1 & 2 (DÀNH CHO SỰ SÁNG TẠO TỐI ĐA)
*Áp dụng cho Hook và Main Body. Hãy dùng hình khối, đồ thị, ẩn dụ hình học tại đây.*

```python
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from skills.fami_lib import *

class Scene_Name(FaMIBaseScene):
    def construct(self):
        title = self.create_title("DÒNG 1", "DÒNG 2")
        
        # ==========================================
        # 🎨 VÙNG SÁNG TẠO (CREATIVE ZONE)
        # Đừng chỉ dùng Text! Hãy tạo ra các cấu trúc Manim độc đáo:
        # - Nếu nói về cân bằng: Vẽ một cái bập bênh.
        # - Nếu nói về quá trình: Vẽ Node, Arrow, Graph.
        # - Nếu là số liệu: Vẽ BarChart, PieChart.
        # Đảm bảo toàn bộ nhóm này nằm trong vùng Y từ -3.5 đến +3.5
        # ==========================================
        
        # ... (Tự code Mobjects của bạn ở đây) ...

        # ==========================================
        # 🎬 ĐỒNG BỘ VOICEOVER CHUẨN
        # ==========================================
        with self.voiceover(text="[Thoại đoạn 1]") as tracker:
            self.update_subtitle("[Phụ đề 1]")
            self.play(Write(title), run_time=min(1.0, tracker.duration * 0.3))
            
            # ... (Tự thiết kế Animation hiện ra cho Mobjects của bạn) ...
            
        self.finish_scene()
```

## 2. TEMPLATE SCENE 3 (TAKEAWAYS / KIẾN THỨC LÕI)
*Thường là thanh tìm kiếm hoặc thẻ ghi nhớ (Flashcard).*
*(Agent: Bạn CÓ THỂ dùng hiệu ứng thanh Search gõ chữ, nhưng NẾU kịch bản phù hợp hơn với việc hiện 3 Thẻ Flashcard, hoặc 1 Biểu đồ tư duy (Mindmap), hãy tự do thay đổi!)*

```python
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from skills.fami_lib import *

class Scene3_Takeaways(FaMIBaseScene):
    def construct(self):
        title = self.create_title("TỪ KHÓA QUAN TRỌNG")
        
        # 🎨 VÙNG SÁNG TẠO: 
        # (Tự code hiệu ứng tổng kết tại đây)
        
        with self.voiceover(text="[Thoại]") as tracker:
            self.update_subtitle("[Phụ đề]")
            self.play(Write(title))
            # (Play Animations)

        self.finish_scene()
```

## 3. TEMPLATE SCENE 4 (CTA - KÊU GỌI HÀNH ĐỘNG)
Scene này cần sự rõ ràng, dứt khoát. Giữ form chuẩn.
```python
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from skills.fami_lib import *

class Scene4_CTA(FaMIBaseScene):
    def construct(self):
        # 1. Câu hỏi lớn (Luôn dùng MarkupText)
        question = MarkupText(f'Câu hỏi: <span color="{ACCENT}">[Từ khóa nổi bật]</span>?', font="Segoe UI", font_size=42, weight=BOLD)
        question.next_to(self.logo, DOWN, buff=1.5)
        if question.width > 7.5: question.scale_to_fit_width(7.5)

        # 🎨 Tùy biến đối tượng minh họa nhỏ ở giữa (nếu cần)

        # 2. Lời kêu gọi (Luôn ở dưới cùng an toàn Y = -3.0)
        cta_box = RoundedRectangle(height=1.2, width=6.5, color=FAMI_CYAN)
        cta_text = Text("Comment câu trả lời!", font="Segoe UI", font_size=32).move_to(cta_box)
        cta_group = VGroup(cta_box, cta_text).move_to(DOWN * 3.0)

        with self.voiceover(text="[Thoại]") as tracker:
            self.update_subtitle("[Phụ đề]")
            self.play(Write(question))
            self.play(FadeIn(cta_group, shift=UP*0.5))

        self.finish_scene()
```