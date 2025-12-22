from src.pages.kurly_main_page import KurlyMainPage
import allure
import pytest


@pytest.mark.ui
@allure.feature("UI 테스트")
@allure.story("검색 실패 케이스")
def test_search_invalid_product(driver):
    """
    빈 검색어로 검색 시 '검색 결과가 없습니다' 메시지 확인 테스트
    """
    main_page = KurlyMainPage(driver)

    # Given: 메인 페이지 열기
    with allure.step("마켓컬리 메인 페이지 열기"):
        main_page.open_main_page()

    # When: 빈 검색어로 검색 시도
    with allure.step("잘못된 검색어로 검색 시도"):
        main_page.search_product("ㅁㄴㅇㄹ")

    # Then: '검색 결과가 없습니다' 메시지 확인
    with allure.step("'검색된 상품이 없습니다' 메시지 확인"):
        assert main_page.is_no_result_message_displayed(), "❌ '검색된 상품이 없습니다' 메시지가 표시되지 않음"