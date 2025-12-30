import os
import sys
import requests

# utils 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from parse_test_result import parse_test_result, get_failed_test_names


def send_slack_result():
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    github_run_id = os.getenv("GITHUB_RUN_ID")
    is_docker = os.getenv("DOCKER_ENV", "false").lower() == "true"
    branch_name = os.getenv("BRANCH_NAME", "main")
    branch_or_env = "docker" if is_docker else branch_name

    print(f"🔍 [DEBUG] Branch: {branch_name}")
    print(f"🔍 [DEBUG] GitHub Run ID: {github_run_id}")
    print(f"🔍 [DEBUG] Webhook URL 설정됨: {bool(webhook_url)}")

    if not webhook_url:
        print("❌ Slack Webhook URL이 설정되지 않았습니다.")
        print("💡 GitHub Secrets에 SLACK_WEBHOOK_URL을 설정하세요.")
        return


    ui_report_path = "reports/ui_report.xml" if is_docker else "ui_report.xml"
    api_report_path = "reports/api_report.xml" if is_docker else "api_report.xml"

    ui_passed, ui_failures, ui_errors, ui_skipped = parse_test_result(ui_report_path)
    api_passed, api_failures, api_errors, api_skipped = parse_test_result(api_report_path)


    failed_ui_tests = get_failed_test_names(ui_report_path)
    failed_api_tests = get_failed_test_names(api_report_path)
    all_failed_tests = failed_ui_tests + failed_api_tests

    passed = ui_passed + api_passed
    failures = ui_failures + api_failures
    errors = ui_errors + api_errors
    skipped = ui_skipped + api_skipped


    # GitHub Pages는 루트에 배포됨 (keep_files: false이므로 브랜치별 경로 없음)
    allure_report_url = "https://yoplekiller.github.io/QATEST/"
    excel_download_url = f"https://github.com/yoplekiller/QATEST/actions/runs/{github_run_id}"

    print(f"🔗 Allure Report URL: {allure_report_url}")
    print(f"🔗 GitHub Actions URL: {excel_download_url}")

    if all_failed_tests:
        failed_test_str = "❌ *실패한 테스트 목록:*\n" + "\n".join(f"- {name}" for name in all_failed_tests)
    else:
        failed_test_str = "✅ *모든 테스트가 완료되었습니다!* 🎉"


    message = {
        "text": (
            f"*📢 테스트 결과 요약*\n\n"
            f"✅ Passed: {passed}\n"
            f"❌ Failed: {failures}\n"
            f"⚠️ Errors: {errors}\n"
            f"⏭️ Skipped: {skipped}\n\n"
            f"{failed_test_str}\n\n"        
            f"*📄 Allure Report 보기*: <{allure_report_url}>\n"
            f"*📊 Excel 리포트 다운로드*: <{excel_download_url}>"
        )
    }

    print("📤 Slack으로 메시지 전송 중...")
    print(f"📊 테스트 결과: Passed={passed}, Failed={failures}, Errors={errors}, Skipped={skipped}")

    try:
        response = requests.post(webhook_url, json=message, timeout=10)
        if response.status_code == 200:
            print("✅ Slack 알림 전송 성공!")
        else:
            print(f"❌ Slack 전송 실패: HTTP {response.status_code}")
            print(f"응답 내용: {response.text}")
    except Exception as e:
        print(f"❌ Slack 전송 중 예외 발생: {e}")

if __name__ == "__main__":
    send_slack_result()
