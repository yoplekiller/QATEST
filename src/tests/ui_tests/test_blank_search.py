import time
import allure
import pytest
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from utils.utilities import capture_screenshot

@allure.feature("UI 테스트")
@allure.story("검색 실패 케이스")
@allure.title("공백 입력 시, 팝업 노출 확인")
def test_search_invalid_product(driver):
    driver.get("https://www.kurly.com/main")
    driver.maximize_window()

    try:
        search_box = driver.find_element(By.XPATH, "//input[@placeholder='검색어를 입력해주세요']")
        search_box.send_keys("")  # 존재하지 않는 검색어 입력
        search_box.send_keys(Keys.RETURN)
        time.sleep(4)

        try:
            popup = driver.find_element(By.XPATH, "//div[@class='popup-content css-15yaaju e1k5padi2']")
            assert popup.is_displayed(), "❌ 팝업이 표시되지 않았습니다."

            # 팝업 텍스트 확인
            popup_text = popup.text
            assert "검색어를 입력해주세요" in popup_text, f"❌ 예기치 않은 팝업 메시지: {popup_text}"

        except Exception as e:
            capture_screenshot(driver, "팝업 미노출", "screenshot_popup_not_found")
            pytest.fail(f"❌ 팝업 확인 실패: {str(e)}")

    except Exception as e:
        capture_screenshot(driver, "예외 발생", "screenshot_invalid_search_exception")
        pytest.fail(f"❌ 예외 발생: {str(e)}")
