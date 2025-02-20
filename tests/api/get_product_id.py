from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from selenium.webdriver.common.by import By
from project.browser_action import search_product


def get_product_id():
    options = Options()
    options.add_argument("--headless")  # GUI 없는 환경에서 실행
    options.add_argument("--no-sandbox")  # 샌드박스 비활성화 (GitHub Actions용)
    options.add_argument("--disable-dev-shm-usage")  # 메모리 문제 방지
    options.add_argument(f"--usdocker stop $(docker ps -q)er-data-dir={os.getcwd()}/selenium_profile")  # 충돌 방지
    options.add_argument("--remote-debugging-port=9222")  # 디버깅 포트 추가


    service = Service("/usr/bin/chromedriver")  # ChromeDriver 경로 지정
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://www.kurly.com/main")
    search_product(driver,"콜라")
    driver.find_element(By.ID," //div[@class='css-11kh0cw e1oh2pka5']//a[1]")

    driver.quit()
