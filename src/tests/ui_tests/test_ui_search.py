import allure
import pytest
from selenium.webdriver import Keys
import time
from utils.excel_reader import read_search_terms_from_excel, file_path
from selenium.webdriver.common.by import By
from utils.utilites import capture_screenshot


search_cases = read_search_terms_from_excel(file_path)

@allure.feature("UI 테스트")
@allure.story("상품 검색 테스트")
@pytest.mark.parametrize("tc_id, search_term", search_cases)
def test_product_search(driver, tc_id, search_term):
    print(f"🔍 TC {tc_id}: '{search_term}' 검색 테스트 실행 중...")

    driver.get("https://www.kurly.com/main")
    try:
        search_box = driver.find_element(By.XPATH, "//input[@placeholder='검색어를 입력해주세요']")
        time.sleep(2)
        for _ in range(10):
            search_box.send_keys(Keys.BACKSPACE)

        search_box.send_keys(search_term)
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)

    except Exception as e:
        capture_screenshot(driver, f"{tc_id}_{search_term}", 'screenshots_Search')
        pytest.fail(f"❌ 검색 실패: {str(e)}")















