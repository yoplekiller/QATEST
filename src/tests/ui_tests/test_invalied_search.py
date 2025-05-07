import time
import allure
import pytest
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from utils.utilities import capture_screenshot

@allure.feature("UI 테스트")
@allure.story("검색 실패 케이스")
@allure.title("존재하지 않는 상품 검색 시, 결과 없음 메시지 확인")
def test_search_invalid_product(driver):
    driver.get("https://www.kurly.com/main")
    driver.maximize_window()

    try:
        search_box = driver.find_element(By.XPATH, "//input[@placeholder='검색어를 입력해주세요']")
        search_box.send_keys("ㅁㄴㅇㄹ")  # 임의의 존재하지 않는 검색어
        search_box.send_keys(Keys.RETURN)
        time.sleep(4)

        if "검색된 상품이 없습니다.다른 검색어를 입력해 주세요." not in driver.page_source:
            capture_screenshot(driver, "검색 실패", "screenshot_invalid_search")
            pytest.fail("❌ '검색 결과 없음' 메시지가 노출되지 않음.")

    except Exception as e:
        capture_screenshot(driver, "예외 발생", "screenshot_invalid_search_exception")
        pytest.fail(f"❌ 예외 발생: {str(e)}")
