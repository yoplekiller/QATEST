import pytest
import allure
from selenium.webdriver.common.by import By
from utils.utilities import capture_screenshot
from config.constants import URLs, Timeouts, Selectors, PopupSelectors


@allure.feature("UI 테스트")
@allure.story("검색창 FAILED 테스트")
@allure.title("FAILED 기능 동작 하는지 확인")
def test_fail_screenshot(driver):
    """
    일부러 실패하게 만드는 테스트
    - 올바르지 않은 요소 선택
    - 검색창이 없는 요소를 클릭 시도하여 실패 유발
    """
    driver.get(URLs.KURLY_MAIN)
    try:
        driver.find_element(By.XPATH, "//input[@id='wrong_search_id']").click()
    except Exception:
        pytest.fail("📌 예상된 실패: 잘못된 XPATH로 인해 클릭할 수 없음")