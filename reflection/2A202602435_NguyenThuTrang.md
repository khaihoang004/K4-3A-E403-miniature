# Personal Reflection

## 1. Thông tin cá nhân

* **Họ và tên:** `Nguyễn Thu Trang`
* **Mã số học viên:** `2A202602435`
* **Vai trò:** Product / Workflow Designer
* **Dự án:** AI-powered Flashcard Generation System

---

## 2. Vai trò và phần việc trực tiếp phụ trách

Trong dự án, tôi phụ trách chính vai trò Product / Workflow Designer, góp phần lập tài liệu AI Spec, khảo sát bài toán thực tế (Evidence mining) cho hệ thống.

Các công việc tôi trực tiếp thực hiện gồm:

* **Khảo sát bài toán & thu thập bằng chứng thực tế (Evidence):**
  * Phỏng vấn $n=12$ học viên VLearn để đào sâu nỗi đau khi ôn tập sau buổi học. Kết quả ghi nhận **75% học viên** thừa nhận việc tự làm flashcard thủ công tốn quá nhiều thời gian và khó duy trì, **50% sẵn sàng sử dụng** flashcard được trích xuất tự động từ slide bài giảng.
  * Thu thập và phân tích các trích dẫn nguyên văn (quotes) về việc đọc bài thụ động, dễ quên kiến thức cốt lõi và tốn công tra lại trang slide gốc khi làm sai thẻ.

* **Tài liệu AI Spec (`spec.md`):**
  * Thiết kế luồng sản phẩm (G1: Minh bạch khả năng hệ thống; G2: Trích dẫn nguồn `[Slide X - Trang Y]`; G9: Hỗ trợ chỉnh sửa thẻ; G10: Giới hạn phạm vi khi dữ liệu bài học quá ít).
  * Xây dựng **8 kịch bản rủi ro chi tiết** cho 4 lớp chỗ khó (Nguồn sự thật, Mơ hồ/thiếu thông tin, Ngoài phạm vi, Đặc thù domain toán/code) và quy định hành vi xử lý mong muốn.
  * Thiết kế **4 đường đi của trải nghiệm** (Happy path, Low-confidence, Failure, Correction) cùng các ranh giới an toàn (Guardrails) bảo vệ dữ liệu gốc của giảng viên.

---

## 3. Cách tôi ứng dụng AI trong quá trình xây dựng

AI được tôi ứng dụng đồng thời ở cả khía cạnh thiết kế sản phẩm và hỗ trợ công việc cá nhân.

### 3.1. AI là một phần của sản phẩm

Tôi không coi AI là một "phép thuật" tự giải quyết mọi thứ, mà là một thành tố cần được định hướng giao diện và luồng tương tác chặt chẽ:

* **Minh bạch trích dẫn nguồn gốc (Grounding & Source Tracing):** Yêu cầu mọi flashcard AI tạo ra bắt buộc phải đính kèm thẻ `[Trang N]` và đoạn văn bản gốc.
* **Xử lý tình huống tin cậy thấp (Low-confidence Handling):** Khi slide bài giảng chứa quá ít chữ hoặc toàn hình ảnh, thiết kế luồng hệ thống chủ động thông báo *"Nội dung bài học ngắn, AI chỉ trích xuất được các thẻ chắc chắn"* thay vì cố tình tạo đủ số lượng thẻ bịa đặt.
* **Thiết lập Ranh giới:** Chỉ cho phép tạo thẻ học từ nội dung có trong tài liệu bài học của VLearn, đồng thời ngăn chặn các yêu cầu hoặc prompt giả mạo nhằm tạo thẻ cho những môn học không thuộc chương trình.

### 3.2. AI hỗ trợ quá trình phát triển

Trong vai trò thiết kế luồng và khảo sát:

* Sử dụng AI để hỗ trợ phân loại và cụ thể hóa các nhóm rủi ro (Edge cases) liên quan đến định dạng code Python và công thức toán LaTeX.
* Sử dụng AI để tổng hợp các câu hỏi khảo sát người dùng theo chuẩn Mom Test và rà soát các điều khoản nguyên tắc PAIR/HAX.

Tuy nhiên, mọi đề xuất của AI đều được tôi đối chiếu lại với dữ liệu phỏng vấn thực tế từ học viên.

---

## 4. Bài học thực tế từ các trường hợp thất bại

Một bài học quan trọng tôi rút ra là **AI trả lời đúng chưa đủ, sản phẩm còn phải dễ dùng và phù hợp với thói quen của người dùng**. Trong thử nghiệm R6, dù AI tạo flashcard khá chính xác, học viên vẫn chưa hài lòng vì thẻ “Chưa nhớ” không được gom lại để ôn ngay và thao tác bằng bàn phím bị gián đoạn khi phải dùng chuột.

Vì vậy, tôi hiểu rằng một sản phẩm AI tốt cần có **trải nghiệm liền mạch, nguồn gốc nội dung rõ ràng, giới hạn kiểm soát phù hợp và đáp ứng đúng cách người dùng thực tế thao tác**.


---

## 5. Kết luận cá nhân

Dự án giúp tôi trưởng thành hơn rất nhiều trong tư duy làm sản phẩm AI và tôi hiểu được giá trị của việc liên tục kiểm tra và cải thiện sản phẩm dựa trên phản hồi từ người dùng thật. Những kinh nghiệm này sẽ là nền tảng để tôi tiếp tục xây dựng các sản phẩm AI hữu ích và thực tế trong tương lai.
