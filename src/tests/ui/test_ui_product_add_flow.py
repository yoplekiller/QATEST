"""
상품 추가 플로우 테스트 (POM 패턴 적용)
로그인 → 상품 검색 → 장바구니 추가 → 확인
"""
import allure
import pytest


@pytest.mark.ui
@allure.feature("E2E 플로우")
@allure.story("로그인 후 상품 추가")
@allure.severity(allure.severity_level.CRITICAL)
class TestProductAddFlow:
    @allure.title("로그인 후 상품 추가 및 장바구니 확인")
    @allure.description("""
    **목적:** 로그인부터 장바구니 담기까지 전체 플로우가 정상 동작하는지 확인

    **테스트 단계:**
    1. 마켓컬리 메인 페이지 접속
    2. 로그인
    3. 상품 검색 ('과자')
    4. 상품 선택 및 장바구니 추가
    5. 수량 조절
    6. 장바구니 담기
    7. 장바구니 페이지로 이동

    **예상 결과:** 전체 플로우가 성공적으로 완료됨
    """)
    def test_full_product_add_flow(self, kurly_login_page, kurly_main_page, kurly_search_page, kurly_product_page, kurly_cart_page, test_credentials):
        """
        로그인 → 상품 검색 → 장바구니 추가 전체 플로우 테스트
        """
        # Step 1: 로그인
        with allure.step("로그인 프로세스"):
            kurly_login_page.open_main_page()
            kurly_login_page.go_to_login_page()
            kurly_login_page.enter_username(test_credentials['username'])
            kurly_login_page.enter_password(test_credentials['password'])
            kurly_login_page.click_login_button()

        # Step 2: 상품 검색
        with allure.step("상품 검색: '과자'"):
            kurly_main_page.search_goods("과자")

        # Step 3: 상품 추가
        with allure.step("세 번째 상품 선택"):
            kurly_search_page.click_nth_add_button(3)
        # Step 4: 수량 조절
        with allure.step("수량 올리기"):
            kurly_search_page.quantity_up_in_alt(1)

        # Step 5: 장바구니 담기
        with allure.step("장바구니 담기"):
            kurly_search_page.click_add_to_cart_in_popup()
            
        with allure.step("장바구니 페이지로 이동"):
            kurly_cart_page.click_cart_icon()

        # Then: 전체 플로우 성공 확인
        with allure.step("결과 확인"):
            kurly_cart_page.take_screenshot("전체_플로우_완료")

            allure.attach(
                "로그인부터 장바구니 추가까지 전체 플로우가 성공적으로 완료되었습니다",
                name="테스트_결과",
                attachment_type=allure.attachment_type.TEXT
            )
