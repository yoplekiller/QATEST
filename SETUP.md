# 환경 설정 가이드 (Setup Guide)

## 📋 목차
1. [필수 요구사항](#필수-요구사항)
2. [환경 변수 설정](#환경-변수-설정)
3. [의존성 설치](#의존성-설치)
4. [테스트 실행](#테스트-실행)
5. [문제 해결](#문제-해결)

---

## 📦 필수 요구사항

### 소프트웨어
- Python 3.11 이상
- pip (Python 패키지 관리자)
- Git
- Chrome 브라우저 (UI 테스트용)
- Android Studio / Appium (Mobile 테스트용, 선택사항)

---

## 🔐 환경 변수 설정

### 1. `.env` 파일 생성

프로젝트 루트에 `.env` 파일을 생성하세요:

```bash
cp .env.example .env
```

### 2. `.env` 파일 편집

다음 내용을 실제 값으로 수정하세요:

```bash
# TMDB API Configuration
TMDB_API_KEY=your_actual_api_key_here

# Kurly Test Account (for testing purposes only)
KURLY_TEST_USERNAME=your_test_username
KURLY_TEST_PASSWORD=your_test_password

# Slack Webhook (optional)
SLACK_WEBHOOK_URL=your_slack_webhook_url

# Test Environment
TEST_ENV=dev
```

### 3. API 키 발급 방법

#### TMDB API 키 (필수)
1. [The Movie Database](https://www.themoviedb.org/) 회원가입
2. 계정 설정 → API → API 키 신청
3. 발급받은 키를 `.env` 파일에 입력

#### Slack Webhook (선택사항)
1. [Slack API](https://api.slack.com/apps) 접속
2. 새 앱 생성 → Incoming Webhooks 활성화
3. Webhook URL 복사하여 `.env` 파일에 입력

---

## 📥 의존성 설치

### 1. 가상환경 생성 (권장)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 2. 패키지 설치

```bash
pip install -r requirements.txt
```

### 3. ChromeDriver 설치 (자동)

프로젝트는 `webdriver-manager`를 사용하여 자동으로 ChromeDriver를 다운로드합니다.

---

## 🚀 테스트 실행

### 전체 테스트 실행

```bash
pytest --alluredir=./allure-results
```

### 특정 테스트 스위트 실행

```bash
# API 테스트만 실행
pytest src/tests/api_tests --alluredir=./allure-results

# UI 테스트만 실행
pytest src/tests/ui_tests --alluredir=./allure-results

# Mobile 테스트만 실행
pytest src/tests/mobile_tests --alluredir=./allure-results
```

### 특정 테스트 파일 실행

```bash
pytest src/tests/api_tests/test_popular_movie.py -v
```

### Allure 리포트 생성 및 확인

```bash
# 리포트 생성 및 자동 브라우저 열기
allure serve ./allure-results
```

---

## 🛠 문제 해결

### 1. 환경변수 로드 오류

**증상:**
```
❌ TMDB API 키가 설정되지 않았습니다.
```

**해결방법:**
- `.env` 파일이 프로젝트 루트에 있는지 확인
- `.env` 파일에 `TMDB_API_KEY` 값이 올바르게 설정되어 있는지 확인
- 파일 인코딩이 UTF-8인지 확인

### 2. 테스트 계정 오류

**증상:**
```
❌ 테스트 계정 정보가 설정되지 않았습니다.
```

**해결방법:**
- `.env` 파일에 `KURLY_TEST_USERNAME`과 `KURLY_TEST_PASSWORD` 설정
- 계정 정보에 공백이나 특수문자가 있다면 따옴표로 감싸기:
  ```bash
  KURLY_TEST_USERNAME="user@example.com"
  ```

### 3. ChromeDriver 오류

**증상:**
```
SessionNotCreatedException: Could not start a new session
```

**해결방법:**
```bash
# ChromeDriver 캐시 삭제
pip uninstall webdriver-manager
pip install webdriver-manager
```

### 4. Allure 설치 오류 (macOS/Linux)

```bash
# macOS (Homebrew)
brew install allure

# Ubuntu/Debian
sudo apt-add-repository ppa:qameta/allure
sudo apt-get update
sudo apt-get install allure
```

---

## 🔒 보안 주의사항

1. **절대** `.env` 파일을 Git에 커밋하지 마세요
2. API 키나 계정 정보를 코드에 직접 작성하지 마세요
3. 공개 저장소에 업로드 전 민감한 정보 확인:
   ```bash
   git log --all --full-history -- .env
   ```
4. 실수로 커밋한 경우 즉시 API 키 재발급

---

## 📞 추가 도움말

- GitHub Issues: 프로젝트 저장소에 이슈 등록
- 문서: [README.md](./README.md) 참고
