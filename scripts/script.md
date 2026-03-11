# VIDEO: GIẢI MÃ BỘ LỌC SPAM GMAIL
# Format: TikTok/Shorts (9:16)
# Chủ đề: Ứng dụng Định lý Bayes trong thực tế

---

## Scene 1: Cú Hook (0s - 5s)
- **Thoại**: "Làm sao Gmail biết đâu là thư rác, còn đâu là thư quan trọng? Bí mật nằm ở một công thức toán học từ thế kỷ 18."
- **Visual**: 
    - Hiện tiêu đề chính: "BÍ MẬT CỦA GMAIL" (Màu Yellow_C, Font 50, Vị trí: Top).
    - Giữa màn hình: Một Icon Email (Blue_B).
    - Hiệu ứng: Các lá thư bay vào phễu lọc, chia ra hai hướng: "SPAM" (Đỏ) và "INBOX" (Xanh).
- **Action**: Dùng `LaggedStart` cho các lá thư bay liên tục.

## Scene 2: Giới thiệu Định lý Bayes (5s - 15s)
- **Thoại**: "Đó là định lý Bayes. Thay vì đoán mò, nó tính toán xác suất dựa trên dữ liệu có sẵn."
- **Visual**: 
    - Công thức Bayes: `P(A|B) = [P(B|A) * P(A)] / P(B)` hiện ra giữa màn hình (MathTex).
    - Đóng khung công thức bằng `SurroundingRectangle` (Màu Cyan).
    - Giải thích nhanh bằng text nhỏ dưới công thức: "Xác suất là thư rác khi có từ khóa lạ".
- **Action**: Công thức hiện ra bằng hiệu ứng `Write`.

## Scene 3: Ví dụ thực tế - Từ khóa "FREE" (15s - 25s)
- **Thoại**: "Giả sử một Email có chứa từ 'miễn phí'. Thuật toán sẽ học rằng: Hầu hết các thư có từ này đều là thư rác."
- **Visual**: 
    - Hiện từ khóa lớn: "FREE" (Màu đỏ neon).
    - Hiển thị một thanh phần trăm (Bar chart đơn giản) đang tăng lên mức 90% kèm nhãn "Khả năng là Spam".
- **Action**: Thanh phần trăm chạy từ 0 đến 90% khớp với lời thoại.

## Scene 4: Hạn chế và Sự tinh vi (25s - 35s)
- **Thoại**: "Nhưng kẻ spam rất tinh vi. Chúng không viết là 'free', mà viết thành 'fr33', 'f.r.e.e', hay 'fr€€' để đánh lừa hệ thống."
- **Visual**: 
    - Từ "FREE" biến đổi liên tục (Morphing) thành các biến thể: "fr33" -> "f.r.e.e" -> "fr€€".
    - Hiện dấu hỏi chấm lớn màu vàng bên cạnh các biến thể này.
- **Action**: Dùng `ReplacementTransform` để chuyển đổi giữa các từ.

## Scene 5: Câu hỏi tương tác (35s - End)
- **Thoại**: "Theo bạn, làm thế nào để toán học xử lý được những kẻ cố tình viết sai chính tả như thế này? Hãy comment câu trả lời của bạn phía dưới nhé!"
- **Visual**: 
    - Câu hỏi chính: "XỬ LÝ 'fr33' NHƯ THẾ NÀO?" (Vị trí: Center).
    - Hiệu ứng: Chữ "Comment" nhấp nháy ở phía dưới.
    - Một icon dấu hỏi chấm lớn xoay nhẹ.
- **Action**: FadeOut toàn bộ scene cũ, chỉ để lại câu hỏi và lời kêu gọi hành động (CTA).