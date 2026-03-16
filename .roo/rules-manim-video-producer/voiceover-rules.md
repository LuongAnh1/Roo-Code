# QUY TẮC ĐỒNG BỘ THỜI GIAN (VOICEOVER & PACING)

Để video TikTok có nhịp độ nhanh, dứt khoát và không bị "chết hình", Agent BẮT BUỘC tuân thủ 4 quy tắc tính toán thời gian sau:

## 1. CẤU TRÚC KHỐI VOICEOVER CHUẨN (MANDATORY)
Mọi khối lệnh âm thanh phải bắt đầu bằng việc kích hoạt Phụ đề (Subtitle). CẤM đặt `self.play` ở ngoài khối này nếu muốn khớp với thoại.
```python
with self.voiceover(text="Nội dung thoại") as tracker:
    self.update_subtitle("Nội dung thoại") # BẮT BUỘC nằm ở dòng 1
    # Các lệnh self.play nằm ở đây...
```

## 2. QUY TẮC 80% (CHIA NHỎ THỜI GIAN)
- Cơ chế: `manim-voiceover` TỰ ĐỘNG CHỜ cho đến khi hết file âm thanh.
- Tính toán: Tổng các `run_time` trong một khối `voiceover` tuyệt đối không được vượt quá 80% (0.8) của `tracker.duration`. Khoảng 20% còn lại là "khoảng nghỉ thở" để thư viện tự động chờ.
```python
  with self.voiceover(text="Câu thoại có 3 ý nhỏ.") as tracker:
      self.update_subtitle("Câu thoại có 3 ý nhỏ.")
      self.play(Action_A, run_time=tracker.duration * 0.3)
      self.play(Action_B, run_time=tracker.duration * 0.3)
      self.play(Action_C, run_time=tracker.duration * 0.2)
      # Tổng = 0.8. CẤM CỘNG ĐỦ 1.0. Manim sẽ tự chờ 0.2 còn lại.
```
## 3. QUY TẮC MAX 2 GIÂY (CHỐNG RỀ RÀ)
Đối với các hiệu ứng xuất hiện (Write, FadeIn, Create): Nếu câu thoại quá dài (ví dụ mất 6s để đọc), việc nhân tỉ lệ có thể khiến hình ảnh hiện ra chậm như rùa.
- **BẮT BUỘC**: Sử dụng hàm `min()` để khóa giới hạn thời gian chạy của một animation xuất hiện là tối đa 1.5 đến 2 giây.
```python
  # Nếu câu thoại dài 6s, 40% là 2.4s. Hàm min sẽ khóa lại ở mức 1.5s cho nhanh gọn.
  self.play(Write(title), run_time=min(1.5, tracker.duration * 0.4))
```

## 4. CÁC LỆNH "CẤM" (ANTI-PATTERNS) GÂY LỖI ĐỨNG HÌNH
Nếu Terminal báo lỗi hoặc video bị đứng hình rất lâu sau mỗi câu nói, bạn đã vi phạm các điều CẤM sau:
- **CẤM 1**: Gọi `self.wait(tracker.duration)` bên trong khối voiceover.
- **CẤM 2**: Gọi `self.wait(tracker.get_remaining_duration())`. (Manim đã tự động tính toán, bạn gọi thêm sẽ gây ra Double-Waiting).
- **CẤM 3**: Dùng `tracker.last_wait_time` (Biến này đã bị xóa khỏi API).
- **CẤM 4**: Dùng `self.wait()` tùy tiện để khớp hình, hãy dùng tỉ lệ % của tracker.duration như ở Mục 2.

## 5. QUY TẮC CHỐNG KHOẢNG LẶNG ĐẦU VIDEO (INSTANT START)
Để video bắt đầu có tiếng ngay lập tức (không bị khựng 0.5s đầu):
- **BẮT BUỘC**: Animation đầu tiên của Scene (thường là hiện Tiêu đề) PHẢI nằm TRONG khối `with self.voiceover` đầu tiên.
- **CẤM**: Không được dùng bất kỳ lệnh `self.play()` hay `self.wait()` nào trước khối `with self.voiceover` đầu tiên (trừ việc khởi tạo đối tượng).
- **Mẹo xử lý**: Nếu vẫn còn khoảng lặng, Agent hãy thêm tham số `offset` hoặc cắt bớt thời gian chờ bằng cách:
  ```python
  # Cách viết CHUẨN để vào tiếng ngay:
  with self.voiceover(text="Chào mừng bạn...") as tracker:
      self.update_subtitle("Chào mừng bạn...")
      self.play(Write(title), run_time=min(1.2, tracker.duration))
  ```

## 6. QUY TẮC SUBTITLE CHIẾN LƯỢC (CHUNK-BASED)
- **CẤM**: Hiện toàn bộ câu thoại dài trong 1 lệnh `update_subtitle` duy nhất.
- **BẮT BUỘC (One-to-One Mapping)**: 
    - Phụ đề phải thay đổi theo nhịp Animation.
    - Với câu thoại dài, hãy sử dụng cấu trúc:
    ```python
    with self.voiceover(text="Câu thoại dài gồm ý 1 và ý 2.") as tracker:
        # Ý 1
        self.update_subtitle("Ý 1: ...")
        self.play(Action_1, run_time=tracker.duration * 0.4)
        
        # Ý 2
        self.update_subtitle("Ý 2: ...")
        self.play(Action_2, run_time=tracker.duration * 0.4)
    ```
- **Tư duy**: Mỗi khi bạn dùng lệnh `self.play(...)` cho một phần nội dung mới, BẮT BUỘC phải gọi `self.update_subtitle()` ngay phía trước. Phụ đề phải là "cái bóng" của hình ảnh.