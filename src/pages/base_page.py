import os
import re
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utils.logger import logger
from typing import Optional, Tuple, Any


Locator = Tuple[By, str]


class BasePage:

    def __init__(self, driver: Any, timeout: int = 5):
        """
        BasePage 생성자
        """
        # WebDriver 저장
        self.driver = driver

        # 기본 timeout 저장
        self.timeout = timeout

        # 기본 WebDriverWait 객체 생성(매번 만들지 않고 재사용)
        self.wait = WebDriverWait(self.driver, self.timeout)

    # =========================
    # 내부 유틸(Private Helpers)
    # =========================

    def _get_wait(self, timeout: Optional[int] = None) -> WebDriverWait:
        """
        timeout이 들어오면 그 값으로 WebDriverWait을 새로 만들고,
        아니면 생성자에서 만든 기본 wait 객체를 사용한다.
        """
        return WebDriverWait(self.driver, timeout) if timeout is not None else self.wait

    def _sanitize_filename(self, text: str, max_len: int = 120) -> str:
        """
        파일명에 들어가면 위험한 문자들을 제거/치환해서 안전한 파일명으로 만든다.
        """
        # None 방지: 혹시라도 None이 들어오면 빈 문자열 처리
        text = str(text) if text is not None else ""

        # 앞뒤 공백 제거 후 공백은 언더스코어로 치환
        text = text.strip().replace(" ", "_")

        # 윈도우/리눅스 파일명에서 위험한 문자 제거: \ / : * ? " < > |
        text = re.sub(r'[\\/:*?"<>|]', "", text)

        # 너무 복잡한 특수문자는 언더스코어로 치환(한글/영문/숫자/._-만 허용)
        text = re.sub(r"[^0-9a-zA-Z가-힣._-]+", "_", text)

        # 길이 제한
        text = text[:max_len] if len(text) > max_len else text

        # 비어버리면 기본값 반환
        return text or "screenshot"

    # =========================
    # 브라우저/페이지 공통 동작
    # =========================

    def open(self, url: str, maximize: bool = True) -> None:
        """
        페이지 열기

        Args:
            url: 이동할 URL
            maximize: 창 최대화 여부(헤드리스 환경에서는 의미 없을 수 있음)
        """
        # 어디로 이동하는지 로그로 남김
        logger.info(f"페이지 열기: {url}")

        # 페이지 이동
        self.driver.get(url)

        # UI 테스트 로컬 실행 시 보기 편하게 창 최대화
        if maximize:
            # 헤드리스/CI에서는 무의미하거나 환경에 따라 실패할 수 있음
            # (필요하면 try/except로 감싸도 됨)
            self.driver.maximize_window()

        # 요청 완료 로그
        logger.info(f"페이지 로드 요청 완료: {url}")

    # =========================
    # Wait 계열 (의도 분리)
    # =========================

    def wait_present(self, locator: Locator, timeout: Optional[int] = None):
        """
        요소가 DOM에 존재(presence)할 때까지 대기

        - "보이는지/클릭 가능한지"는 보장하지 않음
        - 정말 DOM 존재만 필요할 때 사용

        Returns:
            WebElement
        """
        wait = self._get_wait(timeout)
        return wait.until(EC.presence_of_element_located(locator))

    def wait_visible(self, locator: Locator, timeout: Optional[int] = None):
        """
        요소가 화면에 표시(visible)될 때까지 대기

        - 입력/텍스트 검증에 더 안전함

        Returns:
            WebElement
        """
        wait = self._get_wait(timeout)
        return wait.until(EC.visibility_of_element_located(locator))

    def wait_clickable(self, locator: Locator, timeout: Optional[int] = None):
        """
        요소가 클릭 가능한 상태(clickable)일 때까지 대기

        Returns:
            WebElement
        """
        wait = self._get_wait(timeout)
        return wait.until(EC.element_to_be_clickable(locator))

    def wait_for_element(self, locator: Locator, timeout: Optional[int] = None):
        """
        "요소가 나타날 때까지 대기"의 기본은 visible로 둔다.
        (presence는 DOM에만 있어도 통과할 수 있어서 UI 테스트에서 불안정함)

        Returns:
            WebElement
        """
        return self.wait_visible(locator, timeout)

    def wait_until_invisible(self, locator: Locator, timeout: Optional[int] = None) -> bool:
        """
        요소가 사라질 때까지 대기

        Returns:
            bool: 사라지면 True, timeout이면 False
        """
        wait = self._get_wait(timeout)
        try:
            return wait.until(EC.invisibility_of_element_located(locator))
        except TimeoutException:
            logger.warning(f"요소가 사라지지 않음: {locator}")
            return False

    # =========================
    # 스크린샷
    # =========================

    def take_screenshot(self, name: str = "screenshot", folder: str = "screenshots") -> str:
        """
        스크린샷을 파일로 저장하고 저장 경로를 반환

        Args:
            name: 파일명(확장자 제외)
            folder: 저장 폴더

        Returns:
            str: 저장된 파일 경로(실패 시 빈 문자열)
        """
        try:
            # 폴더가 없으면 생성(이미 있으면 아무 동작 안 함)
            os.makedirs(folder, exist_ok=True)

            # 덮어쓰기 방지 + 추적을 위해 타임스탬프 추가
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            # 파일명 안전 처리
            safe_name = self._sanitize_filename(name)

            # 최종 경로 생성
            screenshot_path = os.path.join(folder, f"{safe_name}_{timestamp}.png")

            # 저장 실행
            saved = self.driver.save_screenshot(screenshot_path)

            # Selenium이 False를 반환할 수도 있어서 결과 체크
            if saved:
                logger.info(f"스크린샷 저장: {screenshot_path}")
            else:
                logger.warning(f"스크린샷 저장 실패(드라이버 False 반환): {screenshot_path}")

            return screenshot_path

        except Exception as e:
            # 스크린샷 저장 실패는 테스트 실패를 더 크게 만들 수 있어서 보통은 로그만 남김
            logger.error(f"스크린샷 저장 실패: {e}", exc_info=True)
            return ""

    # =========================
    # 요소 찾기
    # =========================

    def find_element(self, locator: Locator, timeout: Optional[int] = None):
        """
        단일 요소 찾기 (기본은 visible 기준)

        Returns:
            WebElement
        """
        try:
            return self.wait_visible(locator, timeout)
        except TimeoutException:
            # locator는 문자열이 길고 특수문자가 섞일 수 있어서 safe name으로 저장
            self.take_screenshot(name=f"find_element_failed_{locator}")
            logger.error(f"요소 찾기 실패: {locator}")
            raise TimeoutException(f"❌ 요소를 찾을 수 없습니다(visible): {locator}")

    def find_elements(self, locator: Locator, timeout: Optional[int] = None):
        """
        복수 요소 찾기 (기본은 presence_of_all)

        Note:
            여러 요소는 "첫 요소가 visible" 같은 조건이 애매해서 presence 기반으로 두는 편이 많음

        Returns:
            List[WebElement]
        """
        wait = self._get_wait(timeout)
        try:
            return wait.until(EC.presence_of_all_elements_located(locator))
        except TimeoutException:
            logger.warning(f"find_elements 타임아웃: {locator}")
            # 필요하면 여기서도 스크린샷을 찍을 수 있음
            self.take_screenshot(name=f"find_elements_failed_{locator}")
            raise TimeoutException(f"❌ 요소들을 찾을 수 없습니다: {locator}")

    # =========================
    # 공통 액션
    # =========================

    def click(self, locator: Locator, timeout: Optional[int] = None) -> None:
        """
        요소 클릭 (clickable 기준)

        Args:
            locator: 클릭할 요소 locator
            timeout: 이 클릭에서만 적용할 timeout
        """
        try:
            element = self.wait_clickable(locator, timeout)
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
        """
        텍스트 입력

        Args:
            locator: 입력할 input locator
            text: 입력할 문자열
            clear_first: 입력 전 clear() 수행 여부
            timeout: 이 입력에서만 적용할 timeout
        """
        # 입력은 보이는 요소 기준이 더 안정적
        element = self.find_element(locator, timeout)

        # 기존 텍스트 제거 여부
        if clear_first:
            element.clear()

        # 텍스트 입력
        element.send_keys(text)

    def get_text(self, locator: Locator, timeout: Optional[int] = None) -> str:
        """
        요소의 텍스트 가져오기

        Returns:
            str: element.text
        """
        element = self.find_element(locator, timeout)
        return element.text

    def get_attribute(self, locator: Locator, attribute: str, timeout: Optional[int] = None) -> str:
        """
        요소의 속성값 가져오기

        Returns:
            str: element.get_attribute(attribute)
        """
        element = self.find_element(locator, timeout)
        return element.get_attribute(attribute)

    def is_displayed(self, locator: Locator, timeout: Optional[int] = None) -> bool:
        """
        요소 표시 여부 확인

        Returns:
            bool: 표시되면 True, 아니면 False
        """
        try:
            element = self.find_element(locator, timeout)
            return element.is_displayed()
        except (TimeoutException, NoSuchElementException):
            return False

    # =========================
    # 범용 유틸(선택)
    # =========================

    def get_elements_count(self, locator: Locator, timeout: Optional[int] = None) -> int:
        """
        특정 locator의 요소 개수 반환(범용)

        Returns:
            int: 요소 개수
        """
        elements = self.find_elements(locator, timeout)
        return len(elements)

    def click_element_by_index(self, locator: Locator, index: int = 0, timeout: Optional[int] = None) -> None:
        """
        여러 요소 중 특정 인덱스의 요소 클릭(범용)

        Args:
            locator: 요소들의 locator
            index: 클릭할 요소 index (0부터 시작)
            timeout: 대기 시간

        Raises:
            IndexError: index가 범위를 벗어난 경우
        """
        elements = self.find_elements(locator, timeout)

        # index가 범위를 벗어나면 예외 발생
        if index >= len(elements):
            self.take_screenshot(name=f"click_index_out_of_range_{locator}")
            raise IndexError(f"Index {index} out of range. Found {len(elements)} elements")

        # 해당 요소 클릭
        elements[index].click()

    # =========================
    # 상태 정보
    # =========================

    def get_current_url(self) -> str:
        """현재 페이지 URL 반환"""
        return self.driver.current_url

    def get_title(self) -> str:
        """현재 페이지 title 반환"""
        return self.driver.title
