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
    '''미사용 코드'''
    # branch_or_env = "docker" if is_docker else branch_name

    print(f"🔍 [DEBUG] Branch: {branch_name}")
    print(f"🔍 [DEBUG] GitHub Run ID: {github_run_id}")
    print(f"🔍 [DEBUG] Webhook URL 설정됨: {bool(webhook_url)}")

    if not webhook_url:
        print("❌ Slack Webhook URL이 설정되지 않았습니다.")
        print("💡 GitHub Secrets에 SLACK_WEBHOOK_URL을 설정하세요.")
        return


    ui_report_path = "reports/ui_report.xml" if is_docker else "ui_report.xml"

    passed, failures, errors, skipped = parse_test_result(ui_report_path)

    all_failed_tests = get_failed_test_names(ui_report_path)


    # 브랜치별 Allure Report URL (슬래시를 대시로 변환)
    safe_branch = branch_name.replace("/", "-")
    allure_report_url = f"https://yoplekiller.github.io/QATEST/{safe_branch}/"
    excel_download_url = f"https://github.com/yoplekiller/QATEST/actions/runs/{github_run_id}"

    print(f"🔗 Allure Report URL: {allure_report_url}")
    print(f"🔗 GitHub Actions URL: {excel_download_url}")

    # 실패 테스트 요약 (최대 5개만 표시)
    MAX_DISPLAY_FAILURES = 5
    if all_failed_tests:
        displayed_failures = all_failed_tests[:MAX_DISPLAY_FAILURES]
        remaining_count = len(all_failed_tests) - MAX_DISPLAY_FAILURES

        failed_test_str = "❌ *실패한 테스트:*\n" + "\n".join(f"  • `{name}`" for name in displayed_failures)
        if remaining_count > 0:
            failed_test_str += f"\n  _...and {remaining_count}   more (전체 보기: <{allure_report_url}|Allure Report>)_"
    else:
        failed_test_str = "✅ *모든 테스트가 완료되었습니다!* 🎉"

    # 성공/실패에 따른 아이콘
    status_icon = "✅" if failures == 0 and errors == 0 else "❌"
    total_tests = passed + failures + errors + skipped

    message = {
        "text": f"{status_icon} 테스트 결과: {passed}/{total_tests} passed",
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"{status_icon} 테스트 실행 결과",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*✅ Passed:*\n{passed}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*❌ Failed:*\n{failures}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*⚠️ Errors:*\n{errors}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*⏭️ Skipped:*\n{skipped}"
                    }
                ]
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": failed_test_str
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "📊 Allure Report",
                            "emoji": True
                        },
                        "url": allure_report_url,
                        "style": "primary"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "🔍 GitHub Actions",
                            "emoji": True
                        },
                        "url": excel_download_url
                       
                    }
                ]
            }
        ]
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
