import os
import json
import pandas as pd
import requests
from datetime import datetime

from openpyxl.reader.excel import load_workbook

# Allure 결과 경로
ALLURE_RESULT_DIR = "allure-results"

# 디렉토리 존재 확인
if not os.path.exists(ALLURE_RESULT_DIR):
    print(f"❌ Allure 결과 디렉토리 없음: {ALLURE_RESULT_DIR}")
    exit(1)

# 날짜 기반 파일명 생성
now_str = datetime.now().strftime("%Y-%m-%d_%H-%M")
excel_filename = f"test-report_{now_str}.xlsx"

# 테스트 결과 파싱
data = []
for file_name in os.listdir(ALLURE_RESULT_DIR):
    if file_name.endswith("-result.json"):
        with open(os.path.join(ALLURE_RESULT_DIR, file_name), "r", encoding="utf-8") as f:
            result = json.load(f)
            name = result.get("name", "No Name")
            status = result.get("status", "unknown").upper()
            start = result.get("time", {}).get("start", 0)
            stop = result.get("time", {}).get("stop", 0)
            duration = (stop - start) / 1000
            message = result.get("statusDetails", {}).get("message", "")

            data.append({
                "테스트 이름": name,
                "상태": status,
                "소요 시간 (초)": round(duration, 2),
                "실패 메시지": message
            })
            data.sort(key=lambda x: x["테스트 이름"])

if not data:
    print("⚠️ 테스트 결과가 없습니다. Excel 리포트 생성을 건너뜁니다.")
    exit(0)

# Excel 저장
df = pd.DataFrame(data)
df.to_excel(excel_filename, index=False)


wb = load_workbook(excel_filename)
ws = wb.active

for column_cells in ws.columns:
    max_length = 0
    column_letter  = column_cells[0].column_letter
    for cell in column_cells:
        if cell.value:
            max_length = max(max_length, len(str(cell.value)))
        ws.column_dimensions[column_letter].width = max_length + 2

wb.save(excel_filename)



# Slack 업로드
SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK_URL")
if SLACK_WEBHOOK:
    with open(excel_filename, "rb") as file:
        response = requests.post(
            url=SLACK_WEBHOOK,
            files={"file": file},
            data={
                "filename": excel_filename,
                "channels": "#qa-report",
                "initial_comment": f"📊 *자동화 테스트 리포트 업로드 완료!* ({now_str})\n총 {len(df)}건의 테스트 결과가 포함되어 있습니다."
            }
        )

    if response.status_code == 200:
        print("✅ Slack 업로드 완료!")
    else:
        print(f"❌ Slack 업로드 실패! 상태 코드: {response.status_code}")
else:
    print("❌ SLACK_WEBHOOK_URL 환경변수가 설정되어 있지 않습니다.")