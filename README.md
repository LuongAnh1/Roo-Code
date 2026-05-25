# AI MANIM VIDEO PRODUCER

## Mục lục

1. [Tổng quan dự án](#1-tổng-quan-dự-án)
2. [Cách cài đặt, setup](#2-cách-cài-đặt-setup)
3. [Sơ đồ làm việc của Agent](#3-sơ-đồ-làm-việc-của-agent)
4. [Hướng dẫn sử dụng Roo Code](#4-hướng-dẫn-sử-dụng-roo-code)
5. [Vai trò của Người dùng](#5-vai-trò-của-người-dùng)

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

### Cấu trúc dự án: [project_structure.txt](project_structure.txt)
Sơ lược
- `scripts/`: Code Python cho từng scene
- `assets/`: Tài nguyên hình ảnh và icon
- `media/`: Output video (không sync với Git)

---

## 2. Cách cài đặt, setup

### Yêu cầu hệ thống:
- **Python 3.9** trở lên
- **Git** (để clone repository)
- **LaTeX** (MiKTeX hoặc TeX Live) - **BẮT BUỘC** để Manim render công thức toán
- **FFmpeg** - **BẮT BUỘC** để xử lý video
- **Windows/macOS/Linux** (hỗ trợ đầy đủ)

### Hướng dẫn nhanh:

#### **Bước 0: Cài đặt LaTeX và FFmpeg (BẮT BUỘC)**

**Windows:**
- **LaTeX (MiKTeX):** 
  1. Tải từ https://miktex.org/download
  2. Chạy installer và chọn "Install MiKTeX for all users" (hoặc chỉ người dùng hiện tại)
  3. Đặt đường dẫn cài vào thư mục có quyền ghi (ví dụ: `C:\MiKTeX`)
  4. Hoàn tất cài đặt

- **FFmpeg:**
  1. Tải từ https://ffmpeg.org/download.html hoặc https://www.gyan.dev/ffmpeg/builds/
  2. Tải bản "full" hoặc "essentials"
  3. Giải nén vào thư mục (ví dụ: `C:\ffmpeg`)
  4. Thêm vào **PATH**:
     - Mở **Environment Variables** (Tìm kiếm: "Environment Variables" trong Start Menu)
     - Thêm `C:\ffmpeg\bin` vào **PATH** trong **System Variables**
     - Khởi động lại Terminal/PowerShell
  5. Kiểm tra: `ffmpeg -version` (nếu hiện version là OK)

**macOS:**
```bash
# Cài LaTeX (TeX Live)
brew install --cask mactex

# Cài FFmpeg
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
# Cài LaTeX
sudo apt-get install texlive-full

# Cài FFmpeg
sudo apt-get install ffmpeg
```

#### **Bước 1: Clone repository:**
```bash
git clone https://github.com/LuongAnh1/Roo-Code.git
cd Roo-Code
```

#### **Bước 2: Tạo môi trường ảo:**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux
```

#### **Bước 3: Cài đặt Python dependencies:**
```bash
pip install -r requirements.txt
```

#### **Bước 4: Kiểm tra cài đặt:**
```bash
# Kiểm tra Python packages
python -c "import manim; print('Manim OK')"

# Kiểm tra FFmpeg (Windows)
ffmpeg -version

# Kiểm tra LaTeX (tùy chọn)
pdflatex --version  # Windows/macOS/Linux
```

Nếu tất cả các lệnh trên chạy thành công mà không lỗi, bạn đã sẵn sàng!

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

---

## 4. Hướng dẫn sử dụng Roo Code

Roo Code là một AI Coding Agent (trợ lý lập trình trí tuệ nhân tạo dạng tác nhân) được cài đặt dưới dạng một Extension (tiện ích mở rộng) trên VS Code hoặc các IDE mã nguồn mở.

Roo Code hỗ trợ người dùng tạo các Modes tùy thuộc vào đặc trưng công việc thông qua các API được cung cấp bởi các nhà phân phối mà người dùng mua.

Dưới đây chỉ là các bước cơ bản để tạo Mode để Roo Code có thể thực hiện dự án này.

**Lưu ý (Cho việc không dùng Roo Code):** 
- Nếu không sử dụng Roo Code bạn có thể bảo Agent của bạn đọc file `.roo/rules-manim-video-producer/work-flow.md` đầu tiên để Agent thực hiện công việc.
- Về định nghĩa vai trò cho Agent bạn có thể tham khảo Bước 2 ý 4 trong mục này.

### Bước 1: Cấu hình nhà cung cấp API

1. Mở **Settings** trong VS Code hoặc IDE của bạn
2. Truy cập vào phần **Providers** (Nhà cung cấp)
3. Chọn hoặc tạo một **Configuration Profile** (ví dụ: `vertex-gemini-flash`)
4. Lựa chọn **API Provider**: Ví dụ **GCP Vertex AI**, **OpenAI**, **Anthropic**, hoặc các nhà cung cấp khác. Sau đó nhập các thông tin kèm theo tùy vào nhà cung cấp yêu cầu (Ví dụ: **API Key**, **Google Clound Project ID**...) và chọn model muốn dùng (Model mà bạn đã mua từ nahf cung cấp) 

### Bước 2: Tạo Mode với Role Definition

Sau khi cấu hình API, tạo một **Mode** mới để định nghĩa tính cách và chuyên môn của Roo:

1. Vào phần **Modes** (Các chế độ) trong Settings
2. Bấm **Create** để thêm mode mới, đặt tên là `"Manim Video Producer"` 
**Chú ý: nếu đặt tên mode khác thì bạn phải sửa lại tên folder `.roo/rules-manim-video-producer` đúng như chú thích trong mục Mode-specific Custom Instructions (optional)**
3. Chọn **API Configuration** đã tạo ở bước 1
4. Trong phần **Role Definition**, dán nội dung sau:

```
Bạn là một Chuyên gia thiết kế chuyển động (Senior Motion Designer) và Nhà giáo dục toán học xuất sắc. Nhiệm vụ của bạn là biến những khái niệm toán học phức tạp thành các video ngắn (TikTok/Shorts) cực kỳ bắt mắt, dễ hiểu và chuyên nghiệp.

### Chuyên môn của bạn:
1. **Bậc thầy Manim**: Bạn am hiểu sâu sắc thư viện Manim, đặc biệt là cách sử dụng `VGroup`, `ReplacementTransform` và các hiệu ứng `LaggedStart` để tạo ra chuyển động mượt mà.
2. **Kỹ sư âm thanh (Audio-Visual Sync)**: Bạn là chuyên gia sử dụng `manim-voiceover`, luôn đảm bảo hình ảnh xuất hiện đúng mili giây khi giọng đọc nhắc tới.
3. **Tư duy Mobile-First**: Bạn luôn tối ưu bố cục cho màn hình dọc (9:16), sử dụng cỡ chữ lớn, màu sắc rực rỡ và bố cục cân đối để xem tốt trên điện thoại.
4. **Sáng tạo nội dung**: Bạn không chỉ viết code, bạn còn đề xuất các cách trình bày hình ảnh (Visual Metaphor) để làm cho kiến thức trở nên sinh động hơn.

### Tính cách và Cách làm việc:
- **Tỉ mỉ & Thẩm mỹ**: Bạn cực kỳ khắt khe về màu sắc và khoảng cách (alignment). Bạn luôn tuân thủ nghiêm ngặt các bộ Rule trong thư mục `.roo/`.
- **Chủ động**: Trước khi viết code, bạn luôn tóm tắt kế hoạch bố cục (Layout Plan).
- **Kiên nhẫn**: Nếu render lỗi, bạn sẽ tự phân tích log và sửa lỗi cho đến khi hoàn hảo.

Mục tiêu cuối cùng của bạn là tạo ra những video "đẹp như mơ", có chất lượng tương đương với những kênh giáo dục hàng đầu thế giới trên YouTube và TikTok.
```

5. Bấm **Create Mode** để lưu Mode
6. Vẫn trong **Setting/Modes** lướt xuống tìm đến **Mode-specific Custom Instructions (optional)** và điền
```text
bạn hãy luôn đọc file work-flow.md đầu tiên.
```
**Lưu ý:** đây cũng là vị trí bạn thấy đường dẫn tên folder nơi Roo Code sẽ đọc các file rule trong đó. Nếu bạn sử dụng tên Modes khác so với hướng dẫn, hãy sửa lại tên folder chứa các file rule (.md) theo như đường dẫn thấy trong này
**Chú ý:** Sau khi thay đổi Modes bạn nhớ bấm Save để lưu, và trong khung chat nhớ chọn Mode mà bạn vừa tạo

### Bước 3: Bắt đầu sử dụng

Sau khi hoàn tất các bước trên, bạn đã sẵn sàng để:
- **Tải tệp kịch bản**: Chuẩn bị file CSV ở trong scripts với các scene, lời thoại và mô tả hình ảnh
- **Yêu cầu Agent**: Gõ lệnh hoặc yêu cầu để Agent bắt đầu sản xuất video
- **Tham gia quá trình**: Duyệt ý tưởng, xem video nháp, và điều chỉnh nếu cần

Xem phần **Vai trò của Người dùng** bên dưới để hiểu rõ hơn về quy trình tương tác trong quá trình sản xuất.

---

# 5. Vai trò của Người dùng 

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
