from skills.fami_lib import *

class Scene1_Hook(FaMIBaseScene):
    def construct(self):
        # SKILL 1: Tạo tiêu đề chuẩn (Tự động đậm, tự động đúng vị trí)
        title = self.create_title("Làm sao để phân loại", "Email Spam?")

        # SKILL 2: Vẽ nội dung chính (Agent tập trung vào đây)
        envelope = Rectangle(width=2, height=1.5, color=WHITE).shift(UP*0.5)
        
        # SKILL 3: Đồng bộ thoại & Phụ đề
        text_audio = "Làm sao để phân loại Email Spam?"
        with self.voiceover(text=text_audio) as tracker:
            self.update_subtitle(text_audio) # Luôn gọi skill này đầu khối with
            
            # Chia tỉ lệ thời gian (VD: 40% hiện tiêu đề, 60% hiện hình)
            self.play(Write(title), run_time=tracker.duration * 0.4)
            self.play(FadeIn(envelope), run_time=tracker.duration * 0.6)

        # SKILL 4: Kết thúc
        self.finish_scene()