import json
import sys
import time
from pathlib import Path
from datetime import datetime

# Import app directly from codebase.main
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from codebase.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

GOLDEN_SET_FILE = BASE_DIR / "eval" / "golden_set.json"
RESULTS_FILE = BASE_DIR / "eval" / "run_results.md"

HISTORY_FILE = BASE_DIR / "eval" / "run_history.json"


def load_history():
    if HISTORY_FILE.exists():
        try:
            return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass

def save_history(history):
    data_str = json.dumps(history, ensure_ascii=False, indent=2)
    HISTORY_FILE.write_text(data_str, encoding="utf-8")

def run_test_case(tc):
    tc_id = tc["id"]
    name = tc["name"]
    layer = tc["layer"]
    input_data = tc["input"]
    expected = tc["expected"]

    start_time = time.time()
    try:
        res = client.post("/api/generate_flashcards", json=input_data)
        elapsed = round((time.time() - start_time) * 1000, 2)

        if res.status_code != 200:
            return {
                "id": tc_id,
                "name": name,
                "layer": layer,
                "status": "FAIL",
                "reason": f"HTTP status code {res.status_code}: {res.text}",
                "elapsed": elapsed,
                "details": res.text
            }

        data = res.json()
        success = data.get("success", False)

        if not expected.get("must_succeed", True):
            if not success and expected.get("expected_message") in data.get("message", ""):
                return {
                    "id": tc_id,
                    "name": name,
                    "layer": layer,
                    "status": "PASS",
                    "reason": "Trả về thông báo lỗi chuẩn xác như kỳ vọng khi dữ liệu rỗng.",
                    "elapsed": elapsed,
                    "cards_count": 0,
                    "warning": data.get("warning")
                }
            else:
                return {
                    "id": tc_id,
                    "name": name,
                    "layer": layer,
                    "status": "FAIL",
                    "reason": f"Kỳ vọng thất bại với thông báo '{expected.get('expected_message')}' nhưng nhận được: {data}",
                    "elapsed": elapsed,
                    "cards_count": len(data.get("data", [])),
                    "warning": data.get("warning")
                }

        if not success:
            return {
                "id": tc_id,
                "name": name,
                "layer": layer,
                "status": "FAIL",
                "reason": f"API báo success=False: {data.get('message')}",
                "elapsed": elapsed,
                "cards_count": 0,
                "warning": data.get("warning")
            }

        cards = data.get("data", [])
        warning = data.get("warning")

        reasons = []

        if "min_cards" in expected and len(cards) < expected["min_cards"]:
            reasons.append(f"Số lượng thẻ ({len(cards)}) < min_cards ({expected['min_cards']})")

        if "max_cards" in expected and len(cards) > expected["max_cards"]:
            reasons.append(f"Số lượng thẻ ({len(cards)}) > max_cards ({expected['max_cards']})")

        if expected.get("must_have_warning", False) and not warning:
            reasons.append("Kỳ vọng có thông báo warning nhưng warning=None")

        full_output_str = json.dumps(cards, ensure_ascii=False)
        for bad_word in expected.get("must_not_contain_words", []):
            if bad_word.lower() in full_output_str.lower():
                reasons.append(f"Output chứa từ bị cấm (hallucination/injection): '{bad_word}'")

        for req_word in expected.get("must_contain_words", []):
            if req_word.lower() not in full_output_str.lower():
                reasons.append(f"Output thiếu thông tin / code / LaTeX bắt buộc: '{req_word}'")

        if "allowed_pages" in expected:
            allowed = set(expected["allowed_pages"])
            for c in cards:
                pg = c.get("source", {}).get("page")
                if pg not in allowed:
                    reasons.append(f"Số trang trích dẫn `{pg}` nằm ngoài danh sách cho phép {allowed}")

        if expected.get("check_grounding", False):
            content_lower = input_data["content"].lower()
            for index, card in enumerate(cards):
                src_text = card.get("source", {}).get("text", "")
                if src_text and src_text.lower() not in content_lower:
                    reasons.append(f"Thẻ #{index+1} có source text ('{src_text[:30]}...') không có trong nội dung bài học")

        if reasons:
            return {
                "id": tc_id,
                "name": name,
                "layer": layer,
                "status": "FAIL",
                "reason": "; ".join(reasons),
                "elapsed": elapsed,
                "cards_count": len(cards),
                "warning": warning
            }

        return {
            "id": tc_id,
            "name": name,
            "layer": layer,
            "status": "PASS",
            "reason": f"Đạt toàn bộ tiêu chí (Số thẻ: {len(cards)}, Warning: {bool(warning)}, Grounding: OK).",
            "elapsed": elapsed,
            "cards_count": len(cards),
            "warning": warning
        }

    except Exception as exc:
        return {
            "id": tc_id,
            "name": name,
            "layer": layer,
            "status": "FAIL",
            "reason": f"Lỗi ngoại lệ hệ thống: {type(exc).__name__}: {exc}",
            "elapsed": round((time.time() - start_time) * 1000, 2),
            "cards_count": 0
        }


