import allure
import time
import pytest
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from utils.utilities import capture_screenshot


@allure.feature("UI 테스트")
@allure.story("상품 검색")
@allure.title("검색창에서 '과자' 검색 기능 동작 확인")
def test_search_product(driver):
    driver.get("https://www.kurly.com/main")
    driver.maximize_window()

    try:
        search_box = driver.find_element(By.XPATH, "//input[@placeholder='검색어를 입력해주세요']")
        search_box.send_keys("과자")
        search_box.send_keys(Keys.RETURN)
        time.sleep(4)
        assert "과자" in driver.page_source

    except Exception as e:
        capture_screenshot(driver, "상품검색 실패", "screenshot_search")
        pytest.fail(f"❌ 검색 기능 실패: "
                    f"{str(e)}")

