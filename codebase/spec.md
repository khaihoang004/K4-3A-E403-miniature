# AI SPEC — Flashcard Tự Động Sau Buổi Học · Nhóm [XX] · Zone [X]
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
  - **(3) Chatbot QA:** Đòi hỏi học viên phải chủ động biết mình đang không hiểu gì để hỏi. Hơn nữa, học viên có thể chat lan man ra ngoài phạm vi bài học (dễ sinh hallucination, vi phạm rule "chỉ lấy data có trong pack").
- **Ứng viên CHỌN + vì sao:** **(1) Trích xuất Flashcard ôn tập tự động.** 
  - **Lý do (bằng số):** Giải quyết triệt để 100% thời gian chuẩn bị tài liệu (pain point lớn nhất). Giới hạn chặt chẽ scope của AI (chỉ tạo 10-15 thẻ từ data pack, chống hallucination hiệu quả). Cung cấp ngay một công cụ học chủ động (lật thẻ, chọn Đã nhớ/Chưa nhớ) mang lại giá trị tức thì ngay sau buổi học.

## §3. Giải pháp tương tự đã nghiên cứu
- [Sản phẩm 1]: flow / đáng học / đáng né / mình khác gì
- [Sản phẩm 2]: ...

## §4. Thiết kế
- **Lát cắt MỘT CÂU:** Sau khi học xong, học viên bấm "Tạo Flashcard", hệ thống tự động đọc nội dung bài học và trích xuất 10-15 thẻ (Câu hỏi - Đáp án) để ôn tập.
- **Non-goals (≥3 thứ KHÔNG build):**
  1. Không lấy dữ liệu ngoài (chỉ dùng nội dung có sẵn trong bài học để tránh AI bịa đặt).
  2. Không làm các dạng câu hỏi phức tạp (chỉ làm flashcard lật 2 mặt cơ bản).
  3. Không chấm điểm tự động (học viên tự lật thẻ và tự đánh giá Đã nhớ/Chưa nhớ).
- **Mức prototype nhắm tới:** [ ] Sketch [ ] Mock [x] Working
  - **Phần mock:** Giao diện web tổng thể và **nội dung bài học (được giả lập bằng cách sinh ra tóm tắt từ 2 slide PDF trong data được cung cấp).**
  - **Phần thật:** Logic gọi API AI để sinh thẻ từ text giả lập, lưu database (SQLite), luồng lật thẻ, và thao tác sửa/xoá thẻ.
- **Automation:** [x] augment [ ] conditional [ ] automate
  - **Lý do (cost-of-error):** Hậu quả nếu AI sinh thẻ sai là thấp, nhưng vì là công cụ học tập, học viên cần giữ quyền chủ động. AI chỉ đóng vai trò hỗ trợ (augment) tạo bản nháp, học viên tự duyệt và sửa trước khi học.

- **§4b. Nguyên tắc đã áp dụng (HAX/PAIR):**
  | Nguyên tắc | Áp cụ thể vào đâu trong prototype |
  |---|---|
  | **Nêu rõ khả năng của hệ thống** | Tooltip ở nút tạo thẻ: *"Hệ thống sẽ đọc bài học này để tự tạo 10-15 thẻ trọng tâm."* |
  | **Nêu rõ giới hạn của hệ thống** | Cảnh báo khi bài ngắn: *"Nội dung ít, AI chỉ tạo được [X] thẻ. Vui lòng tạo thêm thủ công."* |
  | **Hiển thị ngữ cảnh (Context)** | Mỗi thẻ sinh ra đều có trường **Nguồn** (đoạn text gốc) để người dùng đối chiếu. |
  | **Hỗ trợ chỉnh sửa (Correction)** | Nút **Sửa/Xóa** ngay trên mỗi thẻ để học viên tự viết lại đáp án theo ý hiểu. |

## §5. Kiểu lỗi — 4 lớp chỗ khó + kịch bản (≥8) [bảng theo guide §2.5]

## §6. Bốn đường đi của trải nghiệm
- **Happy path:** Bấm tạo -> AI đọc text -> Trả về JSON chuẩn -> Giao diện hiện 10-15 thẻ bám sát bài học -> Học viên lật thẻ, chọn "Đã nhớ/Chưa nhớ".
- **Low-confidence (②):** Text bài học bị ngắn hoặc chung chung -> AI tạo được ít thẻ (<5) -> Hiện cảnh báo AI thiếu thông tin và khuyến khích học viên bấm nút "Thêm thẻ" thủ công.
- **Failure/không căn cứ (①):** Bài học không trích xuất được text hoặc API lỗi -> Thông báo *"Không thể sinh tự động lúc này. Vui lòng tự tạo flashcard"* và hiện sẵn form trống.
- **Correction (user sửa):** AI làm thẻ hơi khó hiểu -> Học viên bấm "Sửa", gõ lại nội dung theo ý mình -> Hệ thống lưu thành thẻ cá nhân riêng.
- **Khi bị đòi ngoài phạm vi (③):** Do hệ thống khóa luồng (chỉ đọc text đầu vào, không có chỗ cho user chat tự do) và prompt yêu cầu khắt khe "chỉ dùng text được cung cấp", AI sẽ từ chối sinh thẻ bịa đặt.
- **Case đặc thù domain (④):** Các môn như Toán, Code có thể bị lỗi format (mất dấu, vỡ công thức) -> Học viên dùng tính năng **Report (Báo cáo)** để báo cho admin cập nhật pack gốc hoặc tự ấn Edit để sửa nhanh.

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