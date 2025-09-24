import allure
import pytest
from selenium.webdriver import Keys
import time
from utils.read_product_data import read_search_terms_from_excel, file_path
from selenium.webdriver.common.by import By
from utils.utilities import capture_screenshot
from config.constants import URLs, Timeouts, Selectors, PopupSelectors,ErrorMessages, Buttons

search_cases = read_search_terms_from_excel(file_path)

@allure.feature("UI 테스트")
@allure.story("상품 검색 테스트")
@allure.title("입력된 상품명으로 검색 시 검색되는지 확인" )
@pytest.mark.parametrize("tc_id, search_term", search_cases)
def test_product_search(driver, tc_id, search_term):
    driver.get(URLs.KURLY_MAIN)
    time.sleep(2)
    print(f"🔍 TC {tc_id}: '{search_term}' 검색 테스트 실행 중...")

    try:
        search_box = driver.find_element(*Selectors.SEARCH_BOX)
        time.sleep(2)
        for _ in range(10):
            search_box.send_keys(Keys.BACKSPACE)

        search_box.send_keys(search_term)
        search_box.send_keys(Keys.RETURN)
        time.sleep(4)

        product_elements = driver.find_elements(By.XPATH,"//span[@class='css-1qfsi3d e1yof8003']")
        assert len(product_elements) > 0, f"❌ 검색어 '{search_term}'에 대한 검색 결과가 없음."

        capture_screenshot(driver, f"{tc_id}_{search_term}_success", f"screenshot_search_term")

    except Exception as e:
        capture_screenshot(driver, f"{tc_id}_{search_term}_failed", 'screenshots_Search')
        pytest.fail(f"❌ 검색 실패: {str(e)}")















