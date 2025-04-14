import requests
import json

SLACK_URL = "https://hooks.slack.com/services/..."

message = {
  "text": "[ZAP] 보안 스캔 완료! 리포트를 확인해주세요.\n📄 `/zap/allure-results/zap-report.html`"
}

requests.post(SLACK_URL, data=json.dumps(message))