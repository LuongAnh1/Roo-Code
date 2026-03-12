# TIÊU CHUẨN KỸ THUẬT CODE MANIM (ANTI-BUG MANUAL)

File này tập trung vào quy chuẩn lập trình để tránh Crash và lỗi logic. Các quy tắc về Thẩm mỹ và Âm thanh hãy xem tại các file tương ứng.

## 1. CẤU TRÚC FILE & HACK PATH (MANDATORY)
Mọi file code Scene bắt buộc bắt đầu bằng:
  ```python
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from skills.fami_lib import *
  ```

- **Kế thừa**: Luôn dùng `class SceneName(FaMIBaseScene):`

## 2. QUY TẮC PHÒNG CHỐNG CRASH (CRITICAL)
- **Hằng số**: TUYỆT ĐỐI KHÔNG dùng `CENTER`. Bắt buộc dùng `ORIGIN`. Căn giữa `VGroup` dùng `aligned_edge=ORIGIN`.
- **VGroup rỗng**: CẤM gọi `.next_to()`, `.align_to()` hoặc `.match_y()` trên một `VGroup()` chưa có phần tử.
- Text Anti-Crash:
    CẤM dùng `get_part_by_text()` hoặc `set_color_by_text()` trên đối tượng Text.
    BẮT BUỘC dùng `MarkupText` và thẻ `<span>` để tô màu từng phần.
- **Updater an toàn**: CẤM dùng `self.get_time().` BẮT BUỘC dùng `self.renderer.time.` Không khởi tạo Mobject mới trong updater.

## 3. HIỆU ỨNG GÕ CHỮ (TYPING) - CHỐNG LỆCH TUYỆT ĐỐI
Sử dụng logic "Khóa trục Y" để chữ không bị bay ra ngoài hoặc nhảy nhấp nhô:
  ```python
  last_char = reference_obj # Vật thể mốc có sẵn (ví dụ: kính lúp)
  current_buff = 0.3 
  for i, char in enumerate(text_str):
      if char == " ":
          current_buff = 0.2 # Gặp dấu cách: tăng khoảng cách, không tạo object
          continue
      new_char = Text(char, font="Segoe UI", font_size=40)
      new_char.next_to(last_char, RIGHT, buff=current_buff, aligned_edge=DOWN)
      new_char.match_y(reference_obj) # KHÓA CHẾT TRỤC Y THEO VẬT THỂ MỐC
      self.play(FadeIn(new_char), run_time=0.08)
      last_char, current_buff = new_char, 0.05
  ```

## 4. QUY ĐỊNH TOÁN HỌC & LATEX
- **Thư viện**: Luôn dùng `import numpy as np`. Sử dụng tiền tố `np.sin()`, `np.cos()`, `np.pi`.
- **LaTeX**: Luôn dùng chuỗi `raw MathTex(r"...")`. Nếu công thức dài, bắt buộc dùng `.scale_to_fit_width(7.5)`.

## 5. MÃ HÓA & LƯU FILE (ENCODING)
- **UTF-8**: Đảm bảo file lưu định dạng UTF-8.
- **Dấu nháy**: Trong MarkupText, dùng dấu nháy đơn bao ngoài dấu nháy kép '..."..."...' để tránh lỗi cú pháp Python khi định nghĩa màu.

