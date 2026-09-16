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
- Non-goals (≥3 thứ KHÔNG build):
- Mức prototype nhắm tới: [ ] Sketch [ ] Mock [ ] Working — phần nào mock, phần nào thật:
- Automation: [ ] augment [ ] conditional [ ] automate — lý do theo cost-of-error:
- §4b. Nguyên tắc đã áp dụng (≥4 — HAX/PAIR, xem guide):
  | Nguyên tắc | Áp cụ thể vào đâu trong prototype |
  |---|---|

## §5. Kiểu lỗi — 4 lớp chỗ khó + kịch bản (≥8) [bảng theo guide §2.5]

## §6. Bốn đường đi của trải nghiệm
- Happy path: · Low-confidence (②): · Failure/không căn cứ (①): · Correction (user sửa):
- Khi bị đòi ngoài phạm vi (③): · Case đặc thù domain (④):

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