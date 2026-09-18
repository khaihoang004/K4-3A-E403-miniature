from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from codebase.agent_tools import load_tool_schemas
from codebase.provider.gemini_provider import GeminiProvider

EVAL_DIR = Path(__file__).resolve().parent
GOLDEN_FILE = EVAL_DIR / "golden_set.json"
TOOLS_FILE = ROOT / "codebase" / "artifact" / "tools.yaml"
PROMPT_FILE = ROOT / "codebase" / "artifact" / "system_prompt.md"
RUNS_DIR = EVAL_DIR / "runs"
load_dotenv(ROOT / ".env")


def normalize(value: Any) -> Any:
    if isinstance(value, str):
        return value.strip().lower()
    if isinstance(value, dict):
        return {key: normalize(item) for key, item in value.items()}
    if isinstance(value, list):
        return [normalize(item) for item in value]
    return value


def compare_args(expected: dict[str, Any], actual: dict[str, Any]) -> list[str]:
    failures = []
    for key, expected_value in expected.items():
        if key not in actual:
            failures.append(f"missing arg {key}")
        elif normalize(actual[key]) != normalize(expected_value):
            failures.append(f"{key}: expected {expected_value!r}, got {actual[key]!r}")
    return failures


def evaluate(expected: dict[str, Any], actual: list[dict[str, Any]]) -> dict[str, Any]:
    if expected.get("no_tool"):
        return {"passed": not actual, "failures": [] if not actual else ["unexpected tool call"]}

    unmatched = list(actual)
    failures = []
    for expected_call in expected.get("tool_calls", []):
        matches = [item for item in unmatched if item["name"] == expected_call["name"]]
        if not matches:
            failures.append(f"missing tool call {expected_call['name']}")
            continue
        match = min(matches, key=lambda item: len(compare_args(expected_call.get("args", {}), item.get("args", {}))))
        unmatched.remove(match)
        failures.extend(compare_args(expected_call.get("args", {}), match.get("args", {})))
    failures.extend(f"extra tool call {item['name']}" for item in unmatched)
    return {"passed": not failures, "failures": failures}


def case_prompt(case: dict[str, Any]) -> str:
    if "turns" not in case:
        return case.get("query", "")
    previous = case["turns"][:-1]
    latest = case["turns"][-1]["content"]
    context = "\n".join(f"Earlier turn: {item['content']}" for item in previous)
    return f"Conversation context:\n{context}\n\nLatest user turn: {latest}"


def make_messages(system_prompt: str, case: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": case_prompt(case)},
    ]


def run_live(provider: GeminiProvider, system_prompt: str, tools: list[dict[str, Any]], case: dict[str, Any]) -> tuple[list[dict[str, Any]], str | None, str | None]:
    last_error = None
    for attempt in range(3):
        try:
            response = provider.complete(
                messages=make_messages(system_prompt, case),
                tools=tools,
                temperature=0.0,
                tool_choice="none" if case.get("expect", {}).get("no_tool") else "required",
            )
            calls = [{"name": call.name, "args": call.args} for call in response.tool_calls]
            return calls, response.text, None
        except Exception as exc:
            last_error = exc
            error_text = str(exc)
            retryable = any(marker in error_text for marker in ("429", "503", "UNAVAILABLE", "RESOURCE_EXHAUSTED"))
            if not retryable or attempt == 2:
                break
            time.sleep(2 * (attempt + 1))
    return [], None, f"{type(last_error).__name__}: {last_error}"


def run_mock(case: dict[str, Any]) -> tuple[list[dict[str, Any]], str | None, str | None]:
    expected = case.get("expect", {})
    calls = [dict(item) for item in expected.get("tool_calls", [])]
    return calls, "mock response", None


def write_logs(payload: dict[str, Any], timestamp: str) -> tuple[Path, Path]:
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    json_path = RUNS_DIR / f"agent_eval_{timestamp}.json"
    md_path = RUNS_DIR / f"agent_eval_{timestamp}.md"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        f"# Agent Eval: {payload['mode']}",
        "",
        f"Generated: {payload['generated_at']}",
        "",
        "| Case | Result | Tool calls | Details |",
        "|---|---|---:|---|",
    ]
    for result in payload["results"]:
        status = "PASS" if result["evaluation"]["passed"] else "FAIL"
        detail = "; ".join(result["evaluation"]["failures"]) or "-"
        lines.append(f"| {result['id']} | {status} | {len(result['actual_tool_calls'])} | {detail} |")
    lines.extend([
        "",
        f"Passed: {payload['summary']['passed_cases']}/{payload['summary']['total_cases']}",
        f"Accuracy: {payload['summary']['accuracy']:.1%}",
    ])
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return json_path, md_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate VLearn Agent tool selection against golden_set.json.")
    parser.add_argument("--mode", choices=["mock", "live"], default="mock")
    parser.add_argument("--case", action="append", dest="case_ids", help="Run only this case ID; repeatable.")
    args = parser.parse_args()

    dataset = json.loads(GOLDEN_FILE.read_text(encoding="utf-8"))
    cases = [case for case in dataset["cases"] if not args.case_ids or case["id"] in args.case_ids]
    tools = load_tool_schemas(TOOLS_FILE)
    declared = {tool["name"] for tool in tools}
    system_prompt = PROMPT_FILE.read_text(encoding="utf-8")
    provider = GeminiProvider(fallback_models=["gemini-3.1-flash-lite"]) if args.mode == "live" else None

    results = []
    for case in cases:
        if args.mode == "live":
            actual, text, error = run_live(provider, system_prompt, tools, case)
        else:
            actual, text, error = run_mock(case)
        undeclared = [call["name"] for call in actual if call["name"] not in declared]
        if error:
            evaluation = {"passed": False, "failures": [f"provider error: {error}"]}
        elif undeclared:
            evaluation = {"passed": False, "failures": [f"undeclared tool {name}" for name in undeclared]}
        else:
            evaluation = evaluate(case["expect"], actual)
        results.append({
            "id": case["id"],
            "query": case.get("query") or case.get("turns"),
            "expected": case["expect"],
            "actual_tool_calls": actual,
            "actual_text": text,
            "error": error,
            "evaluation": evaluation,
        })
        print(f"{case['id']:<28} {'PASS' if evaluation['passed'] else 'FAIL'}")

    passed = sum(item["evaluation"]["passed"] for item in results)
    payload = {
        "dataset_id": dataset.get("dataset_id"),
        "mode": args.mode,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "summary": {"total_cases": len(results), "passed_cases": passed, "accuracy": passed / len(results) if results else 0},
        "results": results,
    }
    json_path, md_path = write_logs(payload, datetime.now().strftime("%Y%m%dT%H%M%S"))
    print(f"\nPassed: {passed}/{len(results)}")
    print(f"JSON log: {json_path}")
    print(f"Markdown log: {md_path}")


if __name__ == "__main__":
    main()
