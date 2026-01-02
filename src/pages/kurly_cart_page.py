"""
Kurly 장바구니 페이지 Page Object
마켓컬리 웹사이트의 장바구니 기능을 담당하는 페이지 오브젝트
"""
from selenium.webdriver.common.by import By
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
    CART_ICON = (By.XPATH, "//button[@class='css-1e2hf7q eebvnww2']")  # 장바구니 아이콘
    CART_TITLE = (By.XPATH, "//h1[normalize-space()='장바구니']")

    # Locators - 수량 조절
    QUANTITY_UP_BUTTON = (By.CSS_SELECTOR, "svg[width='13.333'][height='13.333']")
    QUANTITY_DOWN_BUTTON = (By.CSS_SELECTOR, "svg[width='13.333'][height='20']")

    # Locators - 버튼
    DELETE_BUTTON = (By.XPATH, "//button[normalize-space()='선택삭제']")
    DELETE_SELECTED_BUTTON = (By.XPATH, "//button[contains(text(), '선택삭제')]")
    FIRST_ITEM_CHECKBOX = (By.XPATH, "(//input[@type='checkbox'])[2]")  # 첫 번째는 전체선택, 두 번째가 첫 상품
    LOGIN_IN_CART = (By.XPATH, "//button[contains(text(),'로그인')]")

    
    # Locators - 메시지
    EMPTY_CART_MESSAGE = (By.XPATH, "//*[contains(text(),'장바구니가 비어')]")

    # Locators - 수량 확인
    CART_ITEM_COUNT = (By.CSS_SELECTOR, "p.kpds_97oqoup")
    CART_QUANTITY_DISPLAY = (By.CSS_SELECTOR, "p.kpds_97oqoup")

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

    def change_quantity(self, button_locator, times=1):
        """수량 변경"""
        for _ in range(times):
            self.click(button_locator)
            self.sleep(0.5)  # UI 반영 대기

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
    
    def get_cart_item_count(self) -> int:
        """
        장바구니에 담긴 상품 종류 개수 반환 ('전체선택 */*'에서 뒤의 숫자)

        Returns:
            int: 장바구니 상품 종류 개수
        """
        element = self.find_element(self.CART_ITEM_COUNT, timeout=0.5)
        text = element.text  # 예: '전체선택 */*'
        try:
            # '*/ *'에서 뒤의 숫자만 추출
            count = int(text.split()[-1].split('/')[-1])
            return count
        except Exception:
            return 0

    def remove_first_item(self) -> None:
        """
        장바구니의 첫 번째 상품을 선택하여 삭제

        Steps:
            1. 첫 번째 상품 체크박스 선택
            2. 선택삭제 버튼 클릭
        """
        # 첫 번째 상품 체크박스 선택
        self.click(self.FIRST_ITEM_CHECKBOX)
        self.sleep(0.5)  # UI 반영 대기

        # 선택삭제 버튼 클릭
        self.click(self.DELETE_SELECTED_BUTTON)
        self.sleep(0.5)  # 삭제 처리 대기   

    def get_cart_kind_count_from_text(self) -> int:
        """
        '전체선택 2/2' 텍스트에서 전체 상품 종류 개수(2)를 추출
        """
        # 해당 <p> 요소를 찾음 (적절한 locator로 교체 필요)
        element = self.get_text(self.CART_ITEM_COUNT)
        text = element.text  # 예: "전체선택 2/2"
        try:
            # "2/2"에서 뒤의 숫자만 추출
            count = int(text.split()[-1].split('/')[-1])
            return count
        except Exception:
            return 0
        
    def get_cart_total_quantity(self) -> int:
        """
        장바구니에 담긴 상품 총 수량 반환 (각 상품별 수량 합산)

        Returns:
            int: 장바구니 상품 총 수량
        """
        # TODO: 실제 수량 표시 셀렉터 및 파싱 로직 구현 필요
        # 예시: 상품별 수량이 span.kpds_xxxxx에 있다면 모두 합산
        # elements = self.find_elements((By.CSS_SELECTOR, 'span.kpds_xxxxx'))
        # return sum(int(e.text) for e in elements if e.text.isdigit())
        return 0  # 실제 구현 필요

