import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.ie.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 웹 실행
@pytest.fixture(scope="module")
def driver():
    chrome_options = Options()

    chrome_options.add_argument("--disable-dev-shm-usage") #메모리 부족 방지
    chrome_options.add_argument("--no-sandbox") #샌드박스 비활성화
    # chrome_options.add_argument("--headless") #GUI없는 환경에서도 실행 가능


    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service,options=chrome_options)

    driver.get("https://www.kurly.com/main")
    driver.maximize_window()
    driver.find_element(By.XPATH,"//input[@id='gnb_search']").click()
    driver.implicitly_wait(10)

    yield driver   # 테스트 실행

    driver.quit()  # 모든 테스트 완료 후 브라우저 종료s



