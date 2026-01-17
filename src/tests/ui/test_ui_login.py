import allure
import pytest


@pytest.mark.ui
@allure.feature("사용자 인증")
@allure.story("로그인")
@allure.severity(allure.severity_level.CRITICAL)
class TestLogin:

    @allure.title("잘못된 계정 정보로 로그인 실패 테스트")
    @allure.description("""
    **목적:** 잘못된 아이디와 비밀번호로 로그인 시도 시 적절한 에러 메시지가 표시되는지 확인

    **테스트 단계:**
    1. 마켓컬리 메인 페이지 접속
    2. 로그인 버튼 클릭
    3. 잘못된 아이디 입력
    4. 잘못된 비밀번호 입력
    5. 로그인 버튼 클릭
    6. 에러 메시지 표시 확인

    **예상 결과:** 로그인 실패 메시지가 화면에 표시됨
    """)
    def test_login_with_invalid_credentials(self, kurly_login_page, test_credentials_invalid):
        """
        잘못된 계정 정보로 로그인 시도 시 실패하는지 확인
        """
        # Given: 로그인 페이지로 이동
        with allure.step("마켓컬리 메인 페이지로 이동"):
            kurly_login_page.open_main_page()

        with allure.step("로그인 페이지로 이동"):
            kurly_login_page.go_to_login_page()

        # When: 잘못된 계정 정보로 로그인 시도
        with allure.step("잘못된 계정 정보 입력 및 로그인 시도"):
            kurly_login_page.enter_username(test_credentials_invalid['username'])
            kurly_login_page.enter_password(test_credentials_invalid['password'])
            kurly_login_page.click_login_button()

        # Then: 에러 메시지가 표시되어야 함
        with allure.step("로그인 실패 메시지 확인"):
            kurly_login_page.take_screenshot("로그인_실패_화면")

            assert kurly_login_page.is_mismatch_error_message_displayed(), \
                "❌ 로그인 실패 메시지가 표시되지 않음"

            error_text = kurly_login_page.get_mismatch_error_message_text()
            allure.attach(
                f"에러 메시지: {error_text}",
                name="에러_메시지_내용",
                attachment_type=allure.attachment_type.TEXT
            )

    @allure.title("빈 계정 정보로 로그인 실패 테스트")
    @allure.description("""
    **목적:** 아이디나 비밀번호를 입력하지 않고 로그인 시도 시 적절한 처리가 되는지 확인

    **테스트 단계:**
    1. 마켓컬리 메인 페이지 접속
    2. 로그인 버튼 클릭
    3. 아이디와 비밀번호를 입력하지 않음
    4. 로그인 버튼 클릭
    5. 에러 메시지 또는 유효성 검사 메시지 표시 확인
    """)
    def test_login_with_empty_credentials(self, kurly_login_page):
        """
        빈 계정 정보로 로그인 시도 시 실패하는지 확인
        """
        # Given: 로그인 페이지로 이동
        kurly_login_page.open_main_page()
        kurly_login_page.go_to_login_page()

        # When: 아무것도 입력하지 않고 로그인 버튼 클릭
        with allure.step("빈 계정 정보로 로그인 시도"):
            kurly_login_page.click_login_button()

        # Then: 에러 메시지가 표시되거나 로그인이 되지 않아야 함
        with allure.step("에러 처리 확인"):
            kurly_login_page.take_screenshot("빈_계정_정보_로그인_시도")
            # 에러 메시지가 표시되거나, 여전히 로그인 페이지에 있어야 함
            is_still_on_login_page = "login" in kurly_login_page.get_current_url()
            has_error_message = kurly_login_page.is_error_message_displayed()

            assert is_still_on_login_page or has_error_message, \
                "❌ 빈 계정 정보로 로그인이 진행되어서는 안 됨"

    @allure.title("로그인 페이지 요소 표시 확인") 
    @allure.description("""
    **목적:** 로그인 페이지의 모든 필수 요소가 올바르게 표시되는지 확인

    **확인 항목:**
    - 아이디 입력 필드
    - 비밀번호 입력 필드
    - 로그인 버튼
    """)
    def test_login_page_elements_displayed(self, kurly_login_page):
        """
        로그인 페이지의 필수 요소들이 화면에 표시되는지 확인
        """
        # Given: 로그인 페이지로 이동
        kurly_login_page.open_main_page()
        kurly_login_page.go_to_login_page()

        # Then: 모든 로그인 요소가 표시되어야 함
        with allure.step("로그인 페이지 요소 확인"):
            kurly_login_page.take_screenshot("로그인_페이지")

            assert kurly_login_page.is_displayed(kurly_login_page.USERNAME_INPUT), \
                "❌ 아이디 입력 필드가 표시되지 않음"

            assert kurly_login_page.is_displayed(kurly_login_page.PASSWORD_INPUT), \
                "❌ 비밀번호 입력 필드가 표시되지 않음"

            assert kurly_login_page.is_displayed(kurly_login_page.SUBMIT_BUTTON), \
                "❌ 로그인 버튼이 표시되지 않음"
