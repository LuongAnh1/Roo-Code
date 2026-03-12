import sys
import os
# ✅ RULE 1: Luôn có Hack Path để Python tìm thấy folder skills ngang hàng
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from skills.fami_lib import *

class Scene_Template(FaMIBaseScene):
    def construct(self):
        # 1. KHỞI TẠO ĐỐI TƯỢNG (Khai báo trước khi play)
        # ✅ RULE 2: Tiêu đề luôn gọi skill create_title
        title = self.create_title("DÒNG TIÊU ĐỀ 1", "Dòng tiêu đề 2 (tùy chọn)")

        # ✅ RULE 3: Nội dung chính đặt dưới tiêu đề (next_to) để tránh đè Logo
        box = RoundedRectangle(corner_radius=0.2, color=FAMI_CYAN, height=2, width=4)
        box.next_to(title, DOWN, buff=1.0)
        
        # ✅ RULE 4: Ép kích thước ngang 7.5 để chống tràn viền mobile
        main_group = VGroup(box).center().shift(UP * 0.5) # Căn chỉnh lại nhóm nếu cần
        if main_group.width > 7.5:
            main_group.scale_to_fit_width(7.5)

        # 2. KỊCH BẢN & ĐỒNG BỘ
        with self.voiceover(text="Đây là câu thoại mẫu để Agent bắt chước.") as tracker:
            # ✅ RULE 5: update_subtitle luôn nằm dòng đầu tiên của khối voiceover
            self.update_subtitle("Đây là câu thoại mẫu để Agent bắt chước.")
            
            # ✅ RULE 6: Animation xuất hiện dùng min() để dứt khoát (không quá 1.5s)
            self.play(Write(title), run_time=min(1.2, tracker.duration * 0.4))
            
            # ✅ RULE 7: Chia tỉ lệ % thời gian sao cho tổng không quá 0.8 (Quy tắc 80%)
            self.play(FadeIn(box, scale=0.5), run_time=tracker.duration * 0.4)
            
            # Manim sẽ tự động chờ 20% thời lượng âm thanh còn lại
        
        # 3. KẾT THÚC
        self.wait(1) # Khoảng nghỉ ngắn để ghép video mượt hơn