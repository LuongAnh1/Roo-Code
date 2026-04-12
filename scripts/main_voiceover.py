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

class mainScenewithvoice(FaMIBaseScene):
    def construct(self):
        # Thiết lập dịch vụ voiceover (nếu cần thiết, giả sử FaMIBaseScene đã lo liệu hoặc dùng mặc định)
        # Nếu chưa có trong FaMIBaseScene, có thể thêm:
        # self.set_speech_service(GTTSService(lang="vi"))

        # 1. Setup + subscene 1
        title = self.create_title("XÁC SUẤT LỖI BIT")
        grid = NumberPlane(
            x_range=[-8, 8, 1],
            y_range=[-4.5, 4.5, 1],
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 2,
                "stroke_opacity": 0.3
            },
            axis_config={
                "stroke_width": 0,
                "include_tip": False,
            }
        )
        text_0 = Tex(r"BEP\\(Bit Error Probability)")
        text_1 = Tex(r"Xác suất lỗi bit, được định nghĩa là xác suất để một bit bất kỳ bị sai trạng thái (từ 0 thành 1 hoặc ngược lại) sau khi đi qua kênh truyền",
                 font_size=24)
        with self.voiceover(text="Chỉ số cốt lõi để đo lường độ chính xác của dữ liệu là BEP (Bit Error Probability - Xác suất lỗi bit).") as tracker:
            self.update_subtitle("Chỉ số cốt lõi để đo lường độ chính xác\ncủa dữ liệu là BEP.")
            self.play(FadeIn(VGroup(title,grid)), run_time=min(1.0, tracker.duration * 0.4))
            self.play(FadeIn(text_0), run_time=min(1.0, tracker.duration * 0.4))

        with self.voiceover(text="BEP được định nghĩa là xác suất để một bit bất kỳ bị sai trạng thái từ 0 thành 1 hoặc ngược lại sau khi đi qua kênh truyền.") as tracker:
            self.update_subtitle("BEP được định nghĩa là xác suất để một bit bất kỳ\nbị sai trạng thái sau khi đi qua kênh truyền.")
            self.play(text_0.animate.shift(UP), run_time=min(1.0, tracker.duration * 0.3))
            self.play(Write(text_1), run_time=min(2.0, tracker.duration * 0.5))

        with self.voiceover(text="Hãy quan sát một mô hình truyền dữ liệu thực tế.") as tracker:
            self.update_subtitle("Hãy quan sát một mô hình truyền dữ liệu thực tế.")
            self.play(FadeOut(VGroup(text_0, text_1)), run_time=min(1.0, tracker.duration * 0.4))

        # 2. Setup + subscene 2
        broadcasting = Broadcasting().scale(0.35)
        receiving = Receiving().scale(0.35)
        self.arrange_comparison(broadcasting, receiving)
        VGroup(broadcasting, receiving).shift(UP * 1.0)

        with self.voiceover(text="Dữ liệu gốc được gửi đi từ bộ phát và nhận được ở bộ thu thông qua kênh truyền.") as tracker:
            self.update_subtitle("Dữ liệu được gửi đi từ bộ phát và nhận được ở bộ thu.")
            self.play(FadeIn(broadcasting), FadeIn(receiving), run_time=min(1.5, tracker.duration * 0.8))

        orig_bits = "10110010"
        recv_bits_str = "00100110"
        m_bits = BitSequence(sequence=orig_bits, color="#00FF00", scale_factor=0.45)
        
        broadcasting.update_sequence(self, orig_bits, scale_factor=0.45)
        m_bits.next_to(broadcasting.icon, RIGHT)

        with self.voiceover(text="Khi truyền một chuỗi bit, nhiễu có thể làm thay đổi giá trị của chúng.") as tracker:
            self.update_subtitle("Nhiễu có thể làm thay đổi giá trị của chuỗi bit.")
            self.play(FadeIn(m_bits), run_time=min(1.0, tracker.duration * 0.2))
            self.play(m_bits.animate.next_to(receiving.icon, LEFT), run_time=min(2.0, tracker.duration * 0.6))

        with self.voiceover(text="Ở ví dụ này, chuỗi 8 bit sau khi truyền đi đã xuất hiện các lỗi sai.") as tracker:
            self.update_subtitle("Chuỗi 8 bit sau khi truyền đi đã xuất hiện các lỗi sai.")
            receiving.update_sequence(self, orig_bits, recv_bits_str, scale_factor=0.45)
            self.play(FadeOut(m_bits), run_time=min(1.0, tracker.duration * 0.4))

        # 3. Subscene 3
        with self.voiceover(text="Ta so sánh chuỗi gửi và nhận để đếm số bit lỗi cụ thể.") as tracker:
            self.update_subtitle("So sánh chuỗi gửi và nhận để đếm số bit lỗi.")
            self.play(VGroup(broadcasting, receiving).animate.move_to(UP * 2), run_time=min(1.0, tracker.duration * 0.8))

        bit_sent = broadcasting.current_seq_display.copy()
        bit_get = receiving.current_seq_display.copy()
        text_0 = Text("Có 3 bit bị lỗi", t2c={"3": RED})
        text_1 = Tex(r"BER(Bit error rate) = $\frac{3}{8} = 0.375$", font_size=48)

        with self.voiceover(text="Trong 8 bit có 3 bit bị lỗi. Tần suất lỗi bit mẫu ở đây là 0.375.") as tracker:
            self.update_subtitle("Có 3 bit bị lỗi. Tỷ lệ lỗi bit mẫu là 0.375.")
            self.play(bit_sent.animate.move_to(UP * 0).scale(2), run_time=min(1.0, tracker.duration * 0.2))
            self.play(bit_get.animate.move_to(UP * -0.5).scale(2), run_time=min(1.0, tracker.duration * 0.2))
            self.play(FadeIn(text_0.move_to(UP * -1.5)), run_time=min(1.0, tracker.duration * 0.2))
            self.play(Write(text_1.move_to(UP * -3)), run_time=min(1.0, tracker.duration * 0.2))

        with self.voiceover(text="Tuy nhiên, để đo lường chính xác, ta cần một mô hình toán học tổng quát hơn.") as tracker:
            self.update_subtitle("Để đo lường chính xác, ta cần mô hình toán học tổng quát.")
            self.play(FadeOut(VGroup(bit_sent, bit_get, text_0, text_1)), run_time=min(1.0, tracker.duration * 0.8))

        # 4. Subscene 4
        line1_1 = Tex("Việc truyền tải ", "$N$", " bit dữ liệu có thể mô phỏng thành dãy", font_size=30)
        line1_2 = Tex("$N$", " phép thử độc lập.", font_size=30)
        line2_1 = Tex("Gọi ", "$X_i$", " là biến ngẫu nhiên chỉ trạng thái của bit thứ ", "$i$,", font_size=30)
        line2_2 = Tex("$X_i \\in \\{0,1\\}$", ", trong đó:", font_size=30)
        line3 = Tex(r"$\bullet$ ", "$X_i = 1$", " là sự kiện bit thứ $i$ ", "bị lỗi", font_size=30)
        line4 = Tex(r"$\bullet$ ", "$X_i = 0$", " là sự kiện bit thứ $i$ ", "truyền đúng", font_size=30)

        line1_1[1].set_color(YELLOW)
        line1_2[0].set_color(YELLOW)
        line1_2[1].set_color(YELLOW)
        line2_1[1].set_color(BLUE)
        line2_1[3].set_color(YELLOW)
        line2_2[0].set_color(BLUE)
        line3[1].set_color(RED)
        line3[3].set_color(RED)
        line4[1].set_color("#00FF00")
        line4[3].set_color("#00FF00")

        paragraph = VGroup(line1_1, line1_2, line2_1, line2_2, line3, line4).arrange(DOWN, aligned_edge=LEFT).shift(DOWN * 1)
        line3.shift(RIGHT * 0.5)
        line4.shift(RIGHT * 0.5)

        with self.voiceover(text="Việc truyền tải N bit dữ liệu có thể được mô hình hóa thành một dãy N phép thử độc lập.") as tracker:
            self.update_subtitle("Truyền tải chuỗi bit là một dãy các phép thử độc lập.")
            self.play(Write(line1_1), run_time=min(1.5, tracker.duration * 0.4))
            self.play(Write(line1_2), run_time=min(1.5, tracker.duration * 0.4))

        with self.voiceover(text="Định nghĩa X i là biến ngẫu nhiên chỉ thị trạng thái lỗi của bit thứ i.") as tracker:
            self.update_subtitle("Gọi biến ngẫu nhiên chỉ thị trạng thái lỗi bit.")
            self.play(Write(line2_1), run_time=min(1.5, tracker.duration * 0.4))
            self.play(Write(line2_2), run_time=min(1.5, tracker.duration * 0.4))

        with self.voiceover(text="X i tuân theo Phân phối Bernoulli: nhận giá trị 1 nếu bit bị lỗi và 0 nếu được truyền đúng.") as tracker:
            self.update_subtitle("Biến ngẫu nhiên tuân theo Phân phối Bernoulli: một là lỗi, không là đúng.")
            self.play(Write(line3), run_time=min(1.5, tracker.duration * 0.4))
            self.play(Write(line4), run_time=min(1.5, tracker.duration * 0.4))

        # 5. Subscene 5
        with self.voiceover(text="Khi đó, tổng số bit lỗi E chính là tổng của các biến ngẫu nhiên này.") as tracker:
            self.update_subtitle("Tổng số bit lỗi là tổng của các biến ngẫu nhiên này.")
            text_abc = Tex(r"Tổng số bit lỗi: $E = \sum_{i = 1}^{N}X_i$", font_size=30)
            self.play(FadeOut(VGroup(paragraph, broadcasting, receiving)), run_time=min(1.0, tracker.duration * 0.8))
            self.play(Write(text_abc), run_time=min(4.0, tracker.duration * 0.8))
            self.play(FadeOut(text_abc), run_time=min(1.0, tracker.duration * 0.8))

        text_0 = Tex(r"Khi đó,", font_size=30)
        equation_0 = MathTex(r"X_i \sim \text{Bernoulli}(\text{BEP})")
        text_1 = Tex(r"Và", font_size=30)
        equation_1 = MathTex(r"\text{BER} &\sim B(N, \text{BEP}) \\")
        equation_2 = MathTex(r"\text{BEP} &\approx \frac{E}{N} = \frac{\sum_{i = 1}^{N}X_i}{N} \text{ khi } N \to \infty")
        
        n, p = 20, 0.5
        x_values = np.arange(0, n + 1)
        y_values = [stats.binom.pmf(k, n, p) for k in x_values]

        B_chart = BarChart(
            values=y_values,
            x_length=10,
            y_length=6,
            y_range=[0, 0.2, 0.05],
            axis_config={"font_size": 24},
            bar_colors=[BLUE],
            bar_fill_opacity=0.8,
            x_axis_config={"include_ticks": False},
            y_axis_config={"stroke_opacity": 0, "include_ticks": False, "include_numbers": False},
        )
        if B_chart.get_y_axis().numbers:
            B_chart.get_y_axis().numbers.set_opacity(0)

        p = 0.2
        x_values = [1 - p, p]
        
        Bernoulli_chart = BarChart(
            values=x_values,
            x_length=4,
            y_length=10,
            y_range=[0, 1, 0.2],
            axis_config={"font_size": 24},
            bar_colors=[BLUE, BLUE],
            bar_fill_opacity=0.8,
            x_axis_config={"include_ticks": False},
            y_axis_config={"stroke_opacity": 0, "include_ticks": False, "include_numbers": False},
        ).rotate(-PI / 2)
        if Bernoulli_chart.get_y_axis().numbers:
            Bernoulli_chart.get_y_axis().numbers.set_opacity(0)

        content_1 = VGroup(text_0, equation_0, Bernoulli_chart).arrange(DOWN, buff=0.5)
        text_0.align_to(equation_2, LEFT)
        Bernoulli_chart.scale(0.3).shift(UP * 1.5)

        content_2 = VGroup(text_1, equation_1, B_chart).arrange(DOWN, buff=0.5).shift(DOWN * 3.75)
        text_1.align_to(equation_2, LEFT)
        B_chart.scale(0.3).shift(UP * 1.8)

        with self.voiceover(text="Biến ngẫu nhiên E sẽ tuân theo Phân phối Nhị thức với tham số là tổng số bit N và xác suất lỗi bit BEP.") as tracker:
            self.update_subtitle("Số bit lỗi tuân theo Phân phối Nhị thức.")
            self.play(Write(content_1), run_time=min(1.5, tracker.duration * 0.2))
            self.play(content_1.animate.shift(UP * 1), run_time=min(1.0, tracker.duration * 0.15))
            self.play(Write(content_2), run_time=min(1.5, tracker.duration * 0.7))

        
        with self.voiceover(text="Theo Luật số lớn, tần suất lỗi sẽ hội tụ về xác suất lý thuyết khi N tiến tới vô cùng.") as tracker:
            self.update_subtitle("Theo Luật số lớn, trung bình mẫu hội tụ về xác suất lỗi khi kích thước mẫu tiến tới vô cùng.")            # Keep charts on screen for the next part

        with self.voiceover(text="Tuy nhiên, với các hệ thống phức tạp, việc tính toán lý thuyết là bất khả thi.") as tracker:
            self.update_subtitle("Với các hệ thống phức tạp, tính toán lý thuyết là bất khả thi.")
            # Fade out old theory charts to make room for simulation setup
            self.play(FadeOut(VGroup(content_1, content_2)), run_time=min(1.0, tracker.duration * 0.4))
            
            text_mc = Text("Mô phỏng Monte Carlo").move_to(UP * 4.8)
            self.play(Transform(title, text_mc), run_time=min(1.0, tracker.duration * 0.4))
            
            broadcasting = Broadcasting().scale(0.35)
            receiving = Receiving().scale(0.35)
            self.arrange_comparison(broadcasting, receiving, buff=1.5)
            VGroup(broadcasting, receiving).shift(UP * 3)
            self.play(FadeIn(VGroup(broadcasting, receiving)), run_time=min(1.0, tracker.duration * 0.4))

        with self.voiceover(text="Lúc này, mô phỏng Monte Carlo giúp ta xấp xỉ BEP bằng tần suất lỗi thông qua lấy mẫu lặp lại.") as tracker:
            self.update_subtitle("Lúc này, mô phỏng Monte Carlo giúp ta xấp xỉ xác suất lỗi bằng tần suất lỗi.")
            self.play(Write(equation_2), run_time=min(1.5, tracker.duration * 0.6))
            # equation_2 stays on screen during next setup

        # 6. Subscene 6
        num_packets = 50000
        error_prob = 0.15
        backend_dir = os.path.join(PROJECT_ROOT, "scripts", "backend")
        exe_path = os.path.join(backend_dir, "generate_packet")
        total_bits = num_packets * 8 
        run_cmd = [exe_path, str(total_bits), str(error_prob)]
        result = subprocess.run(run_cmd, capture_output=True, text=True, check=True)
        output_lines = result.stdout.strip().split("\n")
        full_orig_bits_str = output_lines[0]
        full_recv_bits_str = output_lines[1]

        val_tracker = ValueTracker(2)
        head_pos_container = [ORIGIN]
        
        _text_cache_main = {}
        def get_cached_text(text_str, font_size, color=WHITE, font=""):
            key = (str(text_str), font_size, color, font)
            if key not in _text_cache_main:
                kwargs = {"font_size": font_size, "weight": BOLD}
                if font: kwargs["font"] = font
                t = Text(str(text_str), **kwargs).set_color(color)
                _text_cache_main[key] = t
            return _text_cache_main[key].copy()

        lib_ext = ".dylib" if sys_lib.platform == "darwin" else ".so"
        lib_path = os.path.join(backend_dir, f"libsimulate{lib_ext}")
        ber_lib = ctypes.CDLL(lib_path)
        ber_lib.calculate_ber_array_from_str.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
        ber_lib.calculate_ber_array_from_str.restype = ctypes.POINTER(ctypes.c_double)
        ber_lib.free_ber_array.argtypes = [ctypes.POINTER(ctypes.c_double)]
        ber_lib.free_ber_array.restype = None
        out_array_size = ctypes.c_int(0)
        c_orig_bits = full_orig_bits_str.encode('utf-8')
        c_recv_bits = full_recv_bits_str.encode('utf-8')
        ber_array_ptr = ber_lib.calculate_ber_array_from_str(c_orig_bits, c_recv_bits, total_bits, 8, ctypes.byref(out_array_size))
        precomputed_ber_values = [ber_array_ptr[i] for i in range(out_array_size.value)]
        ber_lib.free_ber_array(ber_array_ptr)
            
        # Asset setup and logic moved earlier for better flow

        def get_plot():
            val = max(val_tracker.get_value(), 2) * 8
            step = val / 8
            y_max = 0.5 + 0.8 * math.exp(-(val - 2) / 50.0)
            y_step = y_max / 5
            axes = Axes(
                x_range=[0, val, step],
                y_range=[0, y_max, y_step],
                x_length=7.5, y_length=4,
                axis_config={"stroke_color": GREY_A, "include_numbers": False}
            )
            for x in np.linspace(0, val, 6):
                t = get_cached_text(str(int(x)), 16)
                t.next_to(axes.c2p(x, 0), DOWN, buff=0.1)
                axes.add(t)
            for y in np.linspace(0, y_max, 6):
                t = get_cached_text(f"{y:.2f}", 16)
                t.next_to(axes.c2p(0, y), LEFT, buff=0.1)
                axes.add(t)
            stride = 100 
            indices = list(range(0, int(val) + 1, stride))
            if indices[-1] != int(val): indices.append(int(val))
            labels = axes.get_axis_labels(x_label=Text("N", font_size=20), y_label=Text("BER", font_size=20))
            target_line = axes.plot(lambda x: 0.15, color=GREY, stroke_width=2).set_opacity(0.5)
            points = [axes.c2p(x, precomputed_ber_values[min(x // 8, len(precomputed_ber_values) - 1)]) for x in indices]
            graph = VMobject(color=YELLOW, stroke_width=4).set_points_as_corners(points)
            vgroup = VGroup(axes, labels, target_line, graph).move_to(DOWN * 0.5).scale(0.9)
            head_pos_container[0] = points[-1]
            return vgroup

        dynamic_plot = always_redraw(get_plot)
        self.add(dynamic_plot)
        
        def get_dynamic_ber_text():
            val = max(val_tracker.get_value(), 2)
            current_idx = min(int(val), len(precomputed_ber_values) - 1)
            text = get_cached_text(f"BER = {precomputed_ber_values[current_idx]:.4f}", 24)
            text.next_to(head_pos_container[0] + UP * 0.5 + LEFT * 2)
            return text

        dynamic_ber = always_redraw(get_dynamic_ber_text)
        self.add(dynamic_ber)

        b_text = BitSequence(sequence="00000000", color="#00FF00", font_size=36, scale_factor=0.27)
        b_text.next_to(broadcasting.label, DOWN, buff=0.25)
        prev_b_text = BitSequence(sequence="00000000", color="#00FF00", font_size=36, scale_factor=0.27).set_opacity(0.3)
        prev_b_text.next_to(b_text, DOWN, buff=0.15)
        r_text = VGroup(*[get_cached_text("0", 36, "#00FF00") for _ in range(8)]).arrange(RIGHT, buff=0.1).scale(0.27)
        r_text.next_to(receiving.label, DOWN, buff=0.25)
        m_bits = BitSequence(sequence="00000000", color="#00FF00", font_size=36, scale_factor=0.27)
        self.add(b_text, prev_b_text, r_text, m_bits)
        
        last_packet_idx = [-1]
        def transmission_updater(mob, dt):
            val = val_tracker.get_value()
            if val >= num_packets: return
            packet_idx = int(val)
            progress = val - packet_idx
            if packet_idx != last_packet_idx[0]:
                last_packet_idx[0] = packet_idx
                orig_bits = full_orig_bits_str[packet_idx * 8:packet_idx * 8 + 8]
                recv_bits = full_recv_bits_str[packet_idx * 8:packet_idx * 8 + 8]
                b_text.become(BitSequence(sequence=orig_bits, color="#00FF00", font_size=36, scale_factor=0.27).move_to(b_text))
                if packet_idx > 0:
                    prev_bits = full_orig_bits_str[(packet_idx - 1) * 8:(packet_idx - 1) * 8 + 8]
                    prev_b_text.become(BitSequence(sequence=prev_bits, color="#00FF00", font_size=36, scale_factor=0.27).move_to(prev_b_text).set_opacity(0.3))
                for k in range(8):
                    c = "#00FF00" if orig_bits[k] == recv_bits[k] else RED
                    r_text[k].become(get_cached_text(recv_bits[k], 36 * 0.27, c).move_to(r_text[k]))
            m_bits.become(BitSequence(sequence=full_orig_bits_str[int(val) * 8:int(val) * 8 + 8], color="#00FF00", font_size=36, scale_factor=0.27).move_to(interpolate(broadcasting.icon.get_right() + RIGHT * 0.2, receiving.icon.get_left() + LEFT * 0.2, progress)))

        m_bits.add_updater(transmission_updater)
        
        with self.voiceover(text="Khi đó, Mô phỏng Monte Carlo được sử dụng như một công cụ mạnh mẽ: lấy mẫu lặp lại nhiều lần để xấp xỉ BEP.") as tracker:
            self.update_subtitle("Mô phỏng Monte Carlo: lấy mẫu lặp lại nhiều lần để xấp xỉ xác suất lỗi.")
            self.play(FadeOut(equation_2), run_time=min(0.5, tracker.duration * 0.1))
            self.play(val_tracker.animate.set_value(num_packets), run_time=min(6.0, tracker.duration * 0.8), rate_func=lambda t: 0.05 * t + 0.95 * (t ** 5))

        m_bits.remove_updater(transmission_updater)
        self.remove(m_bits, b_text, prev_b_text, r_text)

        # 7. Subscene 7
        with self.voiceover(text="Dưới đây là bảng kết quả mô phỏng với các kích thước mẫu N khác nhau.") as tracker:
            self.update_subtitle("Bảng kết quả mô phỏng với các kích thước mẫu khác nhau.")
            self.play(FadeOut(VGroup(broadcasting, receiving, dynamic_plot, dynamic_ber)), run_time=min(1.0, tracker.duration * 0.8))

        data = [["8", f"{precomputed_ber_values[7]:.4f}"], ["64", f"{precomputed_ber_values[63]:.4f}"], ["...", "..."], ["32768", f"{precomputed_ber_values[32767]:.4f}"], ["400000", f"{precomputed_ber_values[-1]:.4f}"]]
        table = Table(data, col_labels=[Tex(r"$N$"), Tex(r"BER")], include_outer_lines=True).scale(0.6).shift(UP * 1.5)
        
        with self.voiceover(text="Phương pháp Monte Carlo khẳng định: với N đủ lớn, ta có thể dùng tần suất xuất hiện lỗi để xấp xỉ chính xác xác suất lỗi.") as tracker:
            self.update_subtitle("Với kích thước mẫu đủ lớn, tần suất lỗi xấp xỉ chính xác xác suất lỗi.")
            self.play(Create(table.get_horizontal_lines()), Create(table.get_vertical_lines()), run_time=min(2.0, tracker.duration * 0.3))
            self.play(FadeIn(table.get_entries()), run_time=min(1.5, tracker.duration * 0.3))
            text_0 = Tex(r"$\Rightarrow$ BEP $\approx 0.15$", font_size=48).move_to(DOWN * 2.25)
            self.play(Write(text_0), run_time=min(1.0, tracker.duration * 0.4))

        self.finish_scene()
