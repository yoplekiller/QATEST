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
        search_box.send_keys("ㅁㄴㅇㄹ")
        search_box.send_keys(Keys.RETURN)
        time.sleep(4)
    except Exception as e:
        capture_screenshot(driver, "검색 실행 실패", "search_box_error")
        pytest.fail(f"❌ 검색 입력 중 오류: {str(e)}")

    try:
        error_msg = driver.find_element(By.XPATH,"//div[@class='css-1d3w5wq e1oh2pka6']")
        assert error_msg.is_displayed()
    except Exception as e:
        capture_screenshot(driver, "결과 메시지 확인 실패", "no_result_msg_error")
        pytest.fail(f"❌ 결과 메시지 미노출 또는 실패: {str(e)}")
