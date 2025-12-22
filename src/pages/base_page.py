"""
Base Page Object
모든 Page Object 클래스의 기본이 되는 베이스 클래스
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utils.logger import logger
from typing import Optional, Tuple
import time


Locator = Tuple[str, str]


class BasePage:
    """
    모든 Page Object의 부모 클래스

    기능:
        - 공통 웹 요소 조작 (클릭, 입력, 찾기 등)
        - 대기 처리 (Explicit Wait)
        - 스크린샷 캡처
        - 예외 처리 및 로깅
    """
    def __init__(self, driver, timeout: int = 5):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(self.driver, self.timeout)

    def open(self, url: str, maximize: bool = True) -> None:
        """페이지 열기 및 창 최대화"""
        logger.info(f"페이지 열기: {url}")
        self.driver.get(url)

        if maximize:
            self.driver.maximize_window()
        logger.info(f"페이지 로드 요청 완료: {url}")

    def _get_wait(self, timeout: Optional[int] = None) -> WebDriverWait:
        """타임아웃 설정에 따른 WebDriverWait 반환"""
        return WebDriverWait(self.driver, timeout) if timeout else self.wait
    
    def wait_for_element(self, locator: Locator, timeout: Optional[int] = None) -> None:
        """
        요소가 나타날 때까지 대기

        Note: 내부적으로 find_element를 호출합니다.
              요소를 반환받으려면 find_element를 직접 사용하세요.
        """
        self.find_element(locator, timeout)

    def take_screenshot(self, name: str = "screenshot") -> None:
        """스크린샷을 파일로 저장"""
        try:
            screenshot_path = f"screenshots/{name}.png"
            self.driver.save_screenshot(screenshot_path)
            logger.info(f"스크린샷 저장: {screenshot_path}")
        except Exception as e:
            logger.error(f"스크린샷 저장 실패: {e}")

    def find_element(self, locator: Locator, timeout: Optional[int] = None):
        """단일 요소 찾기"""
        wait = self._get_wait(timeout)
        try:
            element = wait.until(EC.presence_of_element_located(locator))
            return element
        except TimeoutException:
            self.take_screenshot(name=f"find_element_failed_{locator}")
            logger.error(f"요소 찾기 실패: {locator}")
            raise TimeoutException(f"❌ 요소를 찾을 수 없습니다: {locator}")

    def find_elements(self, locator: Locator, timeout: Optional[int] = None):
        """복수 요소 찾기"""
        wait = self._get_wait(timeout)
        try:
            elements = wait.until(EC.presence_of_all_elements_located(locator))
            return elements
        except TimeoutException:
            logger.warning(f"find_elements 타임아웃: {locator}")
            raise TimeoutException(f"❌ 요소를 찾을 수 없습니다: {locator}")

    def click(self, locator: Locator, timeout: Optional[int] = None) -> None:
        """요소 클릭"""
        wait = self._get_wait(timeout)
        try:
            element = wait.until(EC.element_to_be_clickable(locator))
            element.click()
        except TimeoutException:
            self.take_screenshot(name=f"click_failed_{locator}")
            logger.error(f"클릭 실패: {locator}")
            raise TimeoutException(f"❌ 요소를 클릭할 수 없습니다: {locator}")

    def send_keys(
        self,
        locator: Locator,
        text: str,
        clear_first: bool = True,
        timeout: Optional[int] = None
    ) -> None:
        """텍스트 입력"""
        element = self.find_element(locator, timeout)

        if clear_first:
            element.clear()

        element.send_keys(text)

    def get_text(self, locator: Locator, timeout: Optional[int] = None) -> str:
        """요소의 텍스트 가져오기"""
        element = self.find_element(locator, timeout)
        return element.text

    def get_attribute(self, locator: Locator, attribute: str, timeout: Optional[int] = None) -> str:
        """요소의 속성값 가져오기"""
        element = self.find_element(locator, timeout)
        return element.get_attribute(attribute)

    def is_displayed(self, locator: Locator, timeout: Optional[int] = None) -> bool:
        """요소 표시 여부 확인"""
        try:
            element = self.find_element(locator, timeout)
            return element.is_displayed()
        except (TimeoutException, NoSuchElementException):
            return False

    def wait_until_invisible(self, locator: Locator, timeout: Optional[int] = None) -> bool:
        """요소가 사라질 때까지 대기"""
        wait = self._get_wait(timeout)
        try:
            return wait.until(EC.invisibility_of_element_located(locator))
        except TimeoutException:
            logger.warning(f"요소가 사라지지 않음: {locator}")
            return False

    def get_current_url(self) -> str:
        """현재 페이지의 URL 반환"""
        return self.driver.current_url

    def get_title(self) -> str:
        """현재 페이지의 title 반환"""
        return self.driver.title
    
    def sleep(self, seconds: int) -> None:
        """지정된 시간만큼 대기"""
        time.sleep(seconds)

    # ========================================
    # 공통 메서드 (중복 제거용)
    # ========================================

    def change_quantity(self, locator: Locator, times: int = 1) -> None:
        """
        수량 조절 공통 메서드

        Args:
            locator: 수량 조절 버튼의 locator (증가/감소)
            times: 클릭 횟수 (기본값: 1)

        Note:
            increase_quantity, decrease_quantity의 중복 로직을 통합
        """
        for _ in range(times):
            self.click(locator)

    def get_elements_count(self, locator: Locator, timeout: Optional[int] = None) -> int:
        """
        특정 locator의 요소 개수 반환

        Args:
            locator: 요소를 찾을 locator
            timeout: 대기 시간

        Returns:
            int: 요소 개수

        Note:
            get_product_count 등의 중복 로직을 통합
        """
        elements = self.find_elements(locator, timeout)
        return len(elements)

    def click_element_by_index(self, locator: Locator, index: int = 0, timeout: Optional[int] = None) -> None:
        """
        여러 요소 중 특정 인덱스의 요소 클릭

        Args:
            locator: 요소들의 locator
            index: 클릭할 요소의 인덱스 (0부터 시작)
            timeout: 대기 시간

        Raises:
            IndexError: 인덱스가 범위를 벗어난 경우

        Note:
            click_product, click_search_result 등의 중복 로직을 통합
        """
        elements = self.find_elements(locator, timeout)
        if index >= len(elements):
            raise IndexError(f"Index {index} out of range. Found {len(elements)} elements")
        elements[index].click()
