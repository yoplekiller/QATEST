"""
Kurly 상품 페이지 Page Object
마켓컬리 상품 검색 결과 및 상품 상세 기능을 담당하는 페이지 오브젝트
"""
from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from src.pages.base_page import BasePage


class KurlyProductPage(BasePage):
    """
    마켓컬리 상품 페이지 객체

    기능:
        - 상품 검색
        - 상품 선택
        - 장바구니 담기
        - 수량 조절
    """
    #Product page URL
    URL = "https://www.kurly.com/shop/search.php"

    # Locators - 검색 결과 상품
    PRODUCT_LIST = (By.XPATH, "//a[@class='css-11geqae e1c07x4811']")
    FIRST_PRODUCT = (By.XPATH, "//a[1]//div[2]")
    THIRD_PRODUCT = (By.XPATH, "//a[3]//div[2]")

    # Locators - 상품 추가 버튼 (검색 결과에서)
    ADD_TO_CART_BUTTON_IN_LIST = (By.XPATH, "//a[3]//div[2]//button[1]")
    FIRST_ADD_BUTTON = (By.XPATH, "//a[1]//div[2]//button[1]")

    # Locators - 상품 상세 (팝업)
    PRODUCT_DETAIL_POPUP = (By.XPATH, "//div[contains(@class,'product-detail-modal')]")
    PRODUCT_NAME = (By.XPATH, "//h1[contains(@class,'product-name')]")
    PRODUCT_PRICE = (By.XPATH, "//span[contains(@class,'product-price')]")

    # Locators - 수량 조절 (팝업 내)
    QUANTITY_INPUT = (By.XPATH, "//input[@type='number']")
    QUANTITY_UP_BUTTON = (By.XPATH, "//button[@aria-label='수량올리기']")
    QUANTITY_DOWN_BUTTON = (By.XPATH, "//button[@aria-label='수량내리기']")

    # Locators - 장바구니 담기 버튼 (팝업 내)
    ADD_TO_CART_BUTTON_IN_POPUP = (By.XPATH, "//button[@class='css-ahkst0 e4nu7ef3']")
    ADD_TO_CART_CONFIRM = (By.XPATH, "//button[contains(text(),'장바구니')]")

    
    # Locators - 메시지
    SUCCESS_MESSAGE = (By.XPATH, "//*[contains(text(),'장바구니에 담았습니다')]")
    NO_RESULT_MESSAGE = (By.XPATH, "//*[contains(text(),'검색 결과가 없습니다')]")

    def __init__(self, driver):
        super().__init__(driver)

    def get_product_count(self) -> int:
        """
        상품 목록의 상품 개수 반환
        
        Returns:
            int: 검색 결과 상품 개수
        """
        products = self.find_elements(self.PRODUCT_LIST)
        return len(products)

    def get_products(self) -> List[WebElement]:
        """
        상품 목록 요소 반환
        
        Returns:
            List[WebElement]: 상품 요소 리스트
        """
        return self.find_elements(self.PRODUCT_LIST)

    def click_first_product_add_button(self) -> None:
        """첫 번째 상품의 장바구니 추가 버튼 클릭"""
        self.click(self.FIRST_ADD_BUTTON)

    def click_third_product_add_button(self) -> None:
        """세 번째 상품의 장바구니 추가 버튼 클릭"""
        self.click(self.ADD_TO_CART_BUTTON_IN_LIST)

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

    def add_product_to_cart_flow(self, increase_count: int = 0, decrease_count: int = 0) -> bool:
        #세번째 상품을 장바구니에 추가하는 플로우
        self.click_third_product_add_button()
        #   수량 증가
        if increase_count > 0:
            self.increase_quantity(increase_count)
            #수량 감소
        if decrease_count > 0:
            self.decrease_quantity(decrease_count)


        self.click_add_to_cart_in_popup()

         # 성공 메시지 확인 (선택)
        return self.is_add_to_cart_success()
    


    def is_add_to_cart_success(self) -> bool:
        """
        장바구니 담기 성공 메시지 표시 여부 확인

        Returns:
            bool: 성공 메시지가 표시되면 True
        """
        return self.is_displayed(self.SUCCESS_MESSAGE, timeout=5)



    def is_no_result_displayed(self) -> bool:
        """
        검색 결과 없음 메시지 표시 여부 확인

        Returns:
            bool: 메시지가 표시되면 True
        """
        return self.is_displayed(self.NO_RESULT_MESSAGE, timeout=3)

    def is_keyword_in_page_source(self, keyword: str) -> bool:
        """
        페이지 소스에 특정 키워드가 포함되어 있는지 확인

        Args:
            keyword: 확인할 키워드

        Returns:
            bool: 포함되어 있으면 True
        """
        return keyword in self.driver.page_source
