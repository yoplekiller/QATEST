import pytest
from selenium.webdriver import Keys
import time
from utils.excel_reader import read_search_terms_from_excel
from selenium.webdriver.common.by import By
from utils.utilites import capture_screenshot


search_cases = read_search_terms_from_excel(r"C:\Users\jmlim\Desktop\QA\AutoTest\utils\test_case.xlsx")

@pytest.mark.parametrize("tc_id, search_term", search_cases)
def test_product_search(driver, tc_id, search_term):
    print(f"🔍 TC {tc_id}: '{search_term}' 검색 테스트 실행 중...")


    search_box = driver.find_element(By.XPATH, "//input[@id='gnb_search']")
    time.sleep(2)
    for _ in range(10):
        search_box.send_keys(Keys.BACKSPACE)

    search_box.send_keys(search_term)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)

    capture_screenshot(driver, f"{tc_id}_{search_term}", 'screenshots_Search')




    # #검색 결과 검증
    # results = driver.find_elements(By.XPATH,//title[contains(text(), )
    # assert any(search_term in result.text for result in results), f"❌ {search_term} 검색 결과 없음!"
    #
    # print(f"✅ '{search_term}' 검색 테스트 통과!")






