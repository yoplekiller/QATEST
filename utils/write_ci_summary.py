"""
GitHub Actions 요약(GITHUB_STEP_SUMMARY)용 마크다운 표 생성.

pytest-json-report 는 재시도로 통과한 테스트를 outcome='rerun' 으로만 남기고 passed 에서 빼기 때문에,
conftest 가 만든 test_results_flaky.json 과 합쳐서 '첫 시도 통과 / 재시도 통과(flaky) / 실패'를 나눠 보여준다.

사용: python utils/write_ci_summary.py [json-report 경로] [flaky json 경로] >> $GITHUB_STEP_SUMMARY
"""
import json
import os
import sys


def load(path, default):
    if not os.path.exists(path):
        return default
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def build_summary(report: dict, flaky: dict) -> str:
    summary = report.get("summary", {})
    tests = report.get("tests", [])
    flaky_passed = flaky.get("flaky_passed_on_rerun", [])

    rows = [
        ("✅ 통과 (첫 시도)", summary.get("passed", 0)),
        ("⚠️ Flaky (재시도 후 통과)", len(flaky_passed)),
        ("❌ 실패", summary.get("failed", 0) + summary.get("error", 0)),
        ("🟡 Known issue (xfail)", summary.get("xfailed", 0)),
        ("⏭️ 스킵", summary.get("skipped", 0)),
    ]
    lines = ["## 🧪 UI 테스트 결과", "", "| 구분 | 개수 |", "|---|---:|"]
    lines += [f"| {name} | {count} |" for name, count in rows]

    failed = [t["nodeid"] for t in tests if t.get("outcome") in ("failed", "error")]
    if failed:
        lines += ["", "### ❌ 실패", *[f"- `{n}`" for n in failed]]
    if flaky_passed:
        lines += ["", "### ⚠️ Flaky - 재시도로 통과했지만 원인 확인 필요", *[f"- `{n}`" for n in flaky_passed]]
    xfailed = [t for t in tests if t.get("outcome") == "xfailed"]
    if xfailed:
        lines += ["", "### 🟡 Known issue (사이트 결함, xfail strict)"]
        lines += [f"- `{t['nodeid']}`" for t in xfailed]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    report_path = sys.argv[1] if len(sys.argv) > 1 else "test_results_ui.json"
    flaky_path = sys.argv[2] if len(sys.argv) > 2 else "test_results_flaky.json"
    sys.stdout.reconfigure(encoding="utf-8")
    print(build_summary(load(report_path, {}), load(flaky_path, {})))
