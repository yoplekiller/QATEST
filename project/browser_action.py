from selenium.common import NoSuchElementException, WebDriverException
from selenium.webdriver.common.by import By
from project.utilities import take_screenshot



#검색
def search_product(driver, product_name):
    try:
       search_box = driver.find_element(By.ID, "gnb_search") #검색창
       search_box.send_keys(product_name) #검색어 입력
       search_button = driver.find_element(By.ID,"submit") #검색 버튼
       search_button.click() # 검색버튼 클릭

    except (NoSuchElementException, WebDriverException) as e:
        take_screenshot(driver, f"error_search_{product_name}")
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

def click_category_sort_option(driver, option_text):
    """
    정렬 옵션 클릭
    :param driver: WebDriver 객체
    :param option_text: 정렬 옵션 텍스트 (예: '높은 가격순')
    """
    sort_button = driver.find_element(By.XPATH, f"//span[contains(text(),'{option_text}')]")
    sort_button.click()



