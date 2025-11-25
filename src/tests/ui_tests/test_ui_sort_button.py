import allure
import pytest
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.utilities import FailureScreenshot


@allure.feature("UI 테스트")
@allure.story("카테고리 기능 테스트")
@allure.title("상품 검색 후 카테고리 정렬 버튼들이 정상 동작하는지 확인")
def test_ui_sort_button(driver):
    driver.get("https://www.kurly.com/main")
    driver.maximize_window()

    wait = WebDriverWait(driver, 10)

    with FailureScreenshot(driver, "카테고리버튼", "screenshots_category"):

        # 🔍 검색
        search_box = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='검색어를 입력해주세요']"))
        )
        search_box.send_keys("과자")
        search_box.send_keys(Keys.RETURN)

        # 🔎 검색 결과 로딩 기다림
        wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "div.css-11kh0cw.e1oh2pka5")
        ))

        # 🔧 카테고리별 정렬 테스트 함수
        def click_and_verify_category(category_name):

            # 정렬 전 첫 번째 상품 텍스트 저장
            first_item_before = wait.until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "div.css-11kh0cw.e1oh2pka5 a:nth-child(1)")
                )
            ).text.strip()

            # 카테고리 버튼 클릭
            category_button = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, f"//a[contains(text(), '{category_name}')]")
                )
            )
            category_button.click()

            # 정렬 후 첫 번째 상품 텍스트 다시 읽기
            first_item_after = wait.until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "div.css-11kh0cw.e1oh2pka5 a:nth-child(1)")
                )
            ).text.strip()

            # 검증
            assert first_item_before != first_item_after, \
                f"❌ '{category_name}' 클릭 후 상품 정렬이 적용되지 않음"

            print(f"✅ '{category_name}' 정렬 테스트 성공")

        # 실제 정렬 기준 목록
        categories = [
            "낮은 가격순",
            "높은 가격순",
            "판매량순",
            "혜택순",
            "신상품순",
            "추천순",
        ]

        for category_name in categories:
            click_and_verify_category(category_name, category_name)

        print("🎉 전체 카테고리 정렬 테스트 성공!")
