# AI SPEC — Flashcard Tự Động Sau Buổi Học · Nhóm [Miniature] · Zone [5]
Hướng: [x] A — VLearn  [ ] B — Trợ lý Học viên  [ ] C — Làn mở
Loại: [x] Tính năng mới  [ ] Tối ưu tính năng có sẵn

## §1. User & Job
- **Job executor + workflow:** 
  - **Executor:** Học viên VLearn.
  - **Workflow:** Tham gia buổi học -> Xem lại tài liệu/video -> Lọc kiến thức quan trọng (định nghĩa, công thức) -> Tự ghi chép hoặc làm flashcard thủ công -> Ôn tập & tự kiểm tra lại trí nhớ.
- **Core JTBD:** Tự đánh giá và ghi nhớ các kiến thức trọng tâm (khái niệm, công thức, điểm dễ nhầm) sau mỗi buổi học một cách hệ thống mà không tốn thời gian chuẩn bị tài liệu.
- **Problem statement:** Sau khi kết thúc buổi học, học viên tiếp thu nhiều kiến thức mới nhưng không biết mình cần ôn lại trọng tâm phần nào. Việc tự chép tay, chọn lọc nội dung để làm thẻ ôn tập hoặc tạo câu hỏi trắc nghiệm khiến họ mất quá nhiều thời gian, dễ sinh ra tâm lý lười biếng hoặc bỏ sót các khái niệm cốt lõi, dẫn đến việc chỉ "lướt lại bài" một cách thụ động thay vì "tự kiểm tra" để hiểu sâu.
- **Evidence (dựa trên nhóm 5-10 người dùng thử ban đầu):**
  - **Số liệu mining / kết quả khảo sát:** `[n = 10]` học viên, `[XX]%` xác nhận việc tự tạo flashcard thủ công tốn quá nhiều thời gian và khó duy trì thường xuyên; `[XX]%` xác nhận sẵn sàng sử dụng flashcard được trích xuất trực tiếp từ bài học.
  - **≥5 quote/ví dụ nguyên văn + nguồn:** *(Điền quote thực tế từ bước "Câu hỏi kiểm chứng")*
    1. *"Học xong buổi nào mình cũng cố ghi lại định nghĩa, nhưng làm flashcard thủ công trên Anki/Quizlet tốn cả tiếng đồng hồ nên vài bữa là nản."* (Học viên A - Phỏng vấn)
    2. *"Lúc đọc lại slide thì thấy hiểu, nhưng gập máy lại là quên. Mình cần cái gì đó để tự test nhanh xem nhớ được bao nhiêu."* (Học viên B - Phỏng vấn)
    3. *"Mình hay bị sót các công thức nhỏ hoặc điểm dễ nhầm lẫn mà giảng viên nói lướt qua."* (Học viên C - Phỏng vấn)
    4. *"Nếu hệ thống tự tổng hợp sẵn flashcard của đúng bài hôm đó thì mình mở ra quẹt quẹt ôn lúc đi xe bus là tiện nhất."* (Học viên D - Phỏng vấn)
    5. *"Mình thích ôn bằng flashcard nhưng ngại nhất khâu soạn câu hỏi và tìm lại nguồn ở trang nào để tra lại lúc sai."* (Học viên E - Phỏng vấn)

## §2. Impact & quyết định chọn
- **Bảng impact ≥3 ứng viên:**

| Ứng viên (Giải pháp) | Đối tượng & Số lượng | Tần suất | Pain-point/Cost (Tốn gì mỗi lần) | Khả thi kỹ thuật |
|---|---|---|---|---|
| **1. Trích xuất Flashcard ôn tập tự động** | Học viên VLearn | Sau mỗi bài học / Hàng tuần | Tốn 30-60p soạn nội dung; dễ sót ý. | Cao (Chỉ dùng data bài học, format flashcard Q&A ngắn). |
| **2. Tóm tắt toàn bộ bài học thành văn bản** | Học viên VLearn | Sau mỗi bài học | Tốn thời gian đọc lại một đoạn dài, dễ đọc lướt. | Rất Cao (Summarization cơ bản). |
| **3. Chatbot QA tự động hỏi đáp theo bài** | Học viên VLearn | Khi ôn thi / Ôn tập | Tốn công nghĩ câu lệnh (prompt); dễ lan man. | Trung bình (Dễ bị hallucination ngoài bài học). |

