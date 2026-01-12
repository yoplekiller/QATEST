import allure
import pytest


@pytest.mark.ui
@allure.feature("장바구니")
@allure.story("장바구니 접근")
@allure.severity(allure.severity_level.CRITICAL)
class TestCart:

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
    def test_cart_page_access(self, kurly_main_page, kurly_cart_page):
        """
        장바구니 버튼 클릭 시 장바구니 페이지로 이동하는지 확인
        """
        
        with allure.step("마켓컬리 메인 페이지로 이동"):
            kurly_main_page.open_main_page()
            assert kurly_main_page.is_on_main_page(), "❌ 메인 페이지에 접속하지 못했습니다."

        
        with allure.step("장바구니 아이콘 클릭"):
            kurly_cart_page.click_cart_icon()   

        
        with allure.step("장바구니 페이지 확인"):
            kurly_cart_page.take_screenshot("장바구니_페이지")

            # URL 확인
            assert kurly_cart_page.is_on_cart_page(), \
                "❌ 장바구니 페이지가 아닙니다."

            # 페이지 제목 확인
            assert kurly_cart_page.has_kurly_in_title(), \
                "❌ 컬리 페이지 제목이 다릅니다."

            current_url = kurly_cart_page.get_current_url()
            allure.attach(
                f"현재 URL: {current_url}",
                name="URL_확인",
                attachment_type=allure.attachment_type.TEXT
            )
