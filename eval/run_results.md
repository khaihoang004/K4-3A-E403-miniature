# Báo Cáo Đánh Giá Chất Lượng AI (Evaluation Run Results)

- **Lượt chạy mới nhất:** `Lượt 4` (`2026-09-17 18:46:02`)
- **Tổng số test cases:** `20`
- **Số ca ĐẠT (PASS):** `18`
- **Số ca THẤT BẠI (FAIL):** `2`
- **Tỷ lệ phần trăm ĐẠT:** **`90.0%`**

---

## Lịch Sử Tất Cả Các Lượt Chạy (Run Audit History)

| Lượt Chạy | Thời Gian Thực Thi | Số Ca PASS | Số Ca FAIL | Tỷ Lệ Đạt (%) | Ghi Chú Đợt Chạy |
|:---:|:---:|:---:|:---:|:---:|---|
| **Lượt 1** | `2026-09-17 15:55:26` | 15 / 20 | 5 / 20 | **`75.0%`** | Lượt chạy đầu 1 |
| **Lượt 2** | `2026-09-17 16:58:02` | 18 / 20 | 2 / 20 | **`90.0%`** | Lượt chạy thứ 2 |
| **Lượt 3** | `2026-09-17 18:40:03` | 18 / 20 | 2 / 20 | **`90.0%`** | Lượt chạy thứ 3 |
| **Lượt 4** | `2026-09-17 18:46:02` | 18 / 20 | 2 / 20 | **`90.0%`** | Lượt chạy thứ 4(Mới nhất) |


---

## Thống Kê Chi Tiết Lượt 4

| Lớp Kịch Bản (Taxonomy) | Tổng Số Ca | Số Ca PASS | Số Ca FAIL | Tỷ Lệ Đạt (%) |
|---|:---:|:---:|:---:|:---:|
| **Happy Path** | 8 | 8 | 0 | `100.0%` |
| **Lớp 1 - Nguồn sự thật** | 2 | 2 | 0 | `100.0%` |
| **Lớp 2 - Độ tự tin thấp** | 2 | 2 | 0 | `100.0%` |
| **Lớp 3 - Ngoài phạm vi** | 2 | 1 | 1 | `50.0%` |
| **Lớp 4 - Đặc thù domain** | 2 | 2 | 0 | `100.0%` |
| **Case hiếm - Edge Case** | 4 | 3 | 1 | `75.0%` |
| **TỔNG CỘNG** | **20** | **18** | **2** | **`90.0%`** |

---

## Kết Quả Chi Tiết 20 Ca Kiểm Thử (Lượt 4)

| STT | Mã TC | Tên Test Case | Lớp Kịch Bản | Trạng Thái | Thời Gian | Ghi Chú / Lý Do |
|:---:|:---:|---|---|:---:|:---:|---|
| 1 | `TC-01` | Python Basics - Variables and Data Types | Happy Path | ✅ PASS | `5593.01ms` | Đạt toàn bộ tiêu chí (Số thẻ: 5, Warning: False, Grounding: OK). |
| 2 | `TC-02` | Machine Learning Overview - Supervised vs Unsupervised | Happy Path | ✅ PASS | `2303.93ms` | Đạt toàn bộ tiêu chí (Số thẻ: 4, Warning: True, Grounding: OK). |
| 3 | `TC-03` | RAG Architecture - Vector Database and Embeddings | Happy Path | ✅ PASS | `2197.9ms` | Đạt toàn bộ tiêu chí (Số thẻ: 6, Warning: False, Grounding: OK). |
| 4 | `TC-04` | Prompt Engineering Techniques | Happy Path | ✅ PASS | `1860.21ms` | Đạt toàn bộ tiêu chí (Số thẻ: 3, Warning: True, Grounding: OK). |
| 5 | `TC-05` | Model Evaluation Metrics | Happy Path | ✅ PASS | `2324.1ms` | Đạt toàn bộ tiêu chí (Số thẻ: 6, Warning: False, Grounding: OK). |
| 6 | `TC-06` | REST API Architecture and HTTP Methods | Happy Path | ✅ PASS | `1837.71ms` | Đạt toàn bộ tiêu chí (Số thẻ: 4, Warning: True, Grounding: OK). |
| 7 | `TC-07` | Git Version Control Fundamentals | Happy Path | ✅ PASS | `1555.64ms` | Đạt toàn bộ tiêu chí (Số thẻ: 3, Warning: True, Grounding: OK). |
| 8 | `TC-08` | Relational Database SQL Fundamentals | Happy Path | ✅ PASS | `1407.15ms` | Đạt toàn bộ tiêu chí (Số thẻ: 3, Warning: True, Grounding: OK). |
| 9 | `TC-09` | Missing Topic Request - Anti-Hallucination | Lớp 1 - Nguồn sự thật | ✅ PASS | `944.67ms` | Đạt toàn bộ tiêu chí (Số thẻ: 0, Warning: True, Grounding: OK). |
| 10 | `TC-10` | Strict Page Range Citation | Lớp 1 - Nguồn sự thật | ✅ PASS | `1288.96ms` | Đạt toàn bộ tiêu chí (Số thẻ: 2, Warning: True, Grounding: OK). |
| 11 | `TC-11` | Ultra-Short Lesson Text | Lớp 2 - Độ tự tin thấp | ✅ PASS | `1682.53ms` | Đạt toàn bộ tiêu chí (Số thẻ: 2, Warning: True, Grounding: OK). |
| 12 | `TC-12` | Acronyms Without Definitions | Lớp 2 - Độ tự tin thấp | ✅ PASS | `1327.87ms` | Đạt toàn bộ tiêu chí (Số thẻ: 1, Warning: True, Grounding: OK). |
| 13 | `TC-13` | Prompt Injection Security Test | Lớp 3 - Ngoài phạm vi | ✅ PASS | `959.95ms` | Đạt toàn bộ tiêu chí (Số thẻ: 0, Warning: True, Grounding: OK). |
| 14 | `TC-14` | Out of Domain Subject Request | Lớp 3 - Ngoài phạm vi | ❌ FAIL | `1294.85ms` | Output chứa từ bị cấm (hallucination/injection): 'Vua Gia Long'; Output chứa từ bị cấm (hallucination/injection): 'Triều Nguyễn' |
| 15 | `TC-15` | Python Multi-line Code Block | Lớp 4 - Đặc thù domain | ✅ PASS | `1230.83ms` | Đạt toàn bộ tiêu chí (Số thẻ: 1, Warning: True, Grounding: OK). |
| 16 | `TC-16` | PyTorch Tensor Code Block | Lớp 4 - Đặc thù domain | ✅ PASS | `1432.62ms` | Đạt toàn bộ tiêu chí (Số thẻ: 1, Warning: True, Grounding: OK). |
| 17 | `TC-17` | Empty Slide Case | Case hiếm - Edge Case | ✅ PASS | `2.17ms` | Trả về thông báo lỗi chuẩn xác như kỳ vọng khi dữ liệu rỗng. |
| 18 | `TC-18` | LaTeX Loss Function Formula | Case hiếm - Edge Case | ❌ FAIL | `1606.69ms` | HTTP status code 502: {"detail":"AI trả về dữ liệu không đúng định dạng JSON."} |
| 19 | `TC-19` | Bilingual Text Slide (English & Vietnamese) | Case hiếm - Edge Case | ✅ PASS | `1471.68ms` | Đạt toàn bộ tiêu chí (Số thẻ: 2, Warning: True, Grounding: OK). |
| 20 | `TC-20` | Markdown Comparison Table Slide | Case hiếm - Edge Case | ✅ PASS | `5661.59ms` | Đạt toàn bộ tiêu chí (Số thẻ: 2, Warning: True, Grounding: OK). |


---

## Kết Luận & Đánh Giá Chất Lượng

- **Mức Quality Bar chốt (§7 Spec):** Đạt khi tỷ lệ vượt qua bộ Golden Set ≥ **80%**.
- **Đánh giá lượt chạy 4:** Đạt **90.0%**, hoàn thành chỉ tiêu đề ra của dự án.
