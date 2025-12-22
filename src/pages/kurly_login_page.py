"""
Kurly 로그인 페이지 Page Object
마켓컬리 웹사이트의 로그인 기능을 담당하는 페이지 오브젝트
"""
from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage


class KurlyLoginPage(BasePage):
    """
    마켓컬리 로그인 페이지 객체

    기능:
        - 로그인 페이지 접근
        - 사용자 인증
        - 로그인 성공/실패 확인
    """

    # URL
    KURLY_MAIN_URL = "https://www.kurly.com/main"

    # Locators
    LOGIN_BUTTON = (By.XPATH, "//a[contains(text(),'로그인')]")
    USERNAME_INPUT = (By.XPATH, "//input[@placeholder='아이디를 입력해주세요']")
    PASSWORD_INPUT = (By.XPATH, "//input[@placeholder='비밀번호를 입력해주세요']")
    SUBMIT_BUTTON = (By.XPATH, "//button[@type='submit']")
    ERROR_MESSAGE = (By.XPATH, "//div[@class='css-hj3ig8 e15sbxqa2']")

    # 로그인 성공 후 표시되는 요소 (사용자 메뉴 등)
    USER_MENU = (By.XPATH, "//button[contains(@class,'css-')]")

    def __init__(self, driver):
        super().__init__(driver)

    def open_main_page(self) -> None:
        """마켓컬리 메인 페이지로 이동"""
        self.open(self.KURLY_MAIN_URL)

    def go_to_login_page(self) -> None:
        """메인 페이지에서 로그인 버튼을 클릭하여 로그인 페이지로 이동"""
        self.click(self.LOGIN_BUTTON)

    def enter_username(self, username: str) -> None:
        """
        아이디 입력 필드에 값 입력

        Args:
            username: 입력할 아이디
        """
        self.send_keys(self.USERNAME_INPUT, username)

    def enter_password(self, password: str) -> None:
        """
        비밀번호 입력 필드에 값 입력

        Args:
            password: 입력할 비밀번호
        """
        self.send_keys(self.PASSWORD_INPUT, password)

    def click_login_button(self) -> None:
        """로그인 제출 버튼 클릭"""
        self.click(self.SUBMIT_BUTTON)

    def login(self, username: str, password: str) -> None:
        """
        전체 로그인 플로우 실행

        Args:
            username: 로그인 아이디
            password: 로그인 비밀번호
        """
        self.open_main_page()
        self.go_to_login_page()
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()

    def is_error_message_displayed(self) -> bool:
        """
        로그인 실패 시 에러 메시지가 표시되는지 확인

        Returns:
            bool: 에러 메시지 표시 여부
        """
        return self.is_displayed(self.ERROR_MESSAGE)

    def get_error_message_text(self) -> str:
        """
        에러 메시지의 텍스트를 가져옴

        Returns:
            str: 에러 메시지 텍스트 (없으면 빈 문자열)
        """
        if self.is_error_message_displayed():
            return self.get_text(self.ERROR_MESSAGE)
        return ""

    def is_login_successful(self, timeout: int = 5) -> bool:
        """
        로그인이 성공했는지 확인 (사용자 메뉴 표시 여부로 판단)

        Args:
            timeout: 대기 시간 (초)

        Returns:
            bool: 로그인 성공 여부
        """
        return self.is_displayed(self.USER_MENU, timeout=timeout)