- **Ứng viên ĐÃ LOẠI + vì sao:** 
  - **(2) Tóm tắt bài học:** Chỉ rút ngắn chữ, không giải quyết được nhu cầu "chủ động tự kiểm tra kiến thức" (active recall). Học viên vẫn ở trạng thái thụ động đọc lại bài.
  - **(3) Chatbot QA:** Đòi hỏi học viên phải chủ động biết mình đang không hiểu gì để hỏi. Hơn nữa, học viên có thể chat lan man ra ngoài phạm vi bài học (dễ sinh hallucination, vi phạm rule "chỉ lấy data có trong pack"). Ngoải ra sẽ phát sinh chi phí nhiều hơn khi hỏi đáp với AI.
- **Ứng viên CHỌN + vì sao:** **(1) Trích xuất Flashcard ôn tập tự động.** 
  - **Lý do (bằng số):** Giải quyết triệt để 100% thời gian chuẩn bị tài liệu (pain point lớn nhất). Giới hạn chặt chẽ scope của AI (chỉ tạo 10-15 thẻ từ data pack, chống hallucination hiệu quả). Cung cấp ngay một công cụ học chủ động (lật thẻ, chọn Đã nhớ/Chưa nhớ) mang lại giá trị tức thì ngay sau buổi học.

## §3. Giải pháp tương tự đã nghiên cứu
- [NotebookLM]: Học viên cần upload các tài liệu lên, AI của Google sẽ tạo các câu hỏi, flashcard tương ứng. Điểm trừ là hệ thống học liệu bị rò rỉ, không thống nhất cùng nền tảng.

## §4. Thiết kế
- Lát cắt MỘT CÂU (1 user · 1 việc · 1 quyết định AI · 1 kết quả):
> Giảng viên (1 user) chọn bài học đã có trên VLearn và tích chọn trọng tâm (1 việc), AI phân tích slide bài học và tạo bộ Flashcard nháp thẻ kèm trích dẫn `[Trang N]` (1 quyết định AI), Giảng viên xem lại và bấm 'Phát hành' cho học viên vào lật thẻ ôn tập active recall mà không tốn công soạn thủ công (1 kết quả).
- Non-goals (≥3 thứ KHÔNG build):
  1. Không cho phép học viên trực tiếp chỉnh sửa bộ thẻ gốc của bài học sau khi đã phát hành (chỉ được lật thẻ, đánh dấu "Đã nhớ / Chưa nhớ", hoặc bấm "Báo cáo lỗi / Tạo bản sao cá nhân").
  2. Không yêu cầu Giảng viên phải tải file ngoài lên (chỉ trích xuất dữ liệu từ các bài học đã có sẵn trên nền tảng VLearn).
  3. Không tích hợp đồng bộ tự động với ứng dụng bên thứ ba như Anki/Quizlet qua API (chỉ chạy trực tiếp trên hệ thống VLearn).
- Mức prototype nhắm tới: [ ] Sketch [ ] Mock [ ] Working — phần nào mock, phần nào thật:
- Automation: [ ] augment [ ] conditional [ ] automate — lý do theo cost-of-error:
- §4b. Nguyên tắc đã áp dụng (≥4 — HAX/PAIR, xem guide):
  | Nguyên tắc | Áp cụ thể vào đâu trong prototype |
  |---|---|
  | **G1 — Make clear what the system can do** | Ở Bước 1, giao diện Giảng viên ghi rõ: *"AI đọc nội dung bài học đã chọn và trích xuất thẻ nháp theo trọng tâm"*. |
  | **G2 — Make clear how well the system can do** | Ở Bước 3 (Kiểm duyệt), mỗi thẻ nháp đều hiển thị tag trích dẫn nguồn `[Slide X - Trang Y]` để Giảng viên dễ dàng kiểm tra độ chính xác. |
  | **G9 — Support efficient correction** | Ở Bước 3, Giảng viên xem lại danh sách thẻ nháp và có thể điều chỉnh hoặc duyệt trước khi chính thức nhấn *"Phát hành"*. |
  | **G10 — Scope services when uncertain** | Nếu bài học đã chọn có quá ít nội dung, AI không cố sinh đủ số thẻ yêu cầu mà chỉ sinh 3-5 thẻ chắc chắn kèm thông báo *"Nội dung bài học ngắn, AI chỉ trích xuất được 3 thẻ đạt độ tự tin cao"*. |

