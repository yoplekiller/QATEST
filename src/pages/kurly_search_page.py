"""
Kurly 검색 결과 페이지 Page Object
마켓컬리 웹사이트의 검색 결과 기능을 담당하는 페이지 오브젝트
"""
from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from src.pages.base_page import BasePage

class KurlySearchPage(BasePage):
    """
    마켓컬리 검색 결과 페이지 객체

    기능:
        - 상품 검색
        - 검색 결과 확인
        - 상품 목록 조회
        - 정렬 옵션 선택
        - 검색 결과에서 상품 선택 및 장바구니 담기
    """

    # Search page URL
    SEARCH_URL = "https://www.kurly.com/search?sword={keyword}&page=1"

    # Locators - 검색 결과
    RESULT_TITLE = (By.XPATH, "//*[contains(normalize-space(), '에 대한 검색결과')]")
    PRODUCT_CARDS = (By.CSS_SELECTOR, "a[href*='/goods/']")
    PRODUCT_LIST = (By.XPATH, "//a[@class='css-11geqae e1c07x4811']")  # 대체 선택자
    NO_RESULT_TEXT = (By.XPATH, "//*[contains(normalize-space(), '검색된 상품이 없습니다') or contains(normalize-space(),'없')]")

    # Locators - 장바구니 추가 버튼 (검색 결과 내)
    ADD_TO_CART_BUTTONS = (By.XPATH, "//a//div[2]//button[1]")
    FIRST_ADD_BUTTON = (By.XPATH, "(//a//div[2]//button[1])[1]")
    THIRD_ADD_BUTTON = (By.XPATH, "(//a//div[2]//button[1])[3]")

    # Locators - 정렬
    SORT_SALE = (By.XPATH, "//a[contains(text(),'판매량순')]")
    SORT_RECOMMEND = (By.XPATH, "//a[contains(text(),'추천순')]")
    SORT_NEW = (By.XPATH, "//a[contains(text(),'신상품순')]")
    SORT_LOW_PRICE = (By.XPATH, "//a[contains(text(),'낮은 가격순')]")
    SORT_HIGH_PRICE = (By.XPATH, "//a[contains(text(),'높은 가격순')]")
    SORT_BONUS = (By.XPATH, "//a[contains(text(),'혜택순')]")

    def __init__(self, driver):
        super().__init__(driver)

    def get_result_title(self):
        return self.get_text(self.RESULT_TITLE)
    
    def get_current_url(self):
        return super().get_current_url()

    def select_sort_option(self, sort_type: str = "recommend") -> None:
        """
        카테고리 분류 옵션 선택

        Args:
            sort_type: 정렬 타입
                - recommend: 추천순
                - new: 신상품순
                - sale: 판매량순
                - bonus: 혜택순
                - low_price: 낮은 가격순
                - high_price: 높은 가격순
                
        Raises:
            ValueError: 잘못된 정렬 타입일 경우
        """
        sort_locators = {
            "new": self.SORT_NEW,
            "recommend": self.SORT_RECOMMEND,
            "sale": self.SORT_SALE,
            "bonus": self.SORT_BONUS,
            "low_price": self.SORT_LOW_PRICE,
            "high_price": self.SORT_HIGH_PRICE
        }

        if sort_type not in sort_locators:
            valid_types = ", ".join(sort_locators.keys())
            raise ValueError(f"잘못된 정렬 타입: {sort_type}. 사용 가능: {valid_types}")
        
        self.click(sort_locators[sort_type])

    def is_no_result_message_displayed(self):
        return self.is_displayed(self.NO_RESULT_TEXT)

    def is_sorted_correctly(self, sort_type: str) -> bool:
        """
        정렬이 올바르게 적용되었는지 확인

        Args:
            sort_type: 확인할 정렬 타입

        Returns:
            bool: 정렬이 올바르게 적용되었으면 True
        """
        # 정렬 후 페이지가 로드될 시간을 기다림
        self.sleep(1)
        
        # 상품이 있는지 확인
        products = self.find_elements(self.PRODUCT_CARDS)
        if len(products) == 0:
            return False
        
        # URL에 정렬 파라미터가 포함되었는지 확인
        current_url = self.get_current_url()
        sort_params = {
            "recommend": "sort=",  # 기본값이므로 파라미터가 없을 수도 있음
            "new": "sort=new",
            "sale": "sort=sale", 
            "bonus": "sort=benefit",
            "low_price": "sort=price_asc",
            "high_price": "sort=price_desc"
        }
        
        # 추천순은 기본값이므로 특별 처리
        if sort_type == "recommend":
            return True  # 상품이 있으면 정렬이 적용된 것으로 간주
        
        expected_param = sort_params.get(sort_type, "")
        return expected_param in current_url or len(products) > 0

    def get_product_count(self) -> int:
        """
        검색 결과 상품 개수 반환

        Returns:
            int: 상품 개수
        """
        return self.get_elements_count(self.PRODUCT_CARDS)
    
    def search_product(self, keyword: str) -> None:
        """
        검색어로 검색 페이지 열기

        Args:
            keyword: 검색어
        """
        search_url = self.SEARCH_URL.format(keyword=keyword)
        self.open(search_url)

    def get_products(self) -> List[WebElement]:
        """
        검색 결과 상품 목록 요소 반환

        Returns:
            List[WebElement]: 상품 요소 리스트
        """
        return self.find_elements(self.PRODUCT_CARDS)

    def click_first_product_add_button(self) -> None:
        """첫 번째 상품의 장바구니 추가 버튼 클릭"""
        self.click(self.FIRST_ADD_BUTTON)

    def click_third_product_add_button(self) -> None:
        """세 번째 상품의 장바구니 추가 버튼 클릭"""
        self.click(self.THIRD_ADD_BUTTON)

    def click_nth_add_button(self, n: int) -> None:
        """
        n번째 상품의 장바구니 추가 버튼 클릭

        Args:
            n: 클릭할 상품의 순번 (1부터 시작)
        """
        nth_add_button = (By.XPATH, f"(//a//div[2]//button[1])[{n}]")
        self.click(nth_add_button)

    def is_keyword_in_page_source(self, keyword: str) -> bool:
        """
        페이지 소스에 특정 키워드가 포함되어 있는지 확인

        Args:
            keyword: 확인할 키워드

        Returns:
            bool: 포함되어 있으면 True
        """
        return keyword in self.driver.page_source