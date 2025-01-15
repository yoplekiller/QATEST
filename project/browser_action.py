import os

import pytest
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from project.config import BASE_URL
from project.utilities import take_screenshot
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

@pytest.fixture
def initialize_browser():
    """WebDriver 초기화 및 종료"""
    if os.getenv("CI"):
        # CI 환경에서는 Selenium Grid 사용
        grid_url = "http://localhost:4444/wd/hub"
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        capabilities = DesiredCapabilities.CHROME.copy()
        driver = webdriver.Remote(command_executor=grid_url, options=options, desired_capabilities=capabilities)
    else:
        # 로컬 환경에서는 로컬 ChromeDriver 사용
        chrome_driver_path = r"C:\Users\jmlim\Desktop\chromedriver-win32\chromedriver.exe"
        service_obj = Service(chrome_driver_path)
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=service_obj, options=options)

    # 공통 설정
    driver.maximize_window()
    driver.implicitly_wait(10)

    # BASE_URL 가져오기
    base_url = os.getenv("BASE_URL", "https://www.kurly.com/main")  # 기본값 설정
    driver.get(base_url)
    yield driver
    driver.quit()

#검색
def search_product(driver, product_name):
    try:
       search_box = driver.find_element(By.ID, "gnb_search") #검색창
       search_box.send_keys(product_name) #검색어 입력
       search_button = driver.find_element(By.ID,"submit") #검색 버튼
       search_button.click() # 검색버튼 클릭
    except NotImplemented as e:
        take_screenshot(driver, "error_search")
        print(f"검색 에러: {e}")
        raise

#분류
def click_sort_option(driver, option_text):
    """
    정렬 옵션 클릭
    :param driver: WebDriver 객체
    :param option_text: 정렬 옵션 텍스트 (예: '높은 가격순')
    """
    sort_button = driver.find_element(By.XPATH, f"//a[contains(text(),'{option_text}')]")
    sort_button.click()

def click_price_sort_option(driver, option_text):
    """
    정렬 옵션 클릭
    :param driver: WebDriver 객체
    :param option_text: 정렬 옵션 텍스트 (예: '높은 가격순')
    """
    sort_button = driver.find_element(By.XPATH, f"//span[contains(text(),'{option_text}')]")
    sort_button.click()



