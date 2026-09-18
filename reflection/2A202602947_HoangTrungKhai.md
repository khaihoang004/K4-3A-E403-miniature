# Personal Reflection

## 1. Thông tin cá nhân

* **Họ và tên:** `Hoàng Trung Khải`
* **Mã số học viên:** `2A202602947`
* **Vai trò:** AI / Backend Developer
* **Dự án:** AI-powered Flashcard Generation System

---

## 2. Vai trò và phần việc trực tiếp phụ trách

Trong dự án, tôi phụ trách chính phần **xây dựng prototype backend và tích hợp AI cho hệ thống tự động tạo flashcard từ nội dung bài học**.

Các công việc tôi trực tiếp thực hiện gồm:

* Xây dựng API backend bằng **FastAPI** cho hệ thống flashcard.
* Tích hợp mô hình Gemini để tự động sinh flashcard từ nội dung bài học.
* Thiết kế cấu trúc dữ liệu của flashcard, bao gồm:

  * Question
  * Answer
  * Source
  * Page
  * Source text
* Xây dựng API cho quy trình:

  * Generate flashcards
  * Verify / chỉnh sửa flashcard
  * Publish flashcard deck
  * Clone deck thành bộ flashcard cá nhân
  * Thêm, sửa và xóa flashcard cá nhân
  * Review flashcard
  * Theo dõi learning progress
  * Report flashcard có vấn đề
* Refactor prototype từ một file backend lớn thành các module riêng biệt để dễ kiểm thử và debug.
* Thiết kế và tích hợp **SQLite** để lưu trữ deck, flashcard, lịch sử review và report thay cho việc lưu dữ liệu trực tiếp trong các file JSON.

Một quyết định thiết kế quan trọng của tôi là tách quá trình **AI generation** khỏi quá trình **persist dữ liệu**. Flashcard sau khi được AI tạo ra chưa được lưu ngay vào database. Người dùng có thể kiểm tra và chỉnh sửa trước, sau đó hệ thống mới publish và lưu dữ liệu vào SQLite. Điều này phù hợp với workflow của sản phẩm: **AI tạo → người dùng xác minh → publish → học → đánh giá/report**.

---

## 3. Cách tôi ứng dụng AI trong quá trình xây dựng

AI được sử dụng ở hai vai trò chính trong quá trình thực hiện dự án.

### 3.1. AI là một phần của sản phẩm

Trong prototype, AI được sử dụng để tạo flashcard từ nội dung bài học.

Input của hệ thống là nội dung bài học cùng với các thông tin như lesson ID và phần nội dung người dùng muốn tập trung. Backend gửi các thông tin này tới Gemini và yêu cầu mô hình trả về danh sách flashcard theo một schema xác định.

Kết quả không chỉ chứa câu hỏi và câu trả lời mà còn có **source** để người học có thể truy ngược lại nội dung bài học.

Tôi cũng xây dựng bước kiểm tra output của AI trước khi trả kết quả về frontend. Nếu AI trả về dữ liệu không đúng JSON hoặc không đúng schema flashcard, hệ thống sẽ báo lỗi thay vì lưu dữ liệu không hợp lệ.

### 3.2. AI hỗ trợ quá trình phát triển

Tôi sử dụng AI như một công cụ hỗ trợ trong quá trình:

* Thiết kế API.
* Đề xuất cấu trúc project.
* Refactor code.
* Thiết kế schema database.
* Debug các vấn đề liên quan đến backend.
* Viết và cải thiện prompt cho việc sinh flashcard.

Tuy nhiên, tôi không coi output của AI là kết quả cuối cùng. Các đoạn code và thiết kế được AI đề xuất đều cần được kiểm tra lại bằng cách chạy prototype và đối chiếu với yêu cầu của sản phẩm.

---

## 4. Bài học thực tế từ các trường hợp thất bại

Một bài học quan trọng tôi rút ra là **AI có thể tạo ra output trông hợp lý nhưng vẫn không đảm bảo output đó phù hợp với yêu cầu của sản phẩm**.

Trong quá trình xây dựng flashcard generator, nếu chỉ yêu cầu mô hình "tạo flashcard từ bài học", kết quả có thể chứa những câu hỏi quá chung, câu trả lời không đủ chính xác hoặc không chỉ rõ được nguồn trong bài học. Vì vậy, việc chỉ sử dụng LLM call là chưa đủ. Cần có schema, quality bar và bước xác minh trước khi dữ liệu được đưa vào hệ thống.

Bài học lớn nhất tôi rút ra là:

> **Một prototype AI tốt không chỉ cần chứng minh rằng AI có thể tạo ra kết quả, mà còn phải chứng minh rằng kết quả đó có thể được kiểm soát, xác minh, lưu trữ và sử dụng trong một workflow thực tế.**

---

## 5. Kết luận cá nhân

Qua dự án, tôi hiểu rõ hơn sự khác biệt giữa việc xây dựng một demo sử dụng LLM và xây dựng một prototype AI có thể sử dụng thực tế.

Tôi học được cách kết hợp **LLM + backend + database + validation + user workflow** thay vì chỉ tập trung vào prompt hoặc chất lượng output của mô hình.