## §5. Kiểu lỗi — 4 lớp chỗ khó + kịch bản (≥8) [bảng theo guide §2.5]

## §6. Bốn đường đi của trải nghiệm
- **Happy path:**
  - **Bước 1 (Đầu vào):** Giảng viên chọn bài học đã có trên VLearn và chọn trọng tâm
  - **Bước 2 (AI xử lý):** AI phân tích tài liệu bài học và tự động tạo ra bộ 5-10 thẻ Flashcard nháp có trích dẫn `[Trang N]`.
  - **Bước 3 (Kiểm duyệt):** Giảng viên xem lại danh sách thẻ nháp, sau đó nhấn nút **"Phát hành (Publish)"**.
  - **Bước 4 (Phía học viên):** Học viên vào bài học thấy bộ thẻ đã phát hành, lật từng thẻ ôn tập và bấm đánh dấu *"Đã nhớ / Chưa nhớ"*.
- **Low-confidence path (Khi AI nghi ngờ / Độ tự tin thấp - ②):**
  - Bài học đã chọn có nội dung ngắn hoặc ít khái niệm $\rightarrow$ AI hiển thị thông báo: *"Bài học ngắn, AI chỉ trích xuất được 3 thẻ nháp chắc chắn"* $\rightarrow$ Giảng viên xem duyệt 3 thẻ và có thể tạo thêm thẻ trước khi bấm *"Phát hành"*.
- **Failure / Không căn cứ (Khi không tìm thấy thông tin - ①):**
  - Giảng viên chọn bài học chưa có nội dung slide/văn bản $\rightarrow$ AI thông báo lỗi: *"Bài học này chưa có dữ liệu slide để trích xuất thẻ. Vui lòng chọn bài học khác."*
- **Correction (Cơ chế người dùng sửa kết quả):**
  - **Phía Giảng viên (Bước 3):** Xem lại toàn bộ danh sách thẻ nháp trước khi quyết định ấn "Phát hành".
  - **Phía Học viên (Bước 4):** Học viên không được chỉnh sửa bộ thẻ gốc của bài học, nhưng có thể bấm *"Báo cáo lỗi thẻ"* (gửi phản hồi cho Giảng viên) hoặc bấm *"Tạo bản sao cá nhân"* để tự chỉnh sửa bản riêng theo ý mình.
- **Khi bị đòi ngoài phạm vi (③):**
  - Học viên hoặc Giảng viên yêu cầu sinh thẻ từ nội dung ngoài bài học đã chọn $\rightarrow$ AI từ chối và báo rõ: *"Tutor chỉ hỗ trợ tạo Flashcard từ dữ liệu của bài học được chọn trên VLearn"*.
- **Case đặc thù domain (④):**
  - Bài học chứa khối mã nguồn (code block) hoặc công thức phức tạp $\rightarrow$ AI giữ nguyên định dạng code/công thức trên mặt thẻ, không tự ý tóm tắt làm sai cú pháp lập trình.

## §7. Kiểm thử
- Chiều chất lượng + định nghĩa kiểm chứng được:
- Golden set (≥20 case theo cơ cấu trong guide §2.6, file trong eval/):
- Quality bar (chốt từ hạn chốt spec của khoá, giữ nguyên sau đó): "Đạt khi ≥ ___% qua bộ, và ___"
- Kết quả các lượt chạy (bảng % — cập nhật đến trước CP6):

## §8. Phân công & kế hoạch
- Phân công có tên: spec / evidence / prompt / code / demo
- Willing users (≥2 tên) + kế hoạch vòng validation *(bonus, nếu làm)*:
- Multi-prototype (nếu làm): trục khác biệt của ≥2 phương án + lý do chọn:

## §9. Changelog
| Thời điểm | Đổi gì | Vì sao (trỏ về feedback/case nào) |