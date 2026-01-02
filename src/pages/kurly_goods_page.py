"""
Kurly 상품 상세 팝업 Page Object
마켓컬리 웹사이트의 상품 상세 팝업 기능을 담당하는 페이지 오브젝트
"""
from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage


class KurlyGoodsPage(BasePage):
    """
    마켓컬리 상품 상세 팝업 객체

    기능:
        - 상품 상세 정보 확인
        - 수량 조절 (팝업 내)
        - 장바구니 담기 (팝업 내)
    """
    #URL
    GOODS_URL = "https://www.kurly.com/goods/{good_id}"

    GOODS_ITEMS = (By.XPATH, "//div[contains(@class,'goods-card')]")
    GOODS_TITLE = (By.XPATH, ".//span[contains(@class,'goods-name')]")
    GOODS_PRICE = (By.XPATH, ".//span[contains(@class,'goods-price')]")

    # Locators - 상품 상세 팝업
    GOODS_DETAIL_POPUP = (By.XPATH, "//div[contains(@class,'goods-detail-modal')]")
    GOODS_TITLE = (By.XPATH, "//h1[contains(@class,'goods-name')]")
    GOODS_PRICE = (By.XPATH, "//span[contains(@class,'goods-price')]")

    # Locators - 수량 조절 (팝업 내)
    QUANTITY_INPUT = (By.XPATH, "//input[@type='number']")
    QUANTITY_UP_BUTTON = (By.XPATH, "//button[@aria-label='수량올리기']")
    QUANTITY_DOWN_BUTTON = (By.XPATH, "//button[@aria-label='수량내리기']")

    # Locators - 장바구니 담기 버튼 (팝업 내)
    ADD_TO_CART_BUTTON_IN_POPUP = (By.XPATH, "//button[@class='css-ahkst0 e4nu7ef3']")
    ADD_TO_CART_CONFIRM = (By.XPATH, "//button[contains(text(),'장바구니')]")

    

    def __init__(self, driver):
        super().__init__(driver)

    def increase_quantity(self, times: int = 1) -> None:
        """
        상품 상세 팝업에서 수량 올리기

        Args:
            times: 클릭 횟수 (기본값: 1)
        """
        for _ in range(times):
            self.click(self.QUANTITY_UP_BUTTON)

    def decrease_quantity(self, times: int = 1) -> None:
        """
        상품 상세 팝업에서 수량 내리기

        Args:
            times: 클릭 횟수 (기본값: 1)
        """
        for _ in range(times):
            self.click(self.QUANTITY_DOWN_BUTTON)

    def get_quantity(self) -> int:
        """
        현재 선택된 수량 반환

        Returns:
            int: 현재 수량
        """
        quantity_text = self.get_attribute(self.QUANTITY_INPUT, "value")
        try:
            return int(quantity_text)
        except (ValueError, TypeError):
            return 0

    def click_add_to_cart_in_popup(self) -> None:
        """상품 상세 팝업에서 '장바구니 담기' 버튼 클릭"""
        self.click(self.ADD_TO_CART_BUTTON_IN_POPUP)


    def is_popup_displayed(self) -> bool:
        """
        상품 상세 팝업이 표시되는지 확인

        Returns:
            bool: 팝업이 표시되면 True
        """
        return self.is_displayed(self.GOODS_DETAIL_POPUP, timeout=3)

    def get_good_name(self) -> str:
        """
        팝업에 표시된 상품명 반환

        Returns:
            str: 상품명
        """
        return self.get_text(self.GOODS_NAME)

    def get_good_price(self) -> str:
        """
        팝업에 표시된 상품 가격 반환

        Returns:
            str: 상품 가격
        """
        return self.get_text(self.GOODS_PRICE)
    
    def click_first_search_result(self) -> None:
        """검색 결과에서 첫 번째 상품 클릭"""
        self.click_first_good()
