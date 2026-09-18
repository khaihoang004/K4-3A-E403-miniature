# Nhật ký thử nghiệm người dùng (User Testing Log) — R6

Nhóm thực hiện mời 5 người dùng bên ngoài nhóm (không tham gia phát triển sản phẩm) tham gia trải nghiệm trực tiếp Working Prototype của hệ thống **VLearn Flashcard Tự Động**. Trong đó có **2 người dùng thuộc danh sách Willing Users đã đăng ký từ mốc CP1** (Học viên T01 và Học viên T03).

---

## Bảng nhật ký thử nghiệm chi tiết (User Testing Matrix)

| Người thử | Nhiệm vụ giao (Task) | Điểm tắc nghẽn (Bottleneck) | Trích dẫn nguyên văn (Quote) | Quyết định xử lý của nhóm |
|---|---|---|---|---|
| **Học viên T01** *(Willing User CP1)* | 1. Đăng nhập với vai trò sinh viên.<br>2. Mở bộ flashcard bài Day 01.<br>3. Học và đánh giá các thẻ bằng 2 nút "Đã nhớ" / "Chưa nhớ". | Khi bấm "Chưa nhớ" ở một số thẻ khó (khái niệm Temperature và Top-p), hệ thống vẫn chuyển tiếp sang thẻ sau và kết thúc luôn bộ thẻ. Thẻ "Chưa nhớ" không được đẩy lại để ôn tiếp ngay trong session học như cam kết trong Canvas. | *"Ủa mình bấm Chưa nhớ câu này mà nó cứ trôi đi luôn, đến hết 10 thẻ là báo xong rồi chuyển sang màn hình tiến độ. Thế mấy câu chưa nhớ thì sau này mới xem lại được à, sao không lặp lại cho mình học lại luôn?"* | **Chấp nhận sửa ngay:** Bổ sung cơ chế tự động gom các thẻ "Chưa nhớ" vào vòng ôn tập tiếp theo (Missed Cards Re-queue) ngay khi hoàn thành vòng 1, kèm nút chọn "Ôn lại X thẻ chưa nhớ" cho đến khi học viên nắm chắc 100%. |
| **Học viên T03** *(Willing User CP1)* | 1. Dùng phím tắt để duyệt nhanh toàn bộ thẻ ôn tập.<br>2. Lật thẻ và ghi nhận trạng thái nhớ/quên bằng bàn phím. | Người dùng bấm phím `Space` để lật thẻ rất mượt, nhưng sau khi lật ra mặt sau thì buộc phải nhấc tay bấm chuột vào nút "Đã nhớ" hoặc "Chưa nhớ", làm đứt gãy luồng tập trung (flow) khi ôn bài nhanh. | *"Mình học flashcard hay để một tay trên phím bấm Space cho nhanh, mà lật xong lại phải cầm chuột nhấp nút Xanh nút Đỏ thì hơi cụt hứng. Có phím số kiểu bấm 1 là Chưa nhớ, 2 là Đã nhớ thì tiện hơn nhiều ấy."* | **Chấp nhận sửa ngay:** Bổ sung hotkey số `1` (Chưa nhớ - màu đỏ) và số `2` (Đã nhớ - màu xanh) khi thẻ đang ở trạng thái lật mở (`flipped`), cập nhật gợi ý phím tắt ngay dưới thanh điều khiển. |
| **Học viên T05** | 1. Xem mặt sau của thẻ chứa định nghĩa và số trang bài giảng.<br>2. Thực hiện chức năng "Báo lỗi" (Report) khi phát hiện thẻ giải thích chưa đủ ý. | Sau khi điền form báo lỗi và bấm "Gửi báo cáo", hệ thống báo thành công nhưng thẻ vẫn giữ nguyên trạng thái lật mở, không tự động chuyển sang thẻ tiếp theo hoặc có dấu hiệu thẻ đó đã được ghi nhận đánh dấu lỗi. | *"Mình bấm gửi báo lỗi xong nó hiện cái thông báo nhỏ tí ở góc trên rồi thôi, mình không biết là thẻ này đã được ghi nhận chưa hay mình phải ấn tiếp nút Sau để học tiếp."* | **Chấp nhận sửa trước demo:** Tự động đóng drawer báo lỗi, reset form và hiển thị badge/toast xác nhận rõ ràng, đồng thời cho phép tiếp tục học liền mạch mà không làm mất vị trí thẻ hiện tại. |
| **Học viên T07** | 1. Mở bộ thẻ công khai của giảng viên.<br>2. Muốn chỉnh sửa trực tiếp câu từ của đáp án theo cách hiểu riêng ngay trên màn hình học. | Không thể sửa trực tiếp nội dung thẻ trên giao diện học tập của deck công khai; người dùng tìm nút "Sửa" ngay trên thẻ nhưng chỉ thấy nút "Báo lỗi". | *"Thẻ này AI viết chuẩn sách giáo khoa nhưng hơi dài dòng, mình muốn sửa lại 1 câu ngắn gọn theo cách hiểu của mình ngay ở đây mà không thấy chỗ sửa, chỉ thấy nút báo lỗi."* | **Giữ nguyên thiết kế & Lập luận rõ:** Thẻ công khai (`published_decks`) là tài liệu chuẩn do giảng viên kiểm duyệt và phát hành cho toàn bộ lớp học, học viên không được quyền ghi đè làm sai lệch tài liệu chung. Hướng dẫn học viên dùng nút **"Sao bản cá nhân" (Clone Deck)** để sở hữu bản sao riêng và tự do thêm/sửa/xóa thẻ cá nhân theo nhu cầu. |
| **Học viên T08** | 1. Học thử thẻ có nội dung liên quan đến mã code Python (Prompt Engineering template).<br>2. Đọc và đối chiếu đoạn mã nguồn trích dẫn. | Cỡ chữ khối code (`<pre><code>`) trên màn hình laptop 13 inch hơi nhỏ, màu nền đen tương phản mạnh làm chữ bị chìm, khó đọc nhanh cú pháp thụt đầu dòng (indentation). | *"Mấy thẻ có đoạn code Python chữ hơi bé với dính nhau quá, nhìn trên laptop khó thấy mấy chỗ thụt dòng với dấu ngoặc kép."* | **Chấp nhận sửa ngay:** Tinh chỉnh CSS cho class `.back .a-text pre`, tăng kích thước font từ 12.5px lên 14px, giãn dòng code `line-height: 1.5`, tăng padding và độ tương phản cú pháp để dễ đọc trên mọi kích thước màn hình. |

