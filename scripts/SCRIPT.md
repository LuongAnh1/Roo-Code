**TIÊU ĐỀ VIDEO:** Bức ảnh trong máy tính thực chất là gì?

**(PHẦN 1: SỰ RA ĐỜI CỦA PIXEL)**

Có lẽ bạn đã biết các bức ảnh kỹ thuật số, thực ra là các pixel, nhưng bạn có thực sự hiểu các pixel là gì? Tại sao lại có thể chuyển từ hình ảnh từ thế giới thực trở thành các bức ảnh nằm trong máy tính? Các file JPG, PNG thực ra là gì?

Trong video này, tôi sẽ giải thích cho các bạn về các khái niệm này!

Đầu tiên, ta cùng tìm hiểu định nghĩa cơ bản nhất của một hình ảnh kỹ thuật số.

Một hình ảnh ở không gian vật lý có thể được định nghĩa là một hàm số $f(x,y)$ trong đó $x$ và $y$ là các tọa độ không gian liên tục trong thế giới thực, giá trị của hàm số tại $x,y$ được gọi là cường độ ánh sáng hay mức xám (ở đây ta chưa nhắc đến về màu sắc).

Và ta đều biết, máy tính chỉ có thể lưu trữ các tập hợp hữu hạn. Do nguyên nhân đó, ta xấp xỉ không gian $(x,y)$ và hàm số $f(x,y)$ bằng các đại lượng rời rạc, cách đều nhau và hữu hạn. Hàm số không gian liên tục - Hình ảnh vật lý này từ đó chuyển đổi thành Hàm số rời rạc - một hình ảnh kỹ thuật số.

Và magic bắt đầu ở đây, quá trình chuyển đổi từ "liên tục" sang "rời rạc" này được thực hiện thông qua hai bước cốt lõi:

**1. Lấy mẫu - Sự ra đời của Pixel:**
Hãy tưởng tượng bạn đặt một tấm lưới lên trên bức ảnh vật lý thực tế. Mỗi ô vuông nhỏ trên tấm lưới đó sẽ đại diện cho một tọa độ không gian rời rạc. Ta gọi mỗi ô vuông này là một Pixel (Picture Element).

**2. Lượng tử hóa:**
Ta thực hiện gán một số nguyên đại diện cho cường độ tại pixel đó (thông thường nằm trong khoảng 0 - 255).

Vậy là một bức ảnh đen trắng trong máy tính, thực chất chỉ là một ma trận 2 chiều chứa các con số 0 đến 255. Và nếu bạn tăng số ô chia lưới lên, lưới càng được chia nhỏ, số lượng pixel càng nhiều, thì bức ảnh kỹ thuật số càng chi tiết và xấp xỉ càng sát với hình ảnh trong thế giới thực. Đó chính là lý do ta gọi số lượng ô chiều ngang và chiều dọc là độ phân giải.

**(PHẦN 2: THÊM MÀU SẮC VÀ BÀI TOÁN DỮ LIỆU)**

Tiếp theo, ta sẽ cùng đi phủ màu cho hình ảnh này.

Về mặt toán học, thay vì một ma trận 2 chiều đơn lẻ, một bức ảnh màu là một cấu trúc dữ liệu ba chiều (một Tensor). Nó bao gồm 3 ma trận xếp chồng lên nhau tương ứng với dải cường độ ánh sáng của ba kênh màu: Đỏ (Red), Xanh lục (Green) và Xanh lam (Blue) – hay còn gọi là không gian màu **RGB**. Sự phối hợp cường độ của 3 kênh này tại cùng một tọa độ $(x,y)$ sẽ đánh lừa tế bào hình nón trong mắt bạn, tạo ra cảm giác về hàng triệu màu sắc khác nhau.

Tuy nhiên, quy mô dữ liệu ngày càng phình to đã đặt ra một nghịch lý. Nếu giữ nguyên một bức ảnh độ phân giải 2880 x 1800 (tức là chỉ đủ chi tiết để hiển thị trên một màn hình laptop) ở dạng ma trận RGB nguyên bản, nó đã có kích thước xấp xỉ 47MB, tức là một video 60fps dài một giây với độ phân giải này sẽ nặng gần 3GB. Thật khủng khiếp đúng không nào!

Đó là lý do các tiêu chuẩn biểu diễn và nén ảnh như **JPG** và **PNG** ra đời. Chúng không chỉ là "phần đuôi" của tên file, mà đại diện cho hai trường phái toán học hoàn toàn trái ngược nhau!

**(PHẦN 3: JPG - BẬC THẦY ĐÁNH LỪA THỊ GIÁC VÀ NÉN TỔN HAO)**

Đầu tiên là **JPG** – đại diện cho cơ chế nén tổn hao (lossy compression). Thuật toán này được thiết kế dựa trên một lỗ hổng sinh lý của mắt người: Võng mạc của chúng ta cực kỳ nhạy cảm với "độ sáng", nhưng lại khá kém trong việc nhận diện các chi tiết "màu sắc" nhỏ bé.

