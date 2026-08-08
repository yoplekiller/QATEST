import allure
import pytest

@pytest.mark.ui
@allure.feature("UI 테스트")
@allure.story("검색 실패 케이스")
@allure.title("빈 검색어로 검색 시 '검색어를 입력해주세요' 알럿 확인 테스트")
def test_search_invalid_search(kurly_main_page):
    """
    빈 검색어로 검색 시 '검색어를 입력해주세요' 알럿 확인 테스트
    """
    try:
        with allure.step("마켓컬리 메인 페이지 열기"):
            kurly_main_page.open_main_page()

        with allure.step("빈 검색어로 검색 시도"):
            kurly_main_page.search_goods("")
      
        with allure.step("'검색어를 입력해주세요' 알럿 확인"):
            assert kurly_main_page.is_search_keyword_required_popup_displayed(), "❌ '검색어를 입력해주세요' 알럿이 표시되지 않음"
    except Exception as e:
        kurly_main_page.take_screenshot("빈 검색어_알럿_실패")
        raise