---

## Tổng kết 4 dòng đúc kết (Theo chuẩn Rubric R6)

1. **Chủ đề lặp nhiều nhất:** Trải nghiệm luồng học tập chưa thực sự khép kín khi gặp thẻ "Chưa nhớ" (người dùng muốn được ôn lại ngay các câu sai thay vì chỉ nhận thống kê phần trăm) và nhu cầu thao tác phím tắt 100% không cần chuột.
2. **Sẽ sửa gì trước demo:**
   - Triển khai vòng lặp ôn lại các thẻ "Chưa nhớ" (Re-queue missed cards loop) trong cùng phiên học.
   - Thêm phím tắt `1` (Chưa nhớ) và `2` (Đã nhớ) sau khi lật thẻ.
   - Tăng font size và độ tương phản của khối code Python ở mặt sau thẻ.
3. **Giữ nguyên gì và vì sao:** Giữ nguyên quy tắc **không cho phép học viên sửa trực tiếp thẻ trên deck công khai của giảng viên**, vì đây là ranh giới an toàn (guardrail) bảo vệ tính chính xác của học liệu chuẩn chung; học viên muốn cá nhân hóa cần dùng tính năng "Sao bản cá nhân" (Clone).
4. **Gì để dành sau:** Thuật toán lặp lại ngắt quãng phức tạp (Spaced Repetition SM-2) tính ngày ôn tập tiếp theo (1 ngày, 3 ngày, 7 ngày) và tính năng đồng bộ highlight trực tiếp vào file slide PDF gốc.

