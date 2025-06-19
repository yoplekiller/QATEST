import os
import json
import requests
import pandas as pd
from datetime import datetime
from openpyxl import load_workbook

# 📁 기본 설정
IS_DOCKER = os.getenv("DOCKER_ENV", "false").lower() == "true"
ALLURE_RESULT_DIR = "allure-results/docker" if IS_DOCKER else "allure-results"
SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK_URL")
REPORT_DIR = "reports"
os.makedirs(REPORT_DIR, exist_ok=True)

now_str = datetime.now().strftime("%Y-%m-%d_%H-%M")
excel_filename = os.path.join(REPORT_DIR, f"test-report_{now_str}.xlsx")


def load_allure_results(result_dir: str):
    if not os.path.exists(result_dir):
        print(f"❌ Allure 결과 디렉토리 없음: {result_dir}")
        return []

    data = []
    for file_name in os.listdir(result_dir):
        if file_name.endswith("-result.json"):
            with open(os.path.join(result_dir, file_name), "r", encoding="utf-8") as f:
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
                    "소요 시간 (초)": round(duration, 3),
                    "실패 메시지": message
                })

    return sorted(data, key=lambda x: x["테스트 이름"])


def generate_excel_report(data: list, filename: str):
    if not data:
        print("⚠️ 테스트 결과가 없습니다. Excel 리포트 생성을 건너뜁니다.")
        return False

    pass_count = sum(1 for d in data if d["상태"] == "PASSED")
    fail_count = sum(1 for d in data if d["상태"] == "FAILED")
    skip_count = sum(1 for d in data if d["상태"] == "SKIPPED")
    broken_count = sum(1 for d in data if d["상태"] == "BROKEN")
    total = len(data)
    success_rate = round((pass_count / total) * 100, 2)
    total_duration = round(sum(d["소요 시간 (초)"] for d in data), 2)

    summary_df = pd.DataFrame([{
        "전체 테스트": total,
        "성공": pass_count,
        "실패": fail_count,
        "스킵": skip_count,
        "브로큰": broken_count,
        "성공률 (%)": success_rate,
        "총 소요 시간 (초)": total_duration
    }])

    detail_df = pd.DataFrame(data)

    with pd.ExcelWriter(filename, engine="openpyxl") as writer:
        summary_df.to_excel(writer, sheet_name="요약 통계", index=False)
        detail_df.to_excel(writer, sheet_name="테스트 상세", index=False)

    # 열 너비 자동 조정
    wb = load_workbook(filename)
    for sheet in wb.worksheets:
        for column_cells in sheet.columns:
            max_length = max((len(str(cell.value)) if cell.value else 0) for cell in column_cells)
            col_letter = column_cells[0].column_letter
            sheet.column_dimensions[col_letter].width = max_length + 5
    wb.save(filename)
    print(f"✅ Excel 리포트 저장 완료: {filename}")
    return True


def upload_to_slack(filepath: str, webhook_url: str):
    if not webhook_url:
        print("❌ SLACK_WEBHOOK_URL 환경변수가 설정되어 있지 않습니다.")
        return

    with open(filepath, "rb") as file:
        response = requests.post(
            url=webhook_url,
            files={"file": file},
            data={
                "filename": os.path.basename(filepath),
                "channels": "#qa-report",
                "initial_comment": f"📊 *자동화 테스트 리포트 업로드 완료!* ({now_str})"
            }
        )

    if response.status_code == 200:
        print("✅ Slack 업로드 완료!")
    else:
        print(f"❌ Slack 업로드 실패! 상태 코드: {response.status_code}")


if __name__ == "__main__":
    print(f"✅ 실행 환경: {'Docker' if IS_DOCKER else 'Local'}")
    print(f"📁 결과 디렉토리: {ALLURE_RESULT_DIR}")
    results = load_allure_results(ALLURE_RESULT_DIR)
    if generate_excel_report(results, excel_filename):
        upload_to_slack(excel_filename, SLACK_WEBHOOK)
