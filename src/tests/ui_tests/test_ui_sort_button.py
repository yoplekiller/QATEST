import allure
import pytest
from selenium.webdriver import Keys
import time
from selenium.webdriver.common.by import By
from utils.utilities import capture_screenshot
from config.constants import URLs, Timeouts, Selectors, PopupSelectors,ErrorMessages, Buttons


@allure.feature("UI 테스트")
@allure.story("카테고리 기능 테스트")
@allure.title("상품 검색 후 카테고리 버튼들이 동작하는지 확인")
def test_ui_sort_button(driver):
    driver.get(URLs.KURLY_MAIN)
    driver.maximize_window()

    try:
        # 검색어 입력
        search_box = driver.find_element(*Selectors.SEARCH_BOX)
        search_box.send_keys("과자")
        search_box.send_keys(Keys.RETURN)
        time.sleep(4)

        def click_and_verify_category(category_name, screenshot_name):
            try:

                first_item_selector = "div[class='css-11kh0cw e1oh2pka5'] a:nth-child(1)"
                first_item_before = driver.find_element(By.CSS_SELECTOR, first_item_selector).text


                category_button = driver.find_element(By.XPATH, f"//a[contains(text(), '{category_name}')]")
                category_button.click()
                time.sleep(4)


                first_item_after = driver.find_element(By.CSS_SELECTOR, first_item_selector).text


                assert first_item_before != first_item_after, f"❌ '{category_name}' 클릭 후 상품 화면이 바뀌지 않음"


                capture_screenshot(driver, screenshot_name, "screenshots_category")

            except Exception as e:
                capture_screenshot(driver, f"{screenshot_name}_실패", "screenshots_category")
                allure.attach(driver.get_screenshot_as_png(), name=f"{screenshot_name}_실패",
                              attachment_type=allure.attachment_type.PNG)
                pytest.fail(f"❌ '{category_name}' 테스트 실패: {str(e)}")

        categories = [
            ("낮은 가격순", "낮은가격순"),
            ("높은 가격순", "높은가격순"),
            ("판매량순", "판매량순"),
            ("혜택순", "혜택순"),
            ("신상품순", "신상품순"),
            ("추천순", "추천순"),
        ]
        for category_name, screenshot_name in categories:
            click_and_verify_category(category_name, screenshot_name)

    except Exception as e:
        capture_screenshot(driver, "카테고리_테스트실패", "screenshots_category")
        allure.attach(driver.get_screenshot_as_png(), name="카테고리_테스트실패",
                      attachment_type=allure.attachment_type.PNG)
        pytest.fail(f"❌ 카테고리 전체 테스트 실패: {str(e)}")