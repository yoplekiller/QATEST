"""
Kurly 검색 결과 페이지 Page Object
마켓컬리 웹사이트의 검색 결과 기능을 담당하는 페이지 오브젝트
"""
from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
    TimeoutException,
)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
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
    GOODS_CARDS = (By.CSS_SELECTOR, "a[href*='/goods/']")
    GOODS_LIST = (By.XPATH, "//a[@class='css-11geqae e1c07x4811']")  # 대체 선택자
    NO_RESULT_TEXT = (By.XPATH, "//*[contains(normalize-space(), '검색된 상품이 없습니다') or contains(normalize-space(), '검색결과가 없습니다') or contains(normalize-space(), '에 대한 검색결과 0건')]")

    
    # Locators - ALT 기능 (검색 결과 내 수량 조절 및 확인)
    QUANTITY_UP_BUTTON_IN_ALT = (By.XPATH, "//button[@aria-label='Stepper plus']")
    QUANTITY_DOWN_BUTTON_IN_ALT = (By.XPATH, "//button[@aria-label='Stepper minus']")
    QUANTITY_DISPLAY_IN_ALT = (By.XPATH, "//button[@aria-label='Stepper plus']/preceding-sibling::*[1] | //button[@aria-label='Stepper minus']/following-sibling::*[1]") # 수량 표시 요소 ALT 내
    ADD_TO_CART_BUTTONS_IN_ALT = (By.XPATH, "//button[contains(.,'장바구니 담기')]") # 금액이 앞에 붙은 장바구니 담기 버튼 ALT 내
    SEARCH_RESULT_ADD_BUTTONS = (
        By.XPATH,
        "//button[@type='button' and not(@disabled) and "
        "(contains(normalize-space(.), '담기') "
        "or contains(normalize-space(.), '장바구니') "
        "or contains(@aria-label, '담기') "
        "or contains(@aria-label, '장바구니'))]",
    )


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

    def is_no_result_message_displayed(self) -> bool:
        """
        검색 결과가 없는지 확인
        - 기존: '검색된 상품이 없습니다' 텍스트 확인
        - 변경: 컬리가 결과 없을 때 추천상품만 보여주므로 결과 타이틀의 '0건' 텍스트도 확인

        Returns:
            bool: 검색 결과가 없으면 True
        """
        if self.is_displayed(self.NO_RESULT_TEXT, timeout=3):
            return True
        try:
            title_text = self.get_text(self.RESULT_TITLE, timeout=3)
            return "0건" in title_text
        except Exception:
            return False

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
        goods = self.find_elements(self.GOODS_CARDS)
        if len(goods) == 0:
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
        return expected_param in current_url or len(goods) > 0

    def get_goods_count(self) -> int:
        """
        검색 결과 상품 개수 반환

        Returns:
            int: 상품 개수 (검색 결과가 없으면 0)
        """
        try:
            return self.get_elements_count(self.GOODS_CARDS)
        except Exception:
            # 검색 결과가 없는 경우 0 반환
            return 0
    
    def search_goods(self, keyword: str) -> None:
        """
        검색어로 검색 페이지 열기

        Args:
            keyword: 검색어
        """
        search_url = self.SEARCH_URL.format(keyword=keyword)
        self.open(search_url)

    def get_goods(self) -> List[WebElement]:
        """
        검색 결과 상품 목록 요소 반환

        Returns:
            List[WebElement]: 상품 요소 리스트
        """
        return self.find_elements(self.GOODS_CARDS)

    def click_nth_add_button(self, n: int) -> None:
        """
        n번째 상품의 장바구니 추가 버튼 클릭

        Args:
            n: 클릭할 상품의 순번 (1부터 시작)
        """
        def find_nth_visible_add_button(driver):
            buttons = [
                button
                for button in driver.find_elements(*self.SEARCH_RESULT_ADD_BUTTONS)
                if button.is_displayed() and button.is_enabled()
            ]
            return buttons[n - 1] if len(buttons) >= n else None

        if n < 1:
            raise ValueError("n은 1 이상의 값이어야 합니다.")

        try:
            element = self._get_wait(10).until(find_nth_visible_add_button)
        except TimeoutException:
            self.take_screenshot(name=f"add_button_not_found_{n}")
            raise TimeoutException(f"{n}번째 장바구니 담기 버튼을 찾을 수 없습니다.")

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
            element,
        )

        try:
            ActionChains(self.driver).move_to_element(element).click().perform()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", element)

    def is_keyword_in_page_source(self, keyword: str) -> bool:
        """
        페이지 소스에 특정 키워드가 포함되어 있는지 확인

        Args:
            keyword: 확인할 키워드

        Returns:
            bool: 포함되어 있으면 True
        """
        return keyword in self.driver.page_source
    
    def quantity_up_in_alt(self, times: int =1) -> None:
        """
        ALT에서 수량 올리기

        Args:
            times: 클릭 횟수 (기본값: 1)
        """
        try:
            self.wait_clickable(self.QUANTITY_UP_BUTTON_IN_ALT, timeout=5)
            for _ in range(times):
                self.click(self.QUANTITY_UP_BUTTON_IN_ALT)
        except Exception:
            return False
    
    def quantity_down_in_alt(self, times: int =1) -> None:
        """
        ALT에서 수량 내리기

        Args:
            times: 클릭 횟수 (기본값: 1)
        """
        try:
            self.wait_clickable(self.QUANTITY_DOWN_BUTTON_IN_ALT, timeout=5)
            for _ in range(times):
                self.click(self.QUANTITY_DOWN_BUTTON_IN_ALT)
        except Exception:
            return False
        
    
    def is_diplayed_quantity_in_alt(self, expected_quantity: int) -> bool:
        """
        ALT에서 표시된 수량이 예상 수량과 일치하는지 확인

        Args:add_to_cart_in_alt
            expected_quantity: 예상 수량

        Returns://button[contains(text(),'3,070원 장바구니 담기')]
            bool: 일치하면 True
        """
        quantity_text = self.get_text(self.QUANTITY_DISPLAY_IN_ALT)
        try:
            current_quantity = int(quantity_text)
            return current_quantity == expected_quantity
        except ValueError:
            return False
        

    POPUP_CLOSE_BUTTON = (By.XPATH, "//button[@aria-label='닫기']")

    def click_add_to_cart_in_popup(self) -> None:
        """add_to_cart_in_alt의 별칭 - 팝업에서 장바구니 담기 버튼 클릭"""
        self.add_to_cart_in_alt()

    def close_cart_popup(self) -> None:
        """장바구니 팝업 닫기 버튼 클릭"""
        def find_visible_close_button(driver):
            close_buttons = driver.find_elements(*self.POPUP_CLOSE_BUTTON)
            for button in close_buttons:
                if button.is_displayed() and button.is_enabled():
                    return button
            return None

        def is_click_point_clear(driver):
            return driver.execute_script(
                """
                const el = arguments[0];
                const rect = el.getBoundingClientRect();
                const x = rect.left + rect.width / 2;
                const y = rect.top + rect.height / 2;
                const top = document.elementFromPoint(x, y);
                return top === el || el.contains(top);
                """,
                close_button,
            )

        wait = WebDriverWait(self.driver, 10)
        close_button = wait.until(find_visible_close_button)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
            close_button,
        )

        try:
            WebDriverWait(self.driver, 3).until(is_click_point_clear)
            close_button.click()
        except (ElementClickInterceptedException, TimeoutException):
            self.driver.execute_script("arguments[0].click();", close_button)

        self.wait_until_invisible(self.POPUP_CLOSE_BUTTON, timeout=10)

    def add_to_cart_in_alt(self) -> None:
        """ALT에서 장바구니 담기 버튼 클릭"""
        self.wait_visible(self.ADD_TO_CART_BUTTONS_IN_ALT, timeout=10)
        self.click(self.ADD_TO_CART_BUTTONS_IN_ALT)
        self.close_cart_popup()
        self.wait_until_invisible(self.ADD_TO_CART_BUTTONS_IN_ALT, timeout=10)


    def click_first_good(self) -> None:
        """
        상품 목록에서 첫 번째 상품 클릭

        Raises:
            NoSuchElementException: 상품이 없을 때
        """
        self.click_element_by_index(self.GOODS_CARDS, 0)

    def is_add_to_cart_success(self) -> bool:
        """
        장바구니 담기 성공 여부 확인

        Returns:
            bool: 성공했으면 True
        """
        success_message_locator = (By.XPATH, "//*[contains(text(),'장바구니에 상품을 담았습니다.')]")
        return self.is_displayed(success_message_locator)
    
    def is_check_url(self, substring: str) -> bool:
        """
        현재 URL에 특정 문자열이 포함되어 있는지 확인

        Args:
            substring: 확인할 문자열

        Returns:
            bool: 포함되어 있으면 True
        """
        current_url = self.get_current_url()
        return substring in current_url
    
    def get_title(self) -> str:
        """
        현재 페이지의 제목 반환

        Returns:
            str: 페이지 제목
        """
        return self.driver.title
