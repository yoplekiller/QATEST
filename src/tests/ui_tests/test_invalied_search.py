import allure
import pytest
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.utilities import FailureScreenshot


@allure.feature("UI 테스트")
@allure.story("검색 실패 케이스")
@allure.title("존재하지 않는 상품 검색 시, 결과 없음 메시지 확인")
def test_search_invalid_product(driver):

    driver.get("https://www.kurly.com/main")
    driver.maximize_window()

    wait = WebDriverWait(driver, 10)

    with FailureScreenshot(driver, "존재하지않는상품검색", "screenshots_invalid_search"):
        search_box = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='검색어를 입력해주세요']"))
        )
        search_box.send_keys("ㅁㄴㅇㄹ")   # 존재하지 않는 검색어
        search_box.send_keys(Keys.RETURN)

        # 검색 결과 없음 메시지 대기
        error_msg = wait.until(
            EC.visibility_of_element_located((
                By.XPATH,
                "//div[contains(text(), '검색 결과가 없')] | "
                "//div[contains(text(), '상품이 없')] | "
                "//div[contains(text(), '결과 없음')]"
            ))
        )

        message_text = error_msg.text.strip()
        assert any(keyword in message_text for keyword in ["검색 결과가 없", "상품이 없", "결과 없음"]), \
            f"❌ 예상하지 못한 메시지: {message_text}"

        print(f"✅ 무효한 검색 결과 메시지 확인됨: {message_text}")
