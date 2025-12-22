"""
장바구니 테스트 (POM 패턴 적용)
"""
import allure
import pytest
from src.pages.kurly_main_page import KurlyMainPage
from src.pages.kurly_cart_page import KurlyCartPage


@pytest.mark.ui
@allure.feature("장바구니")
@allure.story("장바구니 접근")
@allure.severity(allure.severity_level.CRITICAL)
class TestCart:
    """
    장바구니 기능 테스트 클래스 (POM 적용)
    """

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """
        각 테스트 메서드 실행 전 자동으로 실행되는 설정
        """
        self.main_page = KurlyMainPage(driver)
        self.cart_page = KurlyCartPage(driver)

    @allure.title("장바구니 페이지 접근 테스트")
    @allure.description("""
    **목적:** 장바구니 아이콘 클릭 시 장바구니 페이지로 정상 이동하는지 확인

    **테스트 단계:**
    1. 마켓컬리 메인 페이지 접속
    2. 장바구니 아이콘 클릭
    3. URL에 'cart' 포함 확인
    4. 페이지 제목 확인

    **예상 결과:** 장바구니 페이지로 정상 이동
    """)
    def test_cart_page_access(self, driver):
        """
        장바구니 버튼 클릭 시 장바구니 페이지로 이동하는지 확인
        """
        # Given: 메인 페이지로 이동
        with allure.step("마켓컬리 메인 페이지로 이동"):
            self.main_page.open_main_page()

        # When: 장바구니 아이콘 클릭
        with allure.step("장바구니 아이콘 클릭"):
            self.cart_page.click_cart_icon()

        # Then: 장바구니 페이지로 이동되어야 함
        with allure.step("장바구니 페이지 확인"):
            self.cart_page.take_screenshot("장바구니_페이지")

            # URL 확인
            assert self.cart_page.is_on_cart_page(), \
                "❌ 장바구니 페이지가 아닙니다."

            # 페이지 제목 확인
            assert self.cart_page.has_kurly_in_title(), \
                "❌ 컬리 페이지 제목이 다릅니다."

            current_url = self.cart_page.get_current_url()
            allure.attach(
                f"현재 URL: {current_url}",
                name="URL_확인",
                attachment_type=allure.attachment_type.TEXT
            )
