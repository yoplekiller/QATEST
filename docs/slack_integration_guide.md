# Slack 알림 통합 가이드

## 문제 상황
- Slack 알림 코드는 있지만 GitHub Actions에서 호출하지 않음
- 따라서 테스트 완료 후 Slack 알림이 전송되지 않음

## 해결 방법

### 1. GitHub Actions 워크플로우 수정

**파일:** `.github/workflows/Test_Automation.yaml`

**추가할 위치:** 파일 맨 끝 (deploy job 이후)

```yaml
  # 기존 코드 끝에 추가

  notify_slack:
    needs: [ui_tests, api_tests, deploy]
    runs-on: ubuntu-latest
    if: always()  # 실패해도 알림 보냄
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"

      - name: Install Dependencies
        run: |
          python -m pip install requests

      - name: Download UI Test Results
        uses: actions/download-artifact@v3
        with:
          name: ui-test-results
          path: .
        continue-on-error: true

      - name: Download API Test Results
        uses: actions/download-artifact@v3
        with:
          name: api-test-results
          path: .
        continue-on-error: true

      - name: Send Slack Notification
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
          GITHUB_RUN_ID: ${{ github.run_id }}
          BRANCH_NAME: ${{ github.ref_name }}
        run: |
          python utils/send_slack_result.py
```

### 2. Artifact 저장 추가

**ui_tests job에 추가:**

```yaml
  ui_tests:
    runs-on: ubuntu-latest
    steps:
      # ... 기존 steps ...

      - name: Upload UI Test Results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: ui-test-results
          path: ui_report.xml
```

**api_tests job에 추가:**

```yaml
  api_tests:
    runs-on: ubuntu-latest
    steps:
      # ... 기존 steps ...

      - name: Upload API Test Results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: api-test-results
          path: api_report.xml
```

---

## 간단한 버전 (Slack Action 사용)

더 간단하게 하려면 Slack GitHub Action 사용:

```yaml
  notify_slack_simple:
    needs: [ui_tests, api_tests, deploy]
    runs-on: ubuntu-latest
    if: always()
    steps:
      - name: Slack Notification
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          text: |
            테스트 완료!
            UI 테스트: ${{ needs.ui_tests.result }}
            API 테스트: ${{ needs.api_tests.result }}
            Report: https://yoplekiller.github.io/QATEST/
          webhook_url: ${{ secrets.SLACK_WEBHOOK_URL }}
        if: always()
```

---

## 테스트 방법

### 로컬에서 테스트:

```bash
cd /c/Users/tbell/QATEST

# 환경변수 설정
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
export GITHUB_RUN_ID="local-test"
export BRANCH_NAME="test"

# 테스트 실행 (XML 파일 생성)
pytest src/tests/api --junitxml=api_report.xml
pytest src/tests/ui --junitxml=ui_report.xml

# Slack 알림 전송 테스트
python utils/send_slack_result.py
```

성공하면 Slack에 메시지가 옵니다!

---

## 트러블슈팅

### 1. "SLACK_WEBHOOK_URL이 설정되지 않았습니다"
→ GitHub Secrets에 SLACK_WEBHOOK_URL 추가

### 2. "Slack 전송 실패: 404"
→ Webhook URL이 잘못됨, Slack에서 다시 생성

### 3. "ui_report.xml을 찾을 수 없습니다"
→ Artifact 다운로드 단계가 필요함

### 4. 메시지가 이상하게 나옴
→ `send_slack_result.py`의 메시지 포맷 수정

---

## 참고 사항

- **비용:** Slack Incoming Webhooks는 무료
- **빈도:** 테스트 실행할 때마다 알림 (8시간마다 + 푸시할 때)
- **채널:** 전용 채널 만드는 것 추천 (#test-automation)

---

## 완료 체크리스트

- [ ] Slack App 생성
- [ ] Incoming Webhook 활성화
- [ ] Webhook URL 복사
- [ ] GitHub Secrets에 SLACK_WEBHOOK_URL 등록
- [ ] GitHub Actions 워크플로우 수정
- [ ] Artifact 업로드/다운로드 추가
- [ ] Git commit & push
- [ ] GitHub Actions 실행 확인
- [ ] Slack 메시지 수신 확인

완료하면 85점 → 88점! 🎉
