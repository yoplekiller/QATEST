import time
import allure
import pytest
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.utilities import FailureScreenshot

@allure.feature("UI 테스트")
@allure.story("검색 실패 케이스")
@allure.title("공백 입력 시, 팝업 노출 확인")
def test_search_invalid_product(driver):
    driver.get("https://www.kurly.com/main")
    driver.maximize_window()

    wait = WebDriverWait(driver, 10)

    with FailureScreenshot(driver, "공백검색", "screenshots_blank_search"):
        search_box = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//input[@placeholder='검색어를 입력해주세요']")
        ))
        search_box.send_keys("")  # 공백 검색
        search_box.send_keys(Keys.RETURN)
        time.sleep(4)


        popup = wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//div[contains(@class, 'popup-content')]")
        ))
        
        # 팝업 텍스트 확인
        popup_text = popup.text
        assert "검색어를 입력해주세요" in popup_text, f"❌ 예기치 않은 팝업 메시지: {popup_text}"
        
        print("✅ 공백 검색 시 팝업 정상 표시됨")
