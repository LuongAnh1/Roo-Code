# HƯỚNG DẪN BƯỚC 3: LẬP TRÌNH & KIỂM THỬ

**📚 TÀI LIỆU BẮT BUỘC ĐỌC TRƯỚC KHI CODE:**
Chỉ đọc 3 file này để lấy bộ khung và quy tắc gõ:
1. `scene-templates.md`: Copy đúng bộ khung (Blueprint) của Scene bạn đang làm.
2. `manim-standards.md`: Tuyệt đối tuân thủ quy tắc chống lệch chữ.
3. `voiceover-rules.md`: Áp dụng quy tắc "Bản vá 80%" để không bị lỗi chờ.

---

**QUY TRÌNH THỰC THI (5 BƯỚC):**

### 1. Dựng khung (Scaffolding)
- Dán bộ khung từ `scene-templates.md` vào file làm việc.
- Đảm bảo dòng 1 luôn có lệnh "Hack Path" (`sys.path.append(...)`) và `from skills.fami_lib import *`.

### 2. Triệu hồi Tool tùy chọn (Nếu cần)
Bạn có quyền import thêm 3 module kỹ năng sau từ thư mục `skills/`:
- `from skills.fami_math_graph import *`: Vẽ trục, đa giác, đồ thị.
- `from skills.fami_effects import *`: Hiệu ứng sinh động (`pop_in`, `typewriter`).
- `from skills.fami_assets_helper import *`: BẮT BUỘC dùng `load_svg_icon("assets/name.svg")` khi cần biểu tượng. **CẤM tự vẽ biểu tượng bằng code.** Nếu file `.svg` không tồn tại, hãy dừng lại và hỏi người dùng.
*(Mẹo: Hãy dùng công cụ `read_file` để xem docstrings của các file này nếu bạn không rõ tham số).*

### 3. Giao thức rà soát trước khi Render (Pre-flight Check)
Trước khi mở Terminal, tự kiểm tra code của bạn:
- [ ] Khối `voiceover` ĐÃ CÓ `self.update_subtitle` ở dòng 1 chưa?
- [ ] Các nhóm Mobject (`VGroup`) ĐÃ CÓ `.scale_to_fit_width(7.5)` để chống tràn chưa?
- [ ] Hiệu ứng gõ chữ (Typing) ĐÃ CÓ `.match_y()` để chống lệch chưa?

### 4. Auto-Debug Loop (Vòng lặp tự sửa lỗi)
- Chạy lệnh: `manim -pql ten_file.py TenClass`.
- **Nếu có lỗi (NameError, IndexError, v.v.):** 
   1. BẠN PHẢI TỰ ĐỘNG đọc Traceback.
   2. **Mở và đọc file `learning-examples.md`** để tìm cách giải quyết.
   3. Tự sửa code và CHẠY LẠI lệnh. KHÔNG ĐƯỢC hỏi người dùng ở bước này.
- **Tự Học:** Nếu fix thành công lỗi mới, cập nhật vào Mục 11 của `learning-examples.md`.

### 5. Nghiệm thu (Review)
Khi Terminal báo render thành công, hiển thị thông báo yêu cầu người dùng xem file mp4.
🔴 **DỪNG LẠI (STOP).** Chờ người dùng phản hồi mới làm Scene tiếp theo.