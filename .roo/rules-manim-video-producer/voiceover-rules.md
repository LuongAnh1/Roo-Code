# QUY TẮC ĐỒNG BỘ GIỌNG NÓI & PHỤ ĐỀ (SUBTITLES)

## 1. Cấu hình & Kế thừa
- **KHÔNG ĐƯỢC** gọi `self.set_speech_service` trong hàm `construct()`. Logic này đã được xử lý tự động trong `FaMIBaseScene`.
- **SUBTITLE**: Mọi block `voiceover` **PHẢI** đi kèm lệnh `self.update_subtitle("Nội dung phụ đề")` ngay dòng đầu tiên trong khối `with`.

## 2. Quy Tắc Timing (Đồng bộ tỉ lệ %)
- **CẤM** dùng `self.wait()` để khớp thời gian nếu không cần thiết. `manim-voiceover` tự động chờ đến hết âm thanh.
- **CHIA NHỎ THỜI GIAN**: Thay vì dùng `run_time=tracker.duration` cho cả câu, hãy chia nhỏ theo ý nghĩa của câu thoại:
  ```python
  with self.voiceover(text="Câu thoại chia làm 3 ý.") as tracker:
      self.update_subtitle("Câu thoại chia làm 3 ý.")
      self.play(Action_A, run_time=tracker.duration * 0.3)
      self.play(Action_B, run_time=tracker.duration * 0.4)
      self.play(Action_C, run_time=tracker.duration * 0.3)
  ```
- **QUY TẮC 2 GIÂY**: Các Animation xuất hiện (Write, FadeIn, Create) không được vượt quá 2 giây. Nếu câu thoại dài, chỉ cho Animation chạy nhanh (1-1.5s), sau đó Manim sẽ tự đợi phần thời gian còn lại.

## 3. Các lỗi cần tránh (Anti-Patterns)
- **CẤM**: `self.wait(tracker.duration)` hoặc `self.wait(tracker.get_remaining_duration())` sau khi đã gọi `self.play` với tổng `run_time` bằng `tracker.duration`. Điều này gây ra lỗi "đứng hình" (double waiting).
- **CẤM**: Dùng `tracker.last_wait_time` (Biến đã bị xóa).
- **CẤM**: Đặt `self.play` bên ngoài khối with `self.voiceover(...)` nếu muốn Animation khớp với lời thoại.

## 4. Kiểm soát nhịp độ (Pacing) cho TikTok
- TikTok yêu cầu nhịp độ nhanh. Tổng thời gian các Animation trong 1 câu không nên chiếm quá 80% thời lượng thoại.
- Luôn để lại khoảng 10-20% thời gian cuối câu làm "khoảng nghỉ" (nếu không dùng lệnh wait, Manim sẽ tự xử lý, nhưng đảm bảo các Animation kết thúc sớm hơn âm thanh một chút để video không bị cụt).