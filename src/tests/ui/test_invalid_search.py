import allure
import pytest


@pytest.mark.ui
@pytest.mark.skip(reason="검색어 'ㅁㄴㅇㄹ'로 검색 시 '검색된 상품이 없습니다' 메시지가 표시되지 않는 이슈 - '상품 메시지가 노출되지 않는 검색어 확인 필요")
@allure.feature("UI 테스트")
@allure.story("검색 실패 케이스")
@allure.title("잘못된 검색어로 검색 시 '검색 결과가 없습니다' 메시지 확인 테스트")
# TC: TC-UI-003 (SC-UI-005)
def test_search_invalid_good(kurly_main_page, kurly_search_page):
    """
    빈 검색어로 검색 시 '검색 결과가 없습니다' 메시지 확인 테스트
    """
    # Given: 메인 페이지 열기
    with allure.step("마켓컬리 메인 페이지 열기"):
        kurly_main_page.open_main_page()

    # When: 빈 검색어로 검색 시도
    with allure.step("잘못된 검색어로 검색 시도"):
        kurly_main_page.search_goods("ㅁㄴㅇㄹ")

    # Then: '검색 결과가 없습니다' 텍스트 확인
    with allure.step("'검색된 상품이 없습니다' 텍스트 확인"):
        assert kurly_search_page.is_no_result_message_displayed(), "❌ '검색된 상품이 없습니다' 메시지가 표시되지 않음"