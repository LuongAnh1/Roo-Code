from skills.fami_lib import *

class Scene_Template(FaMIBaseScene):
    def construct(self):
        # 1. TIÊU ĐỀ (Luôn dùng Skill có sẵn)
        title = self.create_title("Dòng 1", "Dòng 2")

        # 2. KHỞI TẠO ĐỐI TƯỢNG (Khai báo trước khi play)
        box = RoundedRectangle(corner_radius=0.2, color=FAMI_CYAN).center()
        
        # 3. KỊCH BẢN & ĐỒNG BỘ
        with self.voiceover(text="Câu thoại chia làm 2 ý nhỏ.") as tracker:
            # Bật phụ đề ngay lập tức
            self.update_subtitle("Câu thoại chia làm 2 ý nhỏ.")
            
            # Ý 1 (Chiếm 40% thời lượng)
            self.play(Write(title), run_time=tracker.duration * 0.4)
            
            # Ý 2 (Chiếm phần còn lại)
            self.play(FadeIn(box, shift=UP*0.5), run_time=tracker.duration * 0.6)
            
            # Lưu ý: Tuyệt đối KHÔNG dùng self.wait() trong khối này.
        
        # Kết thúc scene an toàn
        self.wait(1)