Tận dụng điều này, JPG bóc tách không gian RGB sang không gian màu **YCbCr** bằng hệ phương trình ma trận tuyến tính:

$$Y = 0.257 \cdot R + 0.504 \cdot G + 0.098 \cdot B + 16$$

$$Cb = -0.148 \cdot R - 0.291 \cdot G + 0.439 \cdot B + 128$$

$$Cr = 0.439 \cdot R - 0.368 \cdot G - 0.071 \cdot B + 128$$

Trong đó, lớp cường độ sáng ($Y$) được giữ lại gần như nguyên vẹn, còn dữ liệu ở hai lớp sắc độ ($Cb$ và $Cr$) bị hệ thống thẳng tay loại bỏ đi một nửa. Mắt bạn nhìn lướt qua sẽ không hề hay biết!

Nhưng cốt lõi sức mạnh của JPG nằm ở một phương trình vi phân kinh điển: **Biến đổi Cosine Rời rạc (2D-DCT)**. Bức ảnh sẽ được băm thành các khối ma trận nhỏ $8 \times 8$. Phương trình 2D-DCT sẽ chuyển đổi tín hiệu từ miền không gian sang miền phổ tần số $F(u,v)$:

$$F(u,v) = \alpha(u)\alpha(v) \sum_{x=0}^{M-1} \sum_{y=0}^{N-1} f(x,y) \cos\left[\frac{(2x+1)u\pi}{2M}\right] \cos\left[\frac{(2y+1)v\pi}{2N}\right]$$

Toán tử này tạo ra một hiện tượng tuyệt mỹ gọi là **"Hội tụ năng lượng"**. Nó dồn toàn bộ thông tin quan trọng nhất của bức ảnh (những mảng màu mượt mà - tần số thấp) vào một góc ma trận, và đẩy các thông tin chi tiết siêu nhỏ, nhiễu hạt (tần số cao) sang góc bên kia.

Tiếp đó, JPG kích hoạt cỗ máy hủy diệt mang tên **Lượng tử hóa** (Quantization):

$$\text{Hệ số Lượng tử hóa} = \text{Làm tròn} \left( \frac{F(u,v)}{Q(u,v)} \right)$$

Hệ thống sẽ lấy các tần số cao chia cho một hằng số $Q$ rất lớn rồi làm tròn. Kết quả? Hàng loạt dữ liệu tần số cao bị nghiền nát thành các số $0$ tròn trĩnh. Chính chuỗi dài các số $0$ này giúp dung lượng file co ngót lại hàng chục lần. Đổi lại, dữ liệu bị mất vĩnh viễn.

Để đo lường sự biến dạng này, khoa học sử dụng công thức **Hệ số Sai số Trung bình Bình phương (MSE)** giữa ảnh gốc $I$ và ảnh đã giải nén $K$:

$$MSE = \frac{1}{m \cdot n} \sum_{i=0}^{m-1} \sum_{j=0}^{n-1} [I(i,j) - K(i,j)]^2$$

**(PHẦN 4: PNG - SỰ HOÀN MỸ CỦA NÉN KHÔNG TỔN HAO)**

Nếu sự hao hụt của JPG là bản án tử đối với các bản vẽ mạch điện tử, văn bản sắc nét hay ảnh y khoa, thì định dạng **PNG** xuất hiện như một đấng cứu thế. PNG sử dụng cơ chế nén không tổn hao (Lossless compression) – bảo toàn nguyên trạng từng bit dữ liệu.

Thay vì dùng phương trình tần số và cắt xén dữ liệu, PNG phân tích cấu trúc bức ảnh bằng các **Màng lọc nội suy dự báo (Predictive Filtering)**.

Nguyên lý của nó rất thanh lịch: Trong một mảng màu thực tế (như mảng tường hay bầu trời), các pixel nằm kề nhau thường có cường độ gần như bằng nhau. Thuật toán của PNG sẽ chạy một phương trình phỏng đoán giá trị của pixel tiếp theo. Sau đó, hệ thống chỉ lưu trữ hiệu số vi phân (kí hiệu là $\Delta$) giữa giá trị thực tế và giá trị phỏng đoán:

$$\Delta = f(x, y) - f_{\text{predict}}(x, y)$$

Quá trình dự báo này bóp méo một ma trận khổng lồ các giá trị từ 0 đến 255 thành một chuỗi các con số xoay quanh mức $0$. Sau đó, chuỗi số này được nén chặt bằng thuật toán **DEFLATE** (một sự kết hợp giữa cơ chế tìm kiếm cửa sổ trượt LZ77 và mã hóa xác suất trên cây nhị phân Huffman).

Kết quả cuối cùng? Thuật toán PNG có thể co ngót kích thước tệp từ 25% đến 50% mà không đánh rơi dù chỉ một hạt nhiễu nhỏ nhất, cho phép khôi phục hình ảnh với độ sắc nét tuyệt đối 100% kèm khả năng tách nền trong suốt!