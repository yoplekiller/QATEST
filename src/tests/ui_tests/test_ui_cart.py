import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.utilities import FailureScreenshot


@allure.feature("UI 테스트")
@allure.story("장바구니 화면 체크 테스트")
@allure.title("장바구니 버튼이 동작 하는지 확인")
def test_cart(driver):

    driver.get("https://www.kurly.com/main")
    driver.maximize_window()

    wait = WebDriverWait(driver, 10)

    with FailureScreenshot(driver, "장바구니", "screenshots_cart"):
        driver.execute_script("""
        const el = document.querySelector('.css-5ojige');
        if (el) el.style.display = 'none';
    """)

        cart_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@class='css-1o9e4kz']//*[name()='svg']"))
        )

        wait.until(
            EC.visibility_of(cart_button)
        )

        cart_button.click()

        # URL 변경까지 기다리기
        wait.until(
            EC.url_contains("cart")
        )

        current_url = driver.current_url    
        print(f"현재 URL: {current_url}")

        # 더 다양한 케이스 체크
        assert any(keyword in current_url.lower() 
                   for keyword in ["cart", "basket"]), "❌ 장바구니 페이지가 아닙니다."

        assert "컬리" in driver.title, "❌ 컬리 페이지 제목이 다릅니다."

        print("🎉 테스트 성공! (실패했을 때만 자동 스크린샷 저장)")
