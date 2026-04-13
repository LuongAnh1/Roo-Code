# BƯỚC 1: TIẾP NHẬN & PHÂN TÍCH KỊCH BẢN

**NHIỆM VỤ:** Trích xuất nội dung từ `scripts/script.csv` (hoặc `.md`).

**PHÂN TÍCH CẤU TRÚC DỮ LIỆU (CỰC KỲ QUAN TRỌNG):**
Kịch bản là một bảng dữ liệu, hãy đọc theo cột:
- **Dòng tiêu đề (Header Row):** Đây là Dòng đầu tiên của file, chứa tên các phân cảnh (ví dụ: Hook, Main Body, Takeaways, CTA). **KHÔNG ĐƯỢC lấy dòng này làm tiêu đề video.**
- **Dòng nội dung:** Dữ liệu bắt đầu từ Dòng thứ 2 trở đi.
  - Các dòng lẻ (2, 4, 6...): Chứa **Lời thoại (Voiceover)** tương ứng của 4 cột.
  - Các dòng chẵn tiếp theo (3, 5, 7...): Chứa **Mô tả hình ảnh (Visuals)** tương ứng của 4 cột.

**QUY TRÌNH TRÍCH XUẤT:**
1. **Đọc file**: Dùng `read_file` để xem cấu trúc file kịch bản.
2. **Ánh xạ (Mapping)**: 
   - Với mỗi cột (Phân cảnh), hãy tạo một Object/Dict chứa: `{"voiceover": Dòng_Thoại, "visual": Dòng_Hình_Ảnh}`.
   - Bỏ qua Dòng đầu tiên (Header) khi tạo nội dung video.
3. **Kiểm định khả thi (Manim Feasibility)**:
   - Manim không vẽ được ảnh thực (người, cảnh vật phức tạp).
   - Nếu kịch bản yêu cầu vẽ ảnh thực, bạn BẮT BUỘC phải chuyển đổi thành: Hình khối (Shapes), Đồ thị (Graphs), Biểu tượng (Icons/SVG) hoặc Chữ (Text).
4. **Xác nhận**: Gửi báo cáo phân tích cho người dùng: 
   *"Tôi đã trích xuất xong 4 phân cảnh. Dưới đây là nội dung thoại và ý tưởng hình học cho từng cảnh."*
🔴 **DỪNG LẠI (STOP):** Chờ người dùng xác nhận bản phân tích trước khi sang Bước 2.