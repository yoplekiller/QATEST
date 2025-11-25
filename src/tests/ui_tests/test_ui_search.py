import allure
import pytest
from selenium.webdriver import Keys
from utils.read_product_data import read_search_terms_from_excel, file_path
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.utilities import FailureScreenshot


search_cases = read_search_terms_from_excel(file_path)


@allure.feature("UI 테스트")
@allure.story("상품 검색 테스트")
@allure.title("입력된 상품명으로 검색 시 검색되는지 확인")
@pytest.mark.parametrize("tc_id, search_term", search_cases)
def test_product_search(driver, tc_id, search_term):

    driver.get("https://www.kurly.com/main")
    driver.maximize_window()

    wait = WebDriverWait(driver, 10)

    with FailureScreenshot(driver, f"검색_{tc_id}_{search_term}", "screenshots_Search"):

        print(f"🔍 TC {tc_id}: '{search_term}' 검색 테스트 실행 중...")

       
        search_box = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='검색어를 입력해주세요']"))
        )

        search_box.clear()
        search_box.send_keys(search_term)
        search_box.send_keys(Keys.RETURN)


        product_elements = wait.until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//span[contains(@class,'css-1qfsi3d')]")
            )
        )

        
        assert len(product_elements) > 0, f"❌ 검색어 '{search_term}'에 대한 검색 결과가 없음."

        print(f"✅ '{search_term}' 검색 성공 - 총 {len(product_elements)}개 검색됨")
