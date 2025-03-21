FROM python:3.13

# 필수 패키지 설치
RUN apt-get update && apt-get install -y wget unzip curl jq

# Google Chrome 설치
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor > /usr/share/keyrings/google-chrome-keyring.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/google-chrome-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" | tee /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable

# Selenium 및 WebDriver Manager 설치
RUN pip install selenium pytest pytest-html webdriver-manager openpyxl

# 작업 디렉토리 설정
WORKDIR /app

# 테스트 코드 복사 (src/tests/ui_tests 포함)
COPY . /app

# WebDriver Manager를 사용하여 ChromeDriver 자동 설치 후 실행
CMD bash -c "pytest src/tests/ui_tests --alluredir=allure-results/docker || true"

