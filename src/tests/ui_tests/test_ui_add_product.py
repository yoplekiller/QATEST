import time
import allure
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from utils.utilities import FailureScreenshot, capture_screenshot

@allure.feature("UI 테스트")
@allure.story("상품 추가 테스트")
@allure.title("상품 검색 후 장바구니 추가 기능 동작 확인")
def test_add_product(driver):
    driver.get("https://www.kurly.com/main")
    driver.maximize_window()

    wait = WebDriverWait(driver, 10)

    with FailureScreenshot(driver, "상품추가", "screenshots_add_product"):
        # 검색
        search_box = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='검색어를 입력해주세요']")))
        search_box.send_keys("과자")
        search_box.send_keys(Keys.RETURN)
        time.sleep(4)
        
        # 상품 추가
        add_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[3]//div[2]//button[1]")))
        add_button.click()
        time.sleep(1)
        
        # 수량 올리기
        quantity_up_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='수량올리기']")))
        for _ in range(2):
            quantity_up_button.click()
        time.sleep(1)
        
        # 수량 내리기
        quantity_down_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='수량내리기']")))
        for _ in range(2):
            quantity_down_button.click()
        time.sleep(1)
        
        # 장바구니 담기
        cart_add_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='css-ahkst0 e4nu7ef3']")))
        cart_add_button.click()
        time.sleep(2)
        
        # 결과 확인
        assert "과자" in driver.page_source, "❌ 검색 결과에서 '과자'가 포함되지 않음"
        
        print("🎉 상품 추가 테스트 성공!")