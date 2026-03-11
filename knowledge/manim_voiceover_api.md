# Manim Voiceover API Standard

## 1. Setup Service
```python
from manim_voiceover.services.gtts import GTTSService
self.set_speech_service(GTTSService(lang="vi"))
```

## 2. Workflow
```python
with self.voiceover(text="Câu thoại tiếng Việt") as tracker:
    # Animation bắt buộc dùng run_time đồng bộ
    self.play(Write(obj), run_time=tracker.duration)
```
## 3. Tracker Properties
- tracker.duration: Tổng thời gian của file âm thanh (giây).
- tracker.audio_path: Đường dẫn file mp3 đã tạo.

4. Agent Note
- Không tự chế biến số: last_wait_time, remaining_duration đều không tồn tại.
- Để tạo khoảng nghỉ sau câu nói: Dùng self.wait(0.5).
- Nếu có nhiều animation trong 1 câu thoại: Chia nhỏ run_time. Ví dụ: run_time=tracker.duration * 0.5.
