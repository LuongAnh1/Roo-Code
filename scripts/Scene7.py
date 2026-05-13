import sys
import os
import numpy as np
# [QUY TẮC 1: HACK PATH]
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from skills.fami_lib import *

class Scene7_InputNormalization(FaMIBaseScene):
    def construct(self):
        # 1. KHÔI PHỤC TIÊU ĐỀ & LOGO (Để đảm bảo tính liên kết)
        title = self.create_title("BƯỚC 3: CHUẨN HÓA DỮ LIỆU", "INPUT NORMALIZATION")
        self.add(title)
        
        # 2. KHỞI TẠO ASSETS CHO CẢNH NÀY
        # Tấm ảnh mèo hoặc một tập hợp ảnh đại diện cho ImageNet
        imagenet_preview = VGroup(*[
            Square(side_length=1.0, stroke_width=0, fill_opacity=0.6, fill_color=FAMI_BLUE)
            for _ in range(6)
        ]).arrange_in_grid(2, 3, buff=0.2).move_to(ORIGIN)
        
        # Nhãn ImageNet
        label_imagenet = Text("Tập dữ liệu ImageNet", font="Segoe UI", font_size=32, color=FAMI_CYAN, weight=BOLD).next_to(imagenet_preview, UP, buff=0.5)

        # Đoạn mã PyTorch (Tech style)
        code_box = RoundedRectangle(width=8.0, height=1.2, corner_radius=0.1, fill_color=BLACK, fill_opacity=0.9, stroke_color=GRAY)
        code_text = Text("transforms.Normalize(mean=[0.485, 0.456, 0.406],\n                     std=[0.229, 0.224, 0.225])", 
                         font="Consolas", font_size=20, color=ACCENT).move_to(code_box)
        pytorch_grp = VGroup(code_box, code_text).move_to(DOWN * 2.5)

        # ==========================================
        # 🎬 ĐỒNG BỘ VOICEOVER
        # ==========================================

        with self.voiceover(text="Trong thực tế với PyTorch, ta thường dùng kỹ thuật Input Normalization dựa trên các thông số của tập dữ liệu ImageNet.") as tracker:
            self.update_subtitle("Trong thực tế với PyTorch, ta thường dùng Input Normalization (ImageNet).")
            
            # Hiện tiêu đề
            # self.play(FadeIn(title), run_time=0.5)
            
            # Hiện tập dữ liệu ImageNet
            self.play(FadeIn(imagenet_preview, scale=0.8), Write(label_imagenet), run_time=tracker.duration * 0.5)

        with self.voiceover(text="Điều này giúp mọi bức ảnh, dù được chụp từ bất kỳ thiết bị nào, cũng đều được đưa về cùng một hệ quy chiếu chung mà các mô hình AI lớn nhất thế giới đã được làm quen.") as tracker:
            self.update_subtitle("Giúp mọi bức ảnh đưa về cùng hệ quy chiếu chung.")
            
            # Hiện code PyTorch - thể hiện sự "chuẩn hóa"
            self.play(FadeIn(pytorch_grp, shift=UP*0.3), run_time=min(1.0, tracker.duration * 0.4))
            
            # Hiệu ứng: Các ô vuông xanh (ảnh) chạy qua code và đồng nhất về một màu (ví dụ: màu trắng nhạt)
            self.play(
                imagenet_preview.animate.set_color(WHITE).set_opacity(0.8),
                run_time=tracker.duration * 0.4
            )
            self.wait(tracker.get_remaining_duration())

        # Dọn dẹp để sang phần Normalization Layer (nếu có)
        self.play(FadeOut(VGroup(imagenet_preview, label_imagenet, pytorch_grp)), run_time=0.6)
        
        # ==========================================
        # 🎬 ĐOẠN 2: CHUẨN HÓA LỚP TRUNG GIAN (INTERMEDIATE NORMALIZATION)
        # ==========================================

        # 1. TẠO MẠNG NƠ-RON (Phóng to và đẩy xuống dưới)
        layers_config = [5, 6, 6, 4]
        colors = [FAMI_BLUE, ORANGE, ORANGE, FAMI_CYAN]
        
        nn_layers = VGroup()
        for i, count in enumerate(layers_config):
            layer = VGroup(*[Circle(radius=0.18, color=colors[i], fill_opacity=1) for _ in range(count)])
            layer.arrange(DOWN, buff=0.35)
            nn_layers.add(layer)
        nn_layers.arrange(RIGHT, buff=1.2).scale(1.5).move_to(DOWN * 1.2) # Phóng to & đẩy xuống

        # Tạo đường nối
        edges = VGroup()
        for i in range(len(nn_layers) - 1):
            for node_a in nn_layers[i]:
                for node_b in nn_layers[i+1]:
                    edges.add(Line(node_a.get_center(), node_b.get_center(), stroke_width=1, stroke_opacity=0.2))
        neural_net = VGroup(edges, nn_layers)

        # 2. MA TRẬN BIẾN ĐỔI (Luôn nằm trên mạng nơ-ron)
        val_m = ValueTracker(0.5)
        def get_mat():
            v = val_m.get_value()
            return Matrix([[f"{v:.2f}", f"{-v:.2f}"], [f"{v*2:.2f}", f"{0.1:.2f}"]]).scale(0.7).next_to(neural_net, UP, buff=0.8)
        
        dynamic_matrix = always_redraw(get_mat)

        # ==========================================
        # 🎬 ANIMATION (SÓNG ÁNH SÁNG + MA TRẬN NHẢY SỐ)
        # ==========================================
        # 1. Câu thoại cảnh báo: "Nhưng chờ đã..."
        with self.voiceover(text="Nhưng chờ đã, chuẩn hóa ở đầu vào thôi là chưa đủ!") as tracker:
            self.update_subtitle("Nhưng chờ đã, chuẩn hóa ở đầu vào thôi là chưa đủ!")
            
            # Xóa các asset ImageNet của đoạn trước
            self.play(FadeOut(VGroup(imagenet_preview, label_imagenet, pytorch_grp)), run_time=0.5)
            
            # Hiện thông báo cảnh báo đỏ rực giữa màn hình
            alert_box = RoundedRectangle(width=6, height=1.2, color=DANGER, fill_opacity=0.2).move_to(ORIGIN)
            alert_text = Text("⚠️ DỮ LIỆU BIẾN ĐỘNG!", font="Segoe UI", font_size=30, color=DANGER, weight=BOLD).move_to(alert_box)
            
            self.play(FadeIn(alert_box, scale=1.2), Write(alert_text), run_time=0.8)
            self.play(Indicate(alert_box, color=DANGER), run_time=tracker.get_remaining_duration())

        # 2. Câu thoại mô tả lỗi: "Khi dữ liệu đi sâu vào..."
        with self.voiceover(text="Khi dữ liệu đi sâu vào hàng chục lớp nơ-ron bên trong, các con số lại bắt đầu bị biến động và méo mó.") as tracker:
            self.update_subtitle("Khi dữ liệu đi sâu vào các lớp nơ-ron, các con số bắt đầu biến động và méo mó.")
            
            # Tắt cảnh báo, hiện mạng nơ-ron và ma trận méo mó
            self.play(FadeOut(alert_box), FadeOut(alert_text), run_time=0.4)
            self.play(FadeIn(neural_net), FadeIn(dynamic_matrix), run_time=0.8)
            
            # Animation sáng dần từng lớp
            for i in range(len(nn_layers)):
                # Cho ma trận "nhảy số" khi lớp sáng lên
                self.play(
                    nn_layers[i].animate.set_stroke(WHITE, width=6).set_fill(opacity=1),
                    val_m.animate.set_value(np.random.uniform(-5, 5)),
                    run_time=0.3
                )
                if i > 0:
                    self.play(nn_layers[i-1].animate.set_stroke(width=0).set_fill(opacity=0.3), run_time=0.2)
                self.wait(1.0)

        # 3. LỚP CHUẨN HÓA (NORM LAYER)
        with self.voiceover(text="Giải pháp của các kỹ sư là chèn hẳn những lớp chuẩn hóa vào ngay giữa mạng CNN.") as tracker:
            self.update_subtitle("Giải pháp: Chèn các Lớp chuẩn hóa (Normalization Layers) vào giữa mạng.")
            
            # Thay vì hình chữ nhật đặc, ta dùng khung viền neon mỏng quanh lớp ẩn
            # Lấy layer thứ 2 (index 1) hoặc 3 (index 2) để chèn
            target_layer = nn_layers[1] 
            
            # Tạo khung bao quanh lớp ẩn (làm nó trông như đang được "đóng gói" để chuẩn hóa)
            norm_layer = SurroundingRectangle(target_layer, color=SUCCESS, buff=0.2, stroke_width=4)
            norm_lbl = Text("NORM LAYER", font="Segoe UI", font_size=20, color=SUCCESS, weight=BOLD)
            norm_lbl.next_to(norm_layer, UP, buff=0.1)
            
            # Hiệu ứng quét sáng (Glow) cho lớp Norm
            self.play(
                Create(norm_layer),
                Write(norm_lbl),
                # Làm mờ nhẹ phần còn lại của mạng để làm nổi bật vùng Norm
                neural_net.animate.set_opacity(0.4),
                # Giữ nguyên độ sáng của lớp đang được chuẩn hóa
                target_layer.animate.set_opacity(1),
                run_time=1.0
            )
            
            # Hiệu ứng ổn định: Ma trận phía trên chuyển sang màu Xanh Success
            self.play(
                dynamic_matrix.animate.set_color(SUCCESS),
                val_m.animate.set_value(0.1), # Số nhỏ ổn định
                run_time=0.8
            )
            
            # Nhấp nháy nhẹ để báo hiệu "Đã xử lý xong"
            self.play(Indicate(norm_layer, color=SUCCESS), run_time=0.6)
            self.wait(tracker.get_remaining_duration())

        self.finish_scene()