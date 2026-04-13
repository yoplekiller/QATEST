import os
import json
import requests
from jira import JIRA
from dotenv import load_dotenv

load_dotenv()

JIRA_URL    = os.getenv("JIRA_URL")
JIRA_EMAIL  = os.getenv("JIRA_EMAIL")
JIRA_TOKEN  = os.getenv("JIRA_API_TOKEN")
PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")
WEBHOOK_URL = os.getenv("QA_SLACK_WEBHOOK_URL") or os.getenv("SLACK_WEBHOOK_URL", "")

os.makedirs("cache", exist_ok=True)
CACHE_FILE = "cache/jira_status_cache.json"

jira = JIRA(server=JIRA_URL, basic_auth=(JIRA_EMAIL, JIRA_TOKEN))

# Jira 이슈 상태 캐시 로드
issues = jira.search_issues(
    f'project={PROJECT_KEY} ORDER BY updated DESC',
    maxResults=200
)
print(f"[DEBUG] PROJECT_KEY={PROJECT_KEY}, 조회된 이슈 수={len(issues)}")
for issue in issues:
    print(f"[DEBUG] {issue.key} | {issue.fields.issuetype.name} | {issue.fields.status.name} | {issue.fields.summary}")
# "key" → "issue 객체" 매핑
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        cache = json.load(f)
else:
    cache = {}


changed = []

# 이슈 상태 비교 및 변경 감지   
for issue in issues:
    key = issue.key
    current_status = issue.fields.status.name
    previous_status = cache.get(key)

    if previous_status is None:
        # 처음 보는 티켓 → 캐시에 저장만 하고 알림 없음
        cache[key] = current_status

    elif previous_status != current_status:
        # 상태가 바뀐 티켓 → changed 리스트에 추가
        changed.append({
            "key": key,
            "summary": issue.fields.summary,
            "previous_status": previous_status,
            "current_status": current_status
        })
        cache[key] = current_status # 캐시 업데이트


if changed:
    text = "🔄 *Jira 티켓 상태 변경*\n\n"
    for item in changed:
        text += f"- {item['key']} ({item['summary']}): {item['previous_status']} → {item['current_status']}\n"

    if WEBHOOK_URL:
        try:
            response = requests.post(WEBHOOK_URL, json={"text": text}, timeout=10)
            print(f"[Slack] 응답 코드: {response.status_code}, 응답 내용: {response.text}")
            if response.status_code == 200:
                print(f"{len(changed)}건의 상태 변경 알림 전송 완료")
            else:
                print(f"[ERROR] Slack 전송 실패: {response.status_code}")
        except Exception as e:
            print(f"[ERROR] Slack 요청 중 예외 발생: {e}")
    else:
        print("QA_SLACK_WEBHOOK_URL이 설정되지 않아 알림 전송을 건너뜀")
else:
    print("상태 변경 감지된 티켓 없음")

# 캐시 파일 업데이트
with open(CACHE_FILE, "w", encoding="utf-8") as f:
    json.dump(cache, f, ensure_ascii=False, indent=2)
print("캐시 파일 업데이트 완료")
