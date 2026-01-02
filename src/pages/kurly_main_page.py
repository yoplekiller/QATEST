"""
Kurly 메인 페이지 Page Object
마켓컬리 웹사이트의 메인 페이지 기능을 담당하는 페이지 오브젝트
"""
from typing import List, Optional
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
from src.pages.base_page import BasePage


class KurlyMainPage(BasePage):
    """
    마켓컬리 메인 페이지 객체

    기능:
        - 상품 검색
        - 카테고리 탐색
        - 장바구니 접근
        - 상품 목록 확인
    """

    # URL
    KURLY_MAIN_URL = "https://www.kurly.com/main"

    # Locators - 검색
    SEARCH_INPUT = (By.XPATH, "//input[@placeholder='검색어를 입력해주세요']")
    SEARCH_BUTTON = (By.XPATH, "(//button[@id='submit'])[1]")

    # Locators - 상품 목록
    GOODS_ITEMS = (By.XPATH, "//div[contains(@class,'goods-card')]")
    GOODS_TITLE = (By.XPATH, ".//span[contains(@class,'goods-name')]")
    GOODS_PRICE = (By.XPATH, ".//span[contains(@class,'goods-price')]")


    # Locators - 카테고리
    CATEGORY_MENU = (By.XPATH, "//button[contains(text(),'카테고리')]")
    CATEGORY_LIST = (By.XPATH, "//div[contains(@class,'category-list')]//a")

    # Locators - 상품
    ADD_TO_CART_BUTTON = (By.XPATH, "//button[contains(text(),'장바구니')]")

    # Locators - 장바구니
    CART_ICON = (By.CSS_SELECTOR, ".css-1o9e4kz")
    CART_COUNT = (By.CSS_SELECTOR, ".css-5ojige") 

    # 팝업
    POPUP_CLOSE_BUTTON = (By.XPATH, "//button[contains(text(),'확인')]")
    POPUP_TEXT = (By.XPATH, "//div[@class='popup-content css-15yaaju e1k5padi2']")

    def __init__(self, driver):
        super().__init__(driver)

    def open_main_page(self) -> None:
        """메인 페이지 열기"""
        self.open(self.KURLY_MAIN_URL)

    def enter_search_keyword(self, keyword: str) -> None:
        """
        검색어 입력
        
        Args:
            keyword: 입력할 검색 키워드
        """
        self.send_keys(self.SEARCH_INPUT, keyword)

    def click_search_button(self) -> None:
        """검색 버튼 클릭"""
        self.click(self.SEARCH_BUTTON)

    def search_goods(self, keyword: str) -> None:
        """
        상품 검색 (입력 + 클릭)
        
        Args:
            keyword: 검색할 상품 키워드
        """
        self.enter_search_keyword(keyword)
        self.click_search_button()


    def open_category_menu(self) -> None:
        """카테고리 메뉴 열기"""
        self.click(self.CATEGORY_MENU)
        

    def get_category_list(self) -> List[str]:
        """
        카테고리 목록 반환

        Returns:
            List[str]: 카테고리 이름 리스트
        """
        categories = self.find_elements(self.CATEGORY_LIST)
        return [cat.text for cat in categories if cat.text]

    def select_category(self, category_name: str) -> None:
        """
        특정 이름의 카테고리 클릭

        Args:
            category_name: 선택할 카테고리 이름
        """
        locator = (By.XPATH, f"//div[contains(@class,'category-list')]//a[contains(text(),'{category_name}')]")
        self.click(locator)

    def go_to_cart(self) -> None:
        """장바구니 페이지로 이동"""
        # 모든 가림막/팝업 숨기기
        self.driver.execute_script("""
            document.querySelectorAll('.css-5ojige, .css-1ieq8u5').forEach(el => el.style.display = 'none');
        """)
        # 장바구니 아이콘 스크롤 이동
        cart_icon_el = self.driver.find_element(*self.CART_ICON)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", cart_icon_el)
        # JS로 직접 클릭
        self.driver.execute_script("arguments[0].click();", cart_icon_el)

    def get_cart_count(self) -> int:
        """
        장바구니에 담긴 상품 개수 반환

        Returns:
            int: 장바구니 상품 개수
        """
        if self.is_displayed(self.CART_COUNT):
            count_text = self.get_text(self.CART_COUNT)
            try:
                return int(count_text)
            except ValueError:
                return 0
        return 0

    def get_goods_count(self) -> int:
        """
        현재 페이지에 표시된 상품 개수 반환

        Returns:
            int: 상품 개수
        """
        return self.get_elements_count(self.GOODS_ITEMS)

    def get_goods(self) -> List[WebElement]:
        """
        현재 페이지의 상품 요소 목록 반환
        
        Returns:
            List[WebElement]: 상품 요소 리스트
        """
        return self.find_elements(self.GOODS_ITEMS)

    def click_good(self, index: int = 0) -> None:
        """
        상품 목록에서 특정 인덱스의 상품 클릭

        Args:
            index: 클릭할 상품 인덱스 (0부터 시작, 기본값=0)

        Raises:
            NoSuchElementException: 상품이 없을 때
            IndexError: 인덱스가 범위를 벗어났을 때
        """
        try:
            self.click_element_by_index(self.GOODS_ITEMS, index)
        except IndexError as e:
            products_count = self.get_elements_count(self.GOODS_ITEMS)
            if products_count == 0:
                raise NoSuchElementException("상품 목록이 비어있습니다")
            raise IndexError(f"인덱스 {index}가 범위 초과 (총 {products_count}개)")

    
    
    def is_search_keyword_required_popup_displayed(self) -> bool:
        """
        '검색어를 입력해주세요' 팝업 메시지 확인
        
        Returns:
            bool: 팝업 표시 여부
        """
        if self.is_displayed(self.POPUP_TEXT, timeout=5):
            popup_text = self.get_text(self.POPUP_TEXT)
            return "검색어를 입력해주세요" in popup_text
        return False
    
    def is_on_main_page(self) -> bool:
        """
        현재 페이지가 메인 페이지인지 확인
        
        Returns:
            bool: 메인 페이지 여부
        """
        return "kurly.com/main" in self.get_current_url()
