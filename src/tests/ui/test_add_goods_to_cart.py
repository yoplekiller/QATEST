import allure
import pytest


@pytest.mark.ui
@allure.feature("장바구니 기능")
@allure.story("상품 추가 플로우")
@allure.title("상품을 장바구니에 추가하는 전체 플로우 테스트")
def test_add_good_to_cart_flow(kurly_main_page, kurly_search_page, kurly_goods_page):
    """
    상품을 장바구니에 추가하는 전체 플로우 테스트
    Steps:
        1. 상품 검색
        2. 세 번째 상품의 추가 버튼 클릭
        3. 수량 2회 증가
        4. 수량 2회 감소
        5. 장바구니에 담기
    """
    increase_count = 2
    decrease_count = 2

    # 1. 메인 페이지 열고 검색
    with allure.step("메인 페이지 접속"):
        kurly_main_page.open_main_page()

    with allure.step("'과자' 검색"):
        kurly_main_page.search_goods("과자")

    # 2. 상품 추가 버튼 클릭
    with allure.step("세 번째 상품 담기 버튼 클릭"):
        kurly_search_page.click_nth_add_button(3)

    # 3. 수량 올리기
    with allure.step(f"수량 {increase_count}회 증가"):
        kurly_search_page.quantity_up_in_alt(increase_count)

    # 4. 수량 내리기
    with allure.step(f"수량 {decrease_count}회 감소"):
        kurly_search_page.quantity_down_in_alt(decrease_count)
    # 5. 장바구니 담기
    with allure.step("장바구니에 담기"):
        kurly_search_page.add_to_cart_in_alt()

    # 6. 성공 검증
    with allure.step("장바구니 담기 성공 확인"):
        assert kurly_search_page.is_add_to_cart_success(), "장바구니 담기가 실패했습니다"