FROM python:3.13

WORKDIR /app

RUN apt-get update && apt-get install -y \
    wget unzip curl \
    xvfb libxi6 libgconf-2-4 \
    libnss3 libxss1 libappindicator3-1\
    fonts-liberation libasound2 libnspr4 libnss3 \
    libx11-xcb1 libxcomposite1 libxcursor1 libxdamage1 libxfixes3 \
    libxrandr2 libxrender1 libgtk-3-0 libgbm1

# Chrome 설치
RUN wget -O /tmp/chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y /tmp/chrome.deb && rm /tmp/chrome.deb

# ChromeDriver 설치
RUN CHROME_DRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE) && \
    wget -q "https://chromedriver.storage.googleapis.com/${CHROME_DRIVER_VERSION}/chromedriver_linux64.zip" -O /tmp/chromedriver.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["pytest", "src/tests/ui_tests", "--html=ui_test_report.html", "--self-contained-html", "/dev/null"]
