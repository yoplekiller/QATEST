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
    StaleElementReferenceException,
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
    # ALT(상품 선택 팝업)는 role=dialog. 팝업 안 요소는 전부 dialog 기준으로 좁혀서,
    # 팝업 뒤 검색 결과 카드의 버튼이 먼저 잡히는 일을 막는다(2026-11-01 실측).
    ALT_DIALOG = (By.XPATH, "//*[@role='dialog']")
    QUANTITY_UP_BUTTON_IN_ALT = (By.XPATH, "//*[@role='dialog']//button[@aria-label='Stepper plus']")
    QUANTITY_DOWN_BUTTON_IN_ALT = (By.XPATH, "//*[@role='dialog']//button[@aria-label='Stepper minus']")
    # 첫 번째 스텝퍼(옵션형 상품이면 첫 옵션)의 수량 표시.
    # 스텝퍼 구조(2026-11-01 실측): [- 버튼][p: 수량][+ 아이콘 div][+ 버튼] 이라
    # "+ 버튼 바로 앞 형제"는 아이콘 div(빈 텍스트)다 → - 버튼 다음의 p 를 읽는다.
    QUANTITY_DISPLAY_IN_ALT = (By.XPATH, "(//*[@role='dialog']//button[@aria-label='Stepper minus'])[1]/following-sibling::p[1]")
    ADD_TO_CART_BUTTONS_IN_ALT = (By.XPATH, "//*[@role='dialog']//button[contains(.,'장바구니 담기')]") # 금액이 앞에 붙은 장바구니 담기 버튼 ALT 내
    ADD_TO_CART_TOAST = (By.XPATH, "//*[contains(text(),'장바구니에 상품을 담았습니다')]")
    SEARCH_RESULT_ADD_BUTTONS = (
        By.XPATH,
        "//button[@type='button' and not(@disabled) and not(ancestor::*[@role='dialog']) and "
        "(contains(normalize-space(.), '담기') "
        "or contains(normalize-space(.), '장바구니') "
        "or contains(@aria-label, '담기') "
        "or contains(@aria-label, '장바구니'))]",
    )
    # 검색어가 보안 필터 등에 걸렸을 때 뜨는 일반 에러 페이지
    ERROR_PAGE_TEXT = (By.XPATH, "//*[contains(normalize-space(), '알 수 없는 에러가 발생했습니다')]")


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
        # URL에 정렬 파라미터가 포함되었는지 확인
        # sorted_type 값은 실제 사이트 동작 확인 후 반영 (2026-08-24 검증)
        sort_params = {
            "new": "sorted_type=0",
            "sale": "sorted_type=1",
            "low_price": "sorted_type=2",
            "high_price": "sorted_type=3",
            "bonus": "sorted_type=5",
        }

        if sort_type == "recommend":
            # 추천순은 기본 정렬이라 URL에 파라미터가 안 붙어서(=생기는 걸 기다릴
            # 대상이 없음) 정렬 클릭이 반영될 시간만 짧게 기다린다.
            self.sleep(1)
        else:
            # 정렬 파라미터가 URL에 실제로 반영될 때까지 대기(고정 sleep 대신)
            self.wait_until_url_contains(sort_params.get(sort_type, ""), timeout=5)

        # 상품이 있는지 확인
        goods = self.find_elements(self.GOODS_CARDS)
        if len(goods) == 0:
            return False

        current_url = self.get_current_url()
        if sort_type == "recommend":
            return "sorted_type=" not in current_url

        return sort_params.get(sort_type, "") in current_url

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

        def find_and_click():
            # 검색 결과 목록은 장바구니 담기/무한스크롤 때 재렌더링되므로 찾기~클릭을 한 단위로 재시도
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

        self.retry_on_stale(find_and_click)
        # 팝업이 열린 것까지 확인해야 다음 단계(수량/담기)가 이전 팝업 잔상과 섞이지 않는다
        self.wait_visible(self.ADD_TO_CART_BUTTONS_IN_ALT, timeout=10)

    def is_keyword_in_page_source(self, keyword: str) -> bool:
        """
        페이지 소스에 특정 키워드가 포함되어 있는지 확인

        Args:
            keyword: 확인할 키워드

        Returns:
            bool: 포함되어 있으면 True
        """
        return keyword in self.driver.page_source
    
    def _read_quantity_in_alt(self):
        """ALT 첫 번째 스텝퍼 수량. 재렌더링 중이라 못 읽으면 None."""
        try:
            return int(self.driver.find_element(*self.QUANTITY_DISPLAY_IN_ALT).text.strip())
        except (NoSuchElementException, StaleElementReferenceException, ValueError):
            return None

    def get_quantity_in_alt(self, timeout: int = 5) -> int:
        """ALT 첫 번째 스텝퍼의 현재 수량 (읽힐 때까지 대기)"""
        self._get_wait(timeout).until(lambda d: self._read_quantity_in_alt() is not None)
        return self._read_quantity_in_alt()

    def _step_quantity_in_alt(self, button_locator, delta: int, times: int) -> None:
        """
        스텝퍼를 times번 누르고, 매번 수량이 실제로 delta만큼 바뀐 것까지 확인한다.

        예전에는 클릭 사이에 sleep(0.3)만 두고 예외를 삼켜서(return False) 클릭이 씹혀도
        테스트가 모른 채 진행했다(2026-10-24 CI: 초기 2, 기대 3 실패). 이제 반영을 기다리고,
        반영이 안 되면 어떤 값에서 멈췄는지 메시지와 함께 실패한다.
        """
        for _ in range(times):
            before = self.get_quantity_in_alt()
            expected = before + delta
            self.click(button_locator)
            try:
                self._get_wait(5).until(lambda d: self._read_quantity_in_alt() == expected)
            except TimeoutException:
                self.take_screenshot(name="quantity_not_changed")
                raise TimeoutException(
                    f"❌ 수량이 {before} → {expected}로 바뀌지 않았습니다(현재 {self._read_quantity_in_alt()})"
                )

    def quantity_up_in_alt(self, times: int = 1) -> None:
        """
        ALT에서 수량 올리기 (클릭마다 반영 확인)

        Args:
            times: 클릭 횟수 (기본값: 1)
        """
        self._step_quantity_in_alt(self.QUANTITY_UP_BUTTON_IN_ALT, +1, times)

    def quantity_down_in_alt(self, times: int = 1) -> None:
        """
        ALT에서 수량 내리기 (클릭마다 반영 확인)

        Args:
            times: 클릭 횟수 (기본값: 1)
        """
        self._step_quantity_in_alt(self.QUANTITY_DOWN_BUTTON_IN_ALT, -1, times)

    def is_diplayed_quantity_in_alt(self, expected_quantity: int) -> bool:
        """
        ALT에서 표시된 수량이 예상 수량과 일치하는지 확인

        Args:
            expected_quantity: 예상 수량

        Returns:
            bool: 일치하면 True
        """
        return self._read_quantity_in_alt() == expected_quantity

    POPUP_CLOSE_BUTTON = (By.XPATH, "//*[@role='dialog']//button[@aria-label='닫기']")

    def click_add_to_cart_in_popup(self) -> None:
        """add_to_cart_in_alt의 별칭 - 팝업에서 장바구니 담기 버튼 클릭"""
        self.add_to_cart_in_alt()

    def close_cart_popup(self) -> None:
        """
        ALT가 아직 열려 있으면 닫기 버튼으로 닫는다. 이미 닫혔으면 아무 것도 하지 않는다.

        닫기 버튼은 매번 새로 찾는다 - 팝업이 닫히는 중(재렌더링)에 예전에 찾아둔 버튼을
        누르면 StaleElementReferenceException이 난다(2026-10-28/29 CI 실패 원인).
        """
        def close_once() -> None:
            buttons = [b for b in self.driver.find_elements(*self.POPUP_CLOSE_BUTTON) if b.is_displayed()]
            if not buttons:
                return
            button = buttons[0]
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
                button,
            )
            if self.wait_click_point_clear(button, timeout=3):
                try:
                    button.click()
                    return
                except ElementClickInterceptedException:
                    pass
            self.driver.execute_script("arguments[0].click();", button)

        self.retry_on_stale(close_once)
        self.wait_until_invisible(self.POPUP_CLOSE_BUTTON, timeout=10)

    def add_to_cart_in_alt(self) -> bool:
        """
        ALT에서 장바구니 담기 버튼 클릭

        2026-11-01 실측: 담기를 누르면 사이트가 ALT를 0.5~0.8초 안에 스스로 닫고
        '장바구니에 상품을 담았습니다.' 토스트를 띄운다. 그래서 닫기 버튼을 누르는 대신
        팝업 DOM이 사라지는 것(staleness)을 기다리고, 그래도 안 닫혔을 때만 직접 닫는다.

        Returns:
            bool: 담기 완료 토스트를 봤으면 True
        """
        self.wait_visible(self.ADD_TO_CART_BUTTONS_IN_ALT, timeout=10)
        self.select_first_option_if_needed()
        dialog = self.wait_present(self.ALT_DIALOG, timeout=5)
        self.click(self.ADD_TO_CART_BUTTONS_IN_ALT)

        try:
            self.wait_visible(self.ADD_TO_CART_TOAST, timeout=5)
            toast_seen = True
        except TimeoutException:
            toast_seen = False

        if not self.wait_for_staleness(dialog, timeout=5):
            self.close_cart_popup()
        self.wait_until_invisible(self.ADD_TO_CART_BUTTONS_IN_ALT, timeout=10)
        return toast_seen

    def select_first_option_if_needed(self) -> None:
        """
        옵션이 여러 개인 상품(예: '~7종 (택1)')은 ALT를 열면 모든 옵션의 수량이 0으로
        시작한다. 아무 옵션도 선택하지 않은 채 장바구니 담기를 확정하면 사이트가
        "최소 구매 수량은 N개 입니다" 경고창을 띄우며 막아버려(실사이트 확인,
        2026-09-20), 이후 상품 선택 로직 전체가 그 경고창에 가려 깨진다.
        첫 옵션 수량이 0일 때만 1개로 올린다.

        2026-11-01 수정: 예전에는 스텝퍼가 보이기만 하면 +를 눌렀는데, 단일 상품도
        스텝퍼가 있고 수량 1로 시작해서 의도와 달리 2개가 담겼다(가격 1,080원 → 2,160원 실측).
        """
        steppers = [
            button
            for button in self.driver.find_elements(*self.QUANTITY_UP_BUTTON_IN_ALT)
            if button.is_displayed() and button.is_enabled()
        ]
        if not steppers or self.get_quantity_in_alt() != 0:
            return
        self._step_quantity_in_alt(self.QUANTITY_UP_BUTTON_IN_ALT, +1, 1)

    def is_error_page(self) -> bool:
        """'알 수 없는 에러가 발생했습니다' 일반 에러 페이지가 떠 있는지"""
        return any(e.is_displayed() for e in self.driver.find_elements(*self.ERROR_PAGE_TEXT))


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
