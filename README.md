# 🗺️ SƠ ĐỒ LUỒNG LÀM VIỆC: AI MANIM VIDEO PRODUCER

## 📊 Sơ đồ Khối (Workflow Diagram)

```mermaid
flowchart TD
    %% Định nghĩa màu sắc
    classDef step1 fill:#1e3a8a,stroke:#4fb0ff,stroke-width:2px,color:#fff;
    classDef step2 fill:#b45309,stroke:#ffd000,stroke-width:2px,color:#fff;
    classDef step3 fill:#14532d,stroke:#00ff00,stroke-width:2px,color:#fff;
    classDef step4 fill:#7f1d1d,stroke:#ff4d4d,stroke-width:2px,color:#fff;
    classDef human fill:#4b5563,stroke:#fff,stroke-width:2px,color:#fff,stroke-dasharray: 5 5;
    classDef loop fill:#4c1d95,stroke:#c084fc,stroke-width:2px,color:#fff;

    Start([🚀 Bắt đầu Dự án]) --> B1

    subgraph BƯỚC 1: TIẾP NHẬN DỮ LIỆU
        B1[Đọc kịch bản script.csv]:::step1 --> B1_1[Trích xuất 4 Phân cảnh: Thoại & Hình]:::step1
        B1_1 --> H1{🧍 NGƯỜI DÙNG DUYỆT:\nCó đúng kịch bản chưa?}:::human
    end

    H1 -- "Đồng ý" --> LoopStart((🔄 BẮT ĐẦU VÒNG LẶP\nLàm từng Scene 1 -> 4)):::loop
    H1 -- "Sửa lại" --> B1

    subgraph BƯỚC 2: PHÁC THẢO NGHỆ THUẬT
        LoopStart --> B2[Đọc step2-planning.md]:::step2
        B2 --> B2_1[Tìm Icon trong /assets\nLên bố cục Visual Metaphors]:::step2
        B2_1 --> H2{🧍 NGƯỜI DÙNG DUYỆT:\nKế hoạch hình ảnh OK chưa?}:::human
    end

    subgraph BƯỚC 3: CODE & TỰ ĐỘNG SỬA LỖI
        H2 -- "Đồng ý" --> B3[Đọc step3-coding.md]:::step3
        H2 -- "Sửa lại" --> B2_1
        
        B3 --> B3_1[Viết Code Python/Manim]:::step3
        B3_1 --> B3_2[Chạy Terminal: manim -pql]:::step3
        B3_2 --> CheckError{Terminal\nbáo lỗi?}
        
        CheckError -- "CÓ LỖI" --> B3_Fix[Agent TỰ ĐỌC Traceback\n& TỰ SỬA CODE]:::step3
        B3_Fix --> B3_2
        
        CheckError -- "THÀNH CÔNG" --> H3{🧍 NGƯỜI DÙNG DUYỆT:\nXem file video mp4 nháp}:::human
    end

    H3 -- "Cần sửa (Màu/Chữ/Tốc độ)" --> B3_1
    H3 -- "Đồng ý (Chốt Scene)" --> CheckLoop{Đã xong\ncả 4 Scene?}

    CheckLoop -- "Chưa xong" --> LoopStart
    CheckLoop -- "Đã xong 4 Scene" --> B4

    subgraph BƯỚC 4: XUẤT BẢN
        B4[Chạy 4 lệnh render chất lượng cao\n-pqh 1080x1920]:::step4 --> Finish([🎉 HOÀN THÀNH DỰ ÁN])
    end
```

# 👨‍💻 Vai trò của Người dùng (Human-in-the-loop)

Hệ thống được thiết kế để tự động hóa 90% công việc lập trình. 10% còn lại là quyết định của bạn. Bạn chỉ cần lên tiếng tại 3 điểm chốt chặn (Nút nét đứt trên sơ đồ):

## 📍 Chốt chặn 1 (Sau Bước 1)**: Duyệt Kịch bản
- **Agent làm gì**: Đọc file CSV, ghép Lời thoại với Mô tả hình ảnh.
- **Bạn làm gì**: Kiểm tra xem Agent có lấy nhầm dòng tiêu đề làm kịch bản không. Bấm OK để Agent bắt đầu nghĩ ý tưởng cho Phân cảnh 1.

## 📍 Chốt chặn 2 (Sau Bước 2): Duyệt Ý tưởng (Storyboard)
- **Agent làm gì**: Trình bày ý tưởng thay thế Text bằng Hình ảnh/Đồ thị, báo cáo các Icon lấy từ thư mục assets/.
- **Bạn làm gì**: Nếu bạn thấy ý tưởng hay, gõ OK, code đi. Nếu bạn muốn đổi, gõ ví dụ: "Đừng vẽ hình tròn, hãy vẽ một cái bập bênh". Agent sẽ sửa kế hoạch trước khi code.

## 📍 Chốt chặn 3 (Sau Bước 3): Nghiệm thu Video Nháp
- **Agent làm gì**: Nó sẽ tự động đánh vật với Terminal. Nếu có lỗi Code, nó tự đọc log và tự sửa. Nó CHỈ GỌI BẠN khi video nháp chất lượng thấp (-pql) đã được render thành công.
- **Bạn làm gì**: Mở file video nháp lên xem.
    Nếu chữ bị lệch, gõ: "Chữ bị lệch, đẩy lên trên 1 chút".
    Nếu thời gian bị chậm, gõ: "Hiệu ứng hiện ra nhanh hơn chút".
    Nếu hoàn hảo, gõ: "Chốt. Chuyển sang làm Scene tiếp theo".
*(Quá trình này lặp lại 4 lần cho 4 phân cảnh. Sau khi bạn chốt Scene 4, Agent sẽ tự động ghép và xuất bản video nét căng ở Bước 4).*