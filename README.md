# AI MANIM VIDEO PRODUCER

## Mục lục

1. [Tổng quan dự án](#1-tổng-quan-dự-án)
2. [Cách cài đặt, setup](#2-cách-cài-đặt-setup)
3. [Sơ đồ làm việc của Agent](#3-sơ-đồ-làm-việc-của-agent)
4. [Vai trò của Người dùng](#4-vai-trò-của-người-dùng)

---

## 1. Tổng quan dự án 

**AI Manim Video Producer** là một hệ thống tự động hóa việc tạo video animation giáo dục từ kịch bản văn bản. Dự án sử dụng công nghệ Manim (Mathematical Animation Engine) kết hợp với trí tuệ nhân tạo để chuyển đổi script CSV thành video chất lượng cao với giọng nói tự nhiên.

### Mục đích:
- Tự động hóa quy trình sản xuất video animation
- Giảm thời gian từ ý tưởng đến sản phẩm cuối
- Tạo video giáo dục chất lượng chuyên nghiệp với chi phí thấp

### Công nghệ chính:
- **Manim 0.18.0**: Engine animation toán học
- **Manim-Voiceover**: Tích hợp giọng nói tự nhiên (gTTS)
- **Python 3.9+**: Ngôn ngữ lập trình chính
- **AI Agent**: Xử lý tự động với human-in-the-loop

### Cấu trúc dự án:
- `scripts/`: Code Python cho từng scene
- `assets/`: Tài nguyên hình ảnh và icon
- `media/`: Output video (không sync với Git)
- `knowledge/`: Tài liệu hướng dẫn

### Chi tiết đầy đủ:
Xem file [SETUP.md](SETUP.md) để có hướng dẫn chi tiết về cài đặt môi trường ảo, troubleshooting và các mẹo sử dụng.
---

## 2. Cách cài đặt, setup

### Yêu cầu hệ thống:
- **Python 3.9** trở lên
- **Git** (để clone repository)
- **Windows/macOS/Linux** (hỗ trợ đầy đủ)

### Hướng dẫn nhanh:

1. **Clone repository:**
   ```bash
   git clone https://github.com/LuongAnh1/Roo-Code.git
   cd Roo-Code
   ```

2. **Tạo môi trường ảo:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # macOS/Linux
   ```

3. **Cài đặt dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Kiểm tra cài đặt:**
   ```bash
   python -c "import manim; print('OK')"
   ```

### Chi tiết đầy đủ:
Xem file [SETUP.md](SETUP.md) để có hướng dẫn chi tiết về cài đặt môi trường ảo, troubleshooting và các mẹo sử dụng.

---

## 3. Sơ đồ làm việc của Agent  

```text
=======================================================================
           SƠ ĐỒ LUỒNG LÀM VIỆC: AI MANIM VIDEO PRODUCER
=======================================================================

   [ BAT DAU DU AN ]
            │
            ▼
 ┌──────────────────────────────────────┐<──────────────┐
 │ BUOC 1: TIEP NHAN DU LIEU            │               │
 │ Doc kich ban script.csv              │               │
 │ Trich xuat Thoai & Hinh anh          │               │
 └──────────────────┬───────────────────┘               │
                    │                                   │
           { BAN DUYET KICH BAN } ────────(Sai)──────┘
                    │
                 (Dong y)
                    │
   ╭────────────────▼───────────────────────────╮
   │ BAT DAU VONG LAP: LAM TU NG SCENE (1->4)   │<──────┐
   ╰────────────────┬───────────────────────────╯       │
                    │                                   │
 ┌──────────────────▼───────────────────┐<────────┐     │
 │ BUOC 2: PHAC THAO NGHE THUAT         │         │     │
 │ De xuat y tuong (Visual Metaphor)    │         │     │
 │ Xac dinh Layout (Y-coordinates)      │         │     │
 └──────────────────┬───────────────────┘         │     │
                    │                             │     │
           { BAN DUYET Y TUONG } ──────(Doi y)─┘     │
                    │                                   │
                 (Dong y)                               │
                    │                                   │
 ┌──────────────────▼───────────────────┐<────────┐     │
 │ BUOC 3: LAP TRINH & KIEM THU         │         │     │
 │ Viet Code (Dung fami_lib)            │         │     │
 │ Chay Terminal: manim -pql            │         │     │
 └──────────────────┬───────────────────┘         │     │
                    │                             │     │
             [ Loi Terminal? ]                    │     │
                    ├──────────(CO LOI)─────┐     │     │
                    │                       │     │     │
               (Thanh cong)       [ TU DOC LOG ]     │
                    │             [ & TU SUA CODE ]     │
                    ▼                       │     │     │
          [ XUAT VIDEO NHAP ] <──────────┘     │     │
                    │                             │     │
           { BAN DUYET VIDEO } ─────(Sua code)─┘     │
                    │                                   │
               (Chot Scene)                             │
                    │                                   │
   ╭────────────────▼───────────────────╮               │
   │      Da xong ca 4 Scene chua?      │               │
   ╰────────┬───────────────────┬───────╯               │
            │                   │                       │
          (Chua)              (Xong)                    │
            │                   │                       │
            └───────────────────┼───────────────────────┘
                                │
            ┌───────────────────┘
            ▼
 ┌──────────────────────────────────────┐
 │ BUOC 4: XUAT BAN HOAN THIEN          │
 │ Chay 4 lenh render net cang          │
 │    (-pqh 1080x1920)                  │
 └──────────────────┬───────────────────┘
                    │
                    ▼
         [ HOAN THANH DU AN ]
```

# 4. Vai trò của Người dùng 

## Chốt chặn 1: Duyệt Kịch bản 
- **Agent làm gì**: Đọc file CSV, ghép Lời thoại với Mô tả hình ảnh.
- **Bạn làm gì**: Kiểm tra xem Agent có lấy nhầm dòng tiêu đề làm kịch bản không. Bấm OK để Agent bắt đầu nghĩ ý tưởng cho Phân cảnh 1.

## Chốt chặn 2: Duyệt Ý tưởng 
- **Agent làm gì**: Trình bày ý tưởng thay thế Text bằng Hình ảnh/Đồ thị, báo cáo các Icon lấy từ thư mục assets/.
- **Bạn làm gì**: Nếu bạn thấy ý tưởng hay, gõ OK, code đi. Nếu bạn muốn đổi, gõ ví dụ: "Đừng vẽ hình tròn, hãy vẽ một cái bập bênh". Agent sẽ sửa kế hoạch trước khi code.

## Chốt chặn 3: Nghiệm thu Video Nháp
- **Agent làm gì**: Nó sẽ tự động đánh vật với Terminal. Nếu có lỗi Code, nó tự đọc log và tự sửa. Nó CHỈ GỌI BẠN khi video nháp chất lượng thấp (-pql) đã được render thành công.
- **Bạn làm gì**: Mở file video nháp lên xem.
    Nếu chữ bị lệch, gõ: "Chữ bị lệch, đẩy lên trên 1 chút".
    Nếu thời gian bị chậm, gõ: "Hiệu ứng hiện ra nhanh hơn chút".
    Nếu hoàn hảo, gõ: "Chốt. Chuyển sang làm Scene tiếp theo".
*(Quá trình này lặp lại 4 lần cho 4 phân cảnh. Sau khi bạn chốt Scene 4, Agent sẽ tự động ghép và xuất bản video nét căng ở Bước 4).*