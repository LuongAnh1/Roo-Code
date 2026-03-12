# HƯỚNG DẪN BƯỚC 3: LẬP TRÌNH & KIỂM THỬ

**BẮT BUỘC ĐỌC TRƯỚC KHI CODE:**
1. `reference_template.py`: Để copy bộ khung chuẩn.
2. `manim-standards.md`: Tuyệt đối tuân thủ quy tắc gõ chữ và MarkupText.
3. `voiceover-rules.md`: Để chia tỉ lệ thời gian chuẩn xác.
4. `learning-examples.md`: Để không mắc lại lỗi cũ.

**QUY TRÌNH THỰC THI:**
1. **Import:** Code luôn bắt đầu bằng: `from skills.fami_lib import *`. Kế thừa `FaMIBaseScene`.
2. **API Verification:** Nếu định dùng một hàm lạ, hãy dùng công cụ Terminal chạy `python -c "import manim; help(manim.Tên_Hàm)"` để kiểm tra trước.
3. **Auto-Debug Loop (Tự sửa lỗi):**
   - Chạy lệnh: `manim -pql ten_file.py TenClass`.
   - Nếu Terminal báo lỗi (NameError, IndexError...): BẠN PHẢI TỰ ĐỘNG đọc Traceback, tự sửa code và CHẠY LẠI lệnh. Không được hỏi người dùng ở bước này.
   - **Tự Học:** Nếu Fix thành công một lỗi mới, tự động mở `learning-examples.md` và ghi chú vào Mục 10.
4. **Nghiệm thu:** Khi Terminal báo render thành công, hiển thị thông báo yêu cầu người dùng xem file mp4 và nhận xét. 🔴 **DỪNG LẠI.**

# BƯỚC 3: LẬP TRÌNH & KIỂM THỬ

**GIAO THỨC TRƯỚC KHI RENDER (Layout-Checklist):**
1. **Kiểm tra Import**: Đã có `from skills.fami_lib import *` chưa?
2. **Kiểm tra Subtitle**: Khối `voiceover` đã có `update_subtitle` chưa?
3. **Kiểm tra Tràn viền**: Đã gọi `.scale_to_fit_width(7.5)` cho các nhóm nội dung (VGroup) chưa?
4. **Kiểm tra Tọa độ**: Đã dùng `POS_TITLE`, `POS_CENTER` chưa? 

**TỰ ĐỘNG DEBUG:**
Nếu sau khi render mà chữ bị lệch hoặc tràn, BẮT BUỘC:
- Dùng `print(obj.width)` trong code để xem kích thước thực của đối tượng.
- Dùng `.match_y()` hoặc `.move_to()` để căn chỉnh lại dựa trên trục Y chuẩn của `fami_lib`.