# Personal Reflection

## 1. Thông tin cá nhân

* **Họ và tên:** `Nguyễn Minh Dương`
* **Mã số học viên:** `2A202602920`
* **Vai trò:** Kỹ sư Prompt & Đánh giá (Prompt/Eval), Quay video & Thuyết trình (Demo)
* **Dự án:** AI-powered Flashcard Generation System

---

## 2. Vai trò và phần việc trực tiếp phụ trách

Trong dự án, tôi phụ trách chính phần **Kỹ sư Prompt, xây dựng bộ đánh giá (Eval) cho Agent, và thực hiện Demo sản phẩm**.

Các công việc tôi trực tiếp thực hiện gồm:

* **Thiết kế và tối ưu System Prompt:** Xây dựng prompt cho mô hình Gemini để đảm bảo AI trích xuất flashcard chính xác từ nội dung bài học, bám sát các nguyên tắc HAX và xử lý tốt 4 lớp lỗi (Nguồn sự thật, mơ hồ, ngoài phạm vi, đặc thù domain).
* **Xây dựng bộ kiểm thử (Golden Set):** Tạo file `eval/golden_set.json` gồm 24 case đa dạng:
  * 12 case routing và truyền arguments cho lesson/card CRUD.
  * 5 case thiếu thông tin, input không hợp lệ.
  * 4 case confirmation, cancellation.
  * 2 case ngoài phạm vi (out of bound).
  * 1 case multi-tool.
* **Chạy và cải thiện Eval:** Theo dõi các lượt chạy eval của hệ thống (từ 20.8% lên 95.8% pass rate), phân tích log để tìm nguyên nhân (ví dụ: thiếu API key, gọi tool thừa, hoặc model tự paraphrase lại nội dung khi confirm). Siết lại prompt dựa trên kết quả.
* **Chuẩn bị kịch bản và Demo:** Thiết kế kịch bản thể hiện rõ nhất các tính năng nổi bật của dự án (luồng Giảng viên tạo thẻ, luồng Học viên ôn tập). Trực tiếp quay video và chuẩn bị tài liệu thuyết trình để giới thiệu sản phẩm.

---

## 3. Cách tôi ứng dụng AI trong quá trình xây dựng

AI được sử dụng ở hai vai trò chính trong quá trình thực hiện dự án.

### 3.1. AI là cốt lõi của Agent xử lý

Trong hệ thống, AI (Gemini) đóng vai trò như một Agent điều phối luồng làm việc.
Nhiệm vụ của tôi là "dạy" Agent này bằng cách đưa ra các Instruction rõ ràng để nó biết khi nào cần gọi Read Tool (xem bài học) và khi nào cần gọi Write Tool (tạo thẻ, cập nhật thẻ, publish). Sự kết hợp giữa Prompt chặt chẽ và cấu trúc JSON Schema giúp AI trả về kết quả có thể trực tiếp render lên Frontend.

### 3.2. AI hỗ trợ quá trình phát triển và kiểm thử

Tôi sử dụng AI như một công cụ hỗ trợ trong quá trình:

* Lên ý tưởng và sinh dữ liệu giả lập cho 24 test case trong Golden Set.
* Viết script chạy Agent Evaluator tự động đánh giá và ghi log kết quả chạy (mock và live).
* Hỗ trợ viết và tinh chỉnh kịch bản quay video demo.
* Đề xuất các cách xử lý góc cạnh (corner cases) để đưa vào System Prompt.

---

## 4. Bài học thực tế từ các trường hợp thất bại

Một bài học đắt giá tôi rút ra là **sự thiếu ổn định của LLM khi xử lý các chuỗi hội thoại dài hoặc khi yêu cầu lặp lại dữ liệu**.

Trong quá trình chạy Eval, có trường hợp (case `L24_confirm_create`) khi người dùng xác nhận tạo flashcard, thay vì tái sử dụng nguyên payload đã sinh ra ở bước trước, mô hình lại tự ý diễn đạt lại (paraphrase) nội dung câu hỏi và câu trả lời. Điều này làm mất đi tính nhất quán và gây lỗi logic. 

Bài học lớn nhất tôi rút ra là:

> **Không bao giờ được tin tưởng hoàn toàn vào khả năng ghi nhớ nguyên văn của LLM qua nhiều lượt hội thoại. Cần kết hợp giữa kỹ thuật Prompt Engineering chặt chẽ và các cơ chế xử lý ở cấp độ Backend (lưu trữ payload tạm) để đảm bảo tính deterministic cho hệ thống.**

---

## 5. Kết luận cá nhân

Qua dự án, tôi nhận thấy vai trò của một Kỹ sư Prompt không chỉ dừng lại ở việc "viết câu lệnh hay", mà là thiết kế một hệ thống quy tắc (System Prompt), xác định ranh giới (Boundaries), và xây dựng bộ đo lường (Eval) để kiểm chứng mức độ hiệu quả. 

Việc theo dõi từ lượt chạy đầu tiên (chỉ pass 20.8%) cho đến khi tinh chỉnh đạt 95.8% là minh chứng rõ nhất cho việc: **AI chỉ thực sự hữu ích và an toàn khi chúng ta có đủ công cụ đo lường và kiểm soát hành vi của nó.**

