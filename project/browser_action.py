from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from project.utilities import take_screenshot


# 초기화
def initialize_browser():
    #chrome 브라우저 초기화
    service_obj = Service(r"C:\Users\jmlim\Desktop\chromedriver-win32\chromedriver.exe")
    driver = webdriver.Chrome(service=service_obj)  # Chrome WebDriver 초기화
    driver.maximize_window()
    driver.implicitly_wait(10)
    return driver

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



