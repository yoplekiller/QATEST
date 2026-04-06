"""
테스트 결과 JSON을 읽어 실패 항목을 Jira 버그 티켓으로 자동 등록
GitHub Actions에서 실행: python utils/create_jira_bugs.py
"""
import os
import json
import glob
from jira import JIRA
from dotenv import load_dotenv

load_dotenv()

JIRA_URL    = os.getenv("JIRA_URL")
JIRA_EMAIL  = os.getenv("JIRA_EMAIL")
JIRA_TOKEN  = os.getenv("JIRA_API_TOKEN")
PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")

jira = JIRA(server=JIRA_URL, basic_auth=(JIRA_EMAIL, JIRA_TOKEN))

# UI + API 결과 파일 수집
result_files = ["test_results_ui.json", "test_results_api.json"]
all_failed = []

for fname in result_files:
    if not os.path.exists(fname):
        print(f"[SKIP] {fname} 없음")
        continue
    with open(fname, "r", encoding="utf-8") as f:
        report = json.load(f)
    failed = [
        t for t in report.get("tests", [])
        if t.get("outcome") in ("failed", "error")
    ]
    print(f"[{fname}] 실패 {len(failed)}건")
    for t in failed:
        t["_source"] = fname
    all_failed.extend(failed)

if not all_failed:
    print("실패 항목 없음 - 버그 티켓 생성 불필요")
    exit(0)

print(f"\n총 {len(all_failed)}건 -> Jira 버그 티켓 생성\n")

# 기존 자동버그 티켓 조회 (중복 방지) - 오픈 상태만 체크
existing = jira.search_issues(
    f'project={PROJECT_KEY} AND issuetype=Bug AND summary ~ "[자동버그]" AND statusCategory != Done',
    maxResults=200
)
# "fname / func" 조합으로 중복 키 생성
existing_keys = set()
for i in existing:
    s = i.fields.summary
    if "] " in s:
        key = s.split("] ", 1)[-1].split(" - ")[0].strip()  # "fname / func"
        existing_keys.add(key)

created = []
skipped = []

for t in all_failed:
    nodeid  = t["nodeid"]
    outcome = t["outcome"]
    source  = t.get("_source", "")

    # 에러 메시지
    call = t.get("call", {})
    longrepr = call.get("longrepr", "에러 없음")
    longrepr_short = longrepr[:2000]

    # 테스트 파일 + 함수명
    parts   = nodeid.replace("\\", "/").split("/")
    fname   = parts[-1].split("::")[0] if "::" in parts[-1] else parts[-1]
    func    = nodeid.split("::")[-1] if "::" in nodeid else nodeid
    category = "UI" if "ui" in source else "API"

    summary = f"[자동버그][{category}] {fname} / {func} - {outcome}"
    dup_key = f"{fname} / {func}"

    if dup_key in existing_keys:
        print(f"  [SKIP] {summary}")
        skipped.append(summary)
        continue

    description = f"""*자동 생성 버그 티켓 (GitHub Actions)*

||항목||내용||
|카테고리|{category}|
|테스트 파일|{fname}|
|테스트 함수|{func}|
|결과|{outcome}|
|소스|{source}|

*에러 로그:*
{{code}}
{longrepr_short}
{{code}}
"""

    try:
        issue = jira.create_issue(
            project=PROJECT_KEY,
            summary=summary,
            description=description,
            issuetype={"name": "Bug"},
        )
        print(f"  [OK] {issue.key} - {summary}")
        created.append(issue.key)
    except Exception as e:
        print(f"  [FAIL] {func}: {e}")

print(f"\n완료: {len(created)}개 생성, {len(skipped)}개 스킵")
