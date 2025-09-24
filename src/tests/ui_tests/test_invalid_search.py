import allure
import pytest
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.utilities import capture_screenshot
from config.constants import URLs, Timeouts, Selectors, PopupSelectors,ErrorMessages


@allure.feature("UI 테스트")
@allure.story("검색 실패 케이스")
@allure.title("존재하지 않는 상품 검색 시, 결과 없음 메시지 확인")
def test_search_invalid_product(driver):
    driver.get(URLs.KURLY_MAIN)
    driver.maximize_window()

    try:
        search_box = WebDriverWait(driver, Timeouts.MEDIUM).until(EC.element_to_be_clickable(Selectors.SEARCH_BOX))
        search_box.send_keys("ㅁㄴㅇㄹ")
        search_box.send_keys(Keys.RETURN)
        driver.implicitly_wait(Timeouts.MEDIUM)
 
    except Exception as e:
        capture_screenshot(driver, "검색 실행 실패", "search_box_error")
        pytest.fail(f"❌ 검색 입력 중 오류: {str(e)}")

    try:
        error_msg = driver.find_element(*ErrorMessages.ERROR_MSG)
        assert error_msg.is_displayed()
    except Exception as e:
        capture_screenshot(driver, "결과 메시지 확인 실패", "no_result_msg_error")
        pytest.fail(f"❌ 결과 메시지 미노출 또는 실패: {str(e)}")