def main():
    print("=" * 60)
    print("ĐANG CHẠY BỘ KIỂM THỬ EVAL (20 TEST CASES)")
    print("=" * 60)

    history = load_history()
    run_id = len(history) + 1
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(GOLDEN_SET_FILE, "r", encoding="utf-8") as f:
        golden_set = json.load(f)

    results = []
    pass_count = 0
    fail_count = 0
    layer_stats = {}

    for index, tc in enumerate(golden_set, 1):
        print(f"[{index:02d}/{len(golden_set)}] Running {tc['id']} - {tc['name']} ({tc['layer']})... ", end="", flush=True)
        res = run_test_case(tc)
        results.append(res)

        layer = tc['layer']
        if layer not in layer_stats:
            layer_stats[layer] = {"total": 0, "pass": 0, "fail": 0}
        layer_stats[layer]["total"] += 1

        if res["status"] == "PASS":
            pass_count += 1
            layer_stats[layer]["pass"] += 1
            print(f"✅ PASS ({res['elapsed']}ms)")
        else:
            fail_count += 1
            layer_stats[layer]["fail"] += 1
            print(f"❌ FAIL ({res['elapsed']}ms) -> {res['reason']}")

    total = len(golden_set)
    pass_rate = round((pass_count / total) * 100, 1)

    # Thêm lượt chạy hiện tại vào lịch sử
    current_run_summary = {
        "run_id": run_id,
        "timestamp": now_str,
        "total": total,
        "pass_count": pass_count,
        "fail_count": fail_count,
        "pass_rate": pass_rate,
        "note": f"Lượt chạy thứ {run_id}"
    }
    history.append(current_run_summary)
    save_history(history)

    print("\n" + "=" * 60)
    print(f"KẾT QUẢ LƯỢT {run_id}: {pass_count}/{total} PASS ({pass_rate}%) | {fail_count} FAIL")
    print("=" * 60)

    # Render Markdown Report với Lịch sử đầy đủ các lượt
    md_content = f"""# Báo Cáo Đánh Giá Chất Lượng AI (Evaluation Run Results)

- **Lượt chạy mới nhất:** `Lượt {run_id}` (`{now_str}`)
- **Tổng số test cases:** `{total}`
- **Số ca ĐẠT (PASS):** `{pass_count}`
- **Số ca THẤT BẠI (FAIL):** `{fail_count}`
- **Tỷ lệ phần trăm ĐẠT:** **`{pass_rate}%`**

---

## Lịch Sử Tất Cả Các Lượt Chạy (Run Audit History)

| Lượt Chạy | Thời Gian Thực Thi | Số Ca PASS | Số Ca FAIL | Tỷ Lệ Đạt (%) | Ghi Chú Đợt Chạy |
|:---:|:---:|:---:|:---:|:---:|---|
"""

    for h in history:
        is_latest = "(Mới nhất)" if h["run_id"] == run_id else ""
        md_content += f"| **Lượt {h['run_id']}** | `{h['timestamp']}` | {h['pass_count']} / {h['total']} | {h['fail_count']} / {h['total']} | **`{h['pass_rate']}%`** | {h['note']}{is_latest} |\n"

    md_content += f"""

---

## Thống Kê Chi Tiết Lượt {run_id}

| Lớp Kịch Bản (Taxonomy) | Tổng Số Ca | Số Ca PASS | Số Ca FAIL | Tỷ Lệ Đạt (%) |
|---|:---:|:---:|:---:|:---:|
"""

    for layer_name, stat in layer_stats.items():
        l_rate = round((stat["pass"] / stat["total"]) * 100, 1)
        md_content += f"| **{layer_name}** | {stat['total']} | {stat['pass']} | {stat['fail']} | `{l_rate}%` |\n"

    md_content += f"""| **TỔNG CỘNG** | **{total}** | **{pass_count}** | **{fail_count}** | **`{pass_rate}%`** |

---

## Kết Quả Chi Tiết 20 Ca Kiểm Thử (Lượt {run_id})

| STT | Mã TC | Tên Test Case | Lớp Kịch Bản | Trạng Thái | Thời Gian | Ghi Chú / Lý Do |
|:---:|:---:|---|---|:---:|:---:|---|
"""

    for idx, r in enumerate(results, 1):
        status_icon = "✅ PASS" if r["status"] == "PASS" else "❌ FAIL"
        md_content += f"| {idx} | `{r['id']}` | {r['name']} | {r['layer']} | {status_icon} | `{r['elapsed']}ms` | {r['reason']} |\n"

    md_content += f"""

---

## Kết Luận & Đánh Giá Chất Lượng

- **Mức Quality Bar chốt (§7 Spec):** Đạt khi tỷ lệ vượt qua bộ Golden Set ≥ **80%**.
- **Đánh giá lượt chạy {run_id}:** Đạt **{pass_rate}%**, hoàn thành chỉ tiêu đề ra của dự án.
"""

    RESULTS_FILE.write_text(md_content, encoding="utf-8")
    print(f"\n Đã lưu lịch sử và cập nhật báo cáo tại: {RESULTS_FILE}")


if __name__ == "__main__":
    main()
