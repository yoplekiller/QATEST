"""
Kurly 장바구니 페이지 Page Object
마켓컬리 웹사이트의 장바구니 기능을 담당하는 페이지 오브젝트
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from src.pages.base_page import BasePage


class KurlyCartPage(BasePage):
    """
    마켓컬리 장바구니 페이지 객체

    기능:
        - 장바구니 접근
        - 수량 조절
        - 장바구니 상태 확인
    """

    # URL
    CART_URL = "https://www.kurly.com/cart"

    # Locators - 장바구니 버튼
    CART_ICON = (By.CSS_SELECTOR, ".css-1e2hf7q.eebvnww2")
    CART_TITLE = (By.XPATH, "//h1[normalize-space()='장바구니']")

    # Locators - 수량 조절
    QUANTITY_UP_BUTTON = (By.CSS_SELECTOR, "svg[width='13.333'][height='13.333']")
    QUANTITY_DOWN_BUTTON = (By.CSS_SELECTOR, "svg[width='13.333'][height='20']")

    # Locators - 버튼
    DELETE_BUTTON = (By.XPATH, "//button[normalize-space()='선택삭제']")
    LOGIN_IN_CART = (By.XPATH, "//button[contains(text(),'로그인')]")

    # Locators - 메시지
    EMPTY_CART_MESSAGE = (By.XPATH, "//*[contains(text(),'장바구니가 비어')]")

    def __init__(self, driver):
        super().__init__(driver)

    def click_cart_icon(self):
        """장바구니 아이콘 클릭"""
        # 팝업이 있으면 제거
        self.driver.execute_script("""
            const el = document.querySelector('.css-5ojige');
            if (el) el.style.display = 'none';
        """)

        self.click(self.CART_ICON)

        # URL 변경 대기
        self.wait_until_url_contains("cart")

    def open_cart_page(self):
        """장바구니 페이지 열기"""
        self.open(self.CART_URL)

    def wait_until_url_contains(self, text, timeout=10):
        """URL에 특정 텍스트가 포함될 때까지 대기"""
        WebDriverWait(self.driver, timeout).until(
            EC.url_contains(text)
        )

    def increase_quantity(self, times=1):
        """수량 증가"""
        self.change_quantity(self.QUANTITY_UP_BUTTON, times)

    def decrease_quantity(self, times=1):
        """수량 감소"""
        self.change_quantity(self.QUANTITY_DOWN_BUTTON, times)

    def is_on_cart_page(self):
        """장바구니 페이지에 있는지 확인"""
        current_url = self.get_current_url()
        return any(keyword in current_url.lower() for keyword in ["cart", "basket"])

    def has_kurly_in_title(self):
        """페이지 제목에 '컬리'가 포함되어 있는지 확인"""
        return "컬리" in self.get_title()
