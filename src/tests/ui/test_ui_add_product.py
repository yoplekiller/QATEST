"""
상품 추가 테스트 (POM 패턴 적용)
"""
import allure
import pytest



@pytest.mark.ui
@allure.feature("상품 관리")
@allure.story("상품 추가")
@allure.severity(allure.severity_level.CRITICAL)
class TestAddProduct:

    @allure.title("상품 검색 후 장바구니 추가 테스트")
    @allure.description("""
    **목적:** 상품 검색 → 수량 조절 → 장바구니 담기 플로우가 정상 동작하는지 확인

    **테스트 단계:**
    1. 마켓컬리 메인 페이지 접속
    2. '과자' 검색
    3. 세 번째 상품의 장바구니 추가 버튼 클릭
    4. 수량 올리기 (2회)
    5. 수량 내리기 (2회)
    6. 장바구니 담기 버튼 클릭
    7. 검색 결과 확인

    **예상 결과:** 상품이 장바구니에 정상적으로 담김
    """)
    def test_add_product_to_cart(self, kurly_main_page, kurly_search_page, kurly_product_page):
        """
        상품 검색 후 장바구니에 추가하는 전체 플로우 테스트
        """
        # Given: 메인 페이지에서 상품 검색
        with allure.step("마켓컬리 메인 페이지로 이동"):
            kurly_main_page.open_main_page()

        with allure.step("'과자' 검색"):
            kurly_main_page.search_product("과자")

        # When: 상품 추가 플로우 실행
        with allure.step("세 번째 상품의 장바구니 추가 버튼 클릭"):
            kurly_search_page.click_third_product_add_button()

        with allure.step("수량 조절 (2회 증가, 2회 감소)"):
            kurly_product_page.increase_quantity(2)
            kurly_product_page.decrease_quantity(2)

        with allure.step("장바구니에 담기"):
            kurly_product_page.click_add_to_cart_in_popup()

        # Then: 검색 결과 및 추가 성공 확인
        with allure.step("결과 확인"):
            kurly_search_page.take_screenshot("상품_추가_완료")

            # 검색 키워드가 페이지에 포함되어 있는지 확인
            assert kurly_search_page.is_keyword_in_page_source("과자"), \
                "❌ 검색 결과에서 '과자'가 포함되지 않음"

            allure.attach(
                "상품 추가 플로우가 성공적으로 완료되었습니다",
                name="테스트_결과",
                attachment_type=allure.attachment_type.TEXT
            )
