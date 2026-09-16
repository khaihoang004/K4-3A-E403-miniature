# Canvas 4 ô

## Người dùng và nỗi đau

**Người dùng chính:** Học viên VLearn sau mỗi buổi học.

**Nỗi đau:** Sau buổi học, học viên có nhiều kiến thức mới nhưng khó biết mình cần ôn lại gì và thường phải tự ghi chép, chọn lọc nội dung để làm flashcard. Việc ôn tập vì vậy tốn thời gian và dễ bỏ sót các khái niệm quan trọng.

**Giải pháp:** AI tự động tạo một bộ flashcard cá nhân từ nội dung bài học, tập trung vào các khái niệm, định nghĩa, công thức và điểm dễ nhầm. Học viên có thể dùng bộ thẻ này để tự kiểm tra mức độ hiểu bài thay vì chỉ đọc lại tài liệu.

**Giá trị chính:** Giảm thời gian chuẩn bị tài liệu ôn tập và giúp học viên chuyển từ **đọc lại bài → chủ động tự kiểm tra kiến thức**.

---

## Kiểm chứng ban đầu

### Giả thuyết cần kiểm chứng

> Học viên có nhu cầu ôn lại bài sau buổi học nhưng gặp khó khăn trong việc tự xác định nội dung quan trọng và tự tạo flashcard.

### Câu hỏi kiểm chứng

* Sau một buổi học, bạn thường ôn lại bài bằng cách nào?
* Bạn có từng tự tạo flashcard không? Nếu có, việc đó mất bao lâu?
* Phần nào trong quá trình ôn tập khiến bạn mất nhiều thời gian nhất?
* Bạn có thường bỏ sót những khái niệm quan trọng khi tự ôn không?
* Nếu VLearn tự tạo flashcard từ bài học, bạn sẽ sử dụng chúng vào thời điểm nào?
* Bạn muốn flashcard tập trung vào **định nghĩa, công thức, khái niệm, ví dụ hay lỗi dễ nhầm**?

### Tín hiệu thành công ban đầu

* Học viên xác nhận việc tự tạo flashcard là tốn thời gian hoặc khó duy trì.
* Học viên sẵn sàng sử dụng flashcard được tạo từ chính bài học.
* Học viên có thể chỉ ra những thẻ AI tạo ra hữu ích hoặc cần chỉnh sửa.
* Có học viên sử dụng lại bộ flashcard sau buổi học thay vì chỉ xem thử.

---

## Lát cắt

**Một học viên · sau một buổi học · AI tạo bộ flashcard từ nội dung bài học · học viên làm quiz nhanh để kiểm tra hiểu bài.**

### Luồng MVP

1. Học viên kết thúc một buổi học trên VLearn.
2. AI lấy **chỉ dữ liệu có trong pack/bài học được cung cấp**.
3. AI xác định các kiến thức quan trọng:

   * Khái niệm / định nghĩa
   * Công thức
   * Mối quan hệ giữa các khái niệm
   * Điểm dễ nhầm
4. AI tạo khoảng **10–15 flashcard**.
5. Mỗi flashcard gồm:

   * **Mặt trước:** câu hỏi / thuật ngữ.
   * **Mặt sau:** câu trả lời ngắn gọn dựa trên nội dung bài học.
   * **Nguồn:** trang / phần bài học mà thẻ được tạo từ.
6. Học viên chọn **Đã nhớ / Chưa nhớ**.
7. Hệ thống ưu tiên đưa các thẻ **Chưa nhớ** quay lại để ôn.
8. Học viên có thể đánh dấu thẻ AI tạo sai hoặc không rõ ràng.

### Hard tests

* **Data thưa:** Bài học có rất ít nội dung → AI không tự bịa thêm kiến thức.
* **Nội dung trùng lặp:** Hai trang cùng nói về một khái niệm → tránh tạo nhiều flashcard gần như giống nhau.
* **Signal nhiễu:** Câu hỏi/chat của một học viên xuất hiện quá nhiều → không để một người làm lệch toàn bộ bộ flashcard.
* **Không đủ căn cứ:** Không có thông tin trong dữ liệu bài học → AI phải nói rằng không đủ căn cứ thay vì đoán.
* **Giảng viên quyết định:** Flashcard chỉ là công cụ hỗ trợ học viên, không tự thay đổi nội dung giảng dạy.

### MVP không làm

* Không xây dựng hệ thống spaced repetition phức tạp.
* Không tạo flashcard từ dữ liệu ngoài pack.
* Không cố gắng thay thế tài liệu chính thức của giảng viên.
* Không công khai thông tin cho biết flashcard được tạo từ câu hỏi của học viên nào.

---

## Người dùng thử & Phân công

### Người dùng thử

**5–10 học viên** đã tham gia ít nhất một buổi học trên VLearn.

Mỗi người dùng thử:

1. Chọn một buổi học vừa hoàn thành.
2. Xem bộ flashcard AI tạo.
3. Làm thử 10–15 thẻ.
4. Đánh dấu thẻ hữu ích / không hữu ích / sai.
5. Trả lời khảo sát ngắn về trải nghiệm.

### Phân công

| Vai trò                | Công việc                                                                              |
| ---------------------- | -------------------------------------------------------------------------------------- |
| **AI / Backend**       | Trích xuất nội dung bài học, tạo flashcard, kiểm soát grounding và chống hallucination |
| **Frontend**           | Giao diện bộ flashcard, lật thẻ, Đã nhớ / Chưa nhớ, báo lỗi                            |
| **Data / Evaluation**  | Xây dựng test cases, kiểm tra chất lượng flashcard và các hard tests                   |
| **Product / UX**       | Thiết kế flow học viên, khảo sát người dùng, tổng hợp feedback                         |
| **Demo / Integration** | Tích hợp tính năng vào VLearn và chuẩn bị kịch bản demo                                |

### Tiêu chí demo

> **Sau một buổi học, một học viên có thể mở VLearn → nhận bộ flashcard được AI tạo từ chính nội dung buổi học → tự kiểm tra → biết mình cần ôn lại kiến thức nào.**
