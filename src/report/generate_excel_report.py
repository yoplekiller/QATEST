import os
import json
import pandas as pd
import requests
from datetime import datetime

#Allure 결과 경로
ALLURE_RESULT_DIR = "allure-results/docker"

#날짜 기반 파일명 생성
now_str = datetime.now().strftime("%Y-%m-%d-%H-%M")
execl_filename = f"test-report_{now_str}.xlsx"


data = []
for file_name in os.listdir(ALLURE_RESULT_DIR):
    if file_name.endswith("-result.json"):
        with open(os.path.join(ALLURE_RESULT_DIR, file_name), "r", encoding="utf-8") as f:
            result = json.load(f)
            name = result.get("name", "No Name")
            status = result.get("status", "unknown").upper()
            time = result.get("time", {}).get("duration", 0) / 1000
            message = result.get("statusDetails", {}).get("message", "")
            data.append({
                "테스트 이름": name,
                "상태": status,
                "소요 시간 (초)": round(time, 2),
                "실패 메시지": message
            })

df = pd.DataFrame(data)
df.to_excel(execl_filename, index=False)
print("report 파일 생성 완료")

SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK_URL")
with open("test-report.xlsx", "rb") as file:
    response = requests.post(
        url=SLACK_WEBHOOK,
        files={"file": file},
        data={"filename": "test-report.xlsx", "channels": "#qa"}
    )
if response.status_code == 200:
    print("✅ Slack 업로드 완료!")
else:
    print(f"❌ Slack 업로드 실패! 상태 코드: {response.status_code}")
