"""
테스트 결과 JSON을 읽어 실패 항목을 Jira 버그 티켓으로 자동 등록
GitHub Actions에서 실행: python utils/create_jira_bugs.py
"""
import os
import json
import glob
from datetime import datetime
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

# 각 결과 파일에서 실패 항목 추출
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

# 기존 자동버그 티켓 조회 (Done 포함 전체 - 재발 시 리오픈을 위해)
existing = jira.search_issues(
    f'project={PROJECT_KEY} AND issuetype=Bug AND summary ~ "자동버그"',
    maxResults=200
)
# "fname / func" 조합 → issue 객체 매핑
existing_map = {}
for i in existing:
    s = i.fields.summary
    if "] " in s:
        key = s.split("] ")[-1].split(" - ")[0].strip()  # "fname / func"
        existing_map[key] = i

created = []
skipped = []
reopened = []

now_str = datetime.now().strftime("%Y-%m-%d %H:%M")

# 실패 항목별로 티켓 생성 또는 리오픈 처리
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

    # 기존 티켓 존재 여부 확인
    if dup_key in existing_map:
        existing_issue = existing_map[dup_key]
        status_cat = existing_issue.fields.status.statusCategory.key  # "done" / "indeterminate" / "new"

        if status_cat == "done":
            # 완료된 버그가 재발 → 리오픈
            transitions = jira.transitions(existing_issue)
            reopen_t = next(
                (t for t in transitions if any(kw in t["name"].lower() for kw in ["reopen", "재열기", "재오픈", "open"])),
                None
            )
            if reopen_t:
                jira.transition_issue(existing_issue, reopen_t["id"])
                jira.add_comment(
                    existing_issue,
                    f"*[자동] 버그 재발 감지 — {now_str}*\n\n"
                    f"이전에 완료 처리된 버그가 다시 실패했습니다.\n\n"
                    f"*에러 로그:*\n{{code}}\n{longrepr_short}\n{{code}}"
                )
                print(f"  [REOPEN] {existing_issue.key} - {summary}")
                reopened.append(existing_issue.key)
            else:
                # 리오픈 트랜지션 없으면 코멘트만 추가
                jira.add_comment(
                    existing_issue,
                    f"*[자동] 버그 재발 감지 — {now_str}* (리오픈 트랜지션 없음, 코멘트로 대체)\n\n"
                    f"{{code}}\n{longrepr_short}\n{{code}}"
                )
                print(f"  [COMMENT] 리오픈 트랜지션 없음, 코멘트 추가: {existing_issue.key}")
                reopened.append(existing_issue.key)
        else:
            # 이미 오픈 중 → 스킵
            print(f"  [SKIP] 이미 오픈 중 ({existing_issue.fields.status.name}): {existing_issue.key}")
            skipped.append(summary)
        continue

    # 새 버그 티켓 생성
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

print(f"\n완료: {len(created)}개 생성, {len(reopened)}개 리오픈, {len(skipped)}개 스킵")
