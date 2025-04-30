import os
import requests
from parse_test_result import parse_test_result

def send_slack_result():
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    github_run_id = os.getenv("GITHUB_RUN_ID")  # 추가


    if not webhook_url:
        print("❌ Slack Webhook URL이 설정되지 않았습니다.")
        return

    ui_passed, ui_failures, ui_errors, ui_skipped = parse_test_result("ui_report.xml")
    api_passed, api_failures, api_errors, api_skipped = parse_test_result("api_report.xml")

    passed = ui_passed + api_passed
    failures = ui_failures + api_failures
    errors = ui_errors + api_errors
    skipped = ui_skipped + api_skipped

    allure_report_url = "https://yoplekiller.github.io/QATEST/allure-report/index.html"
    excel_download_url = f"https://github.com/yoplekiller/QATEST/actions/runs/{github_run_id}"

    message = {
        "text": (
            f"*📢 테스트 결과 요약*\n\n"
            f"✅ Passed: {passed}\n"
            f"❌ Failed: {failures}\n"
            f"⚠️ Errors: {errors}\n"
            f"⏭️ Skipped: {skipped}\n\n"
            f"*📄 Allure Report 보기*: <{allure_report_url}>\n"
            f"*📊 Excel 리포트 다운로드*: <{excel_download_url}>"
        )
    }

    response = requests.post(webhook_url, json=message)
    if response.status_code != 200:
        print(f"❌ Slack 전송 실패: {response.status_code}, {response.text}")

if __name__ == "__main__":
    send_slack_result()
