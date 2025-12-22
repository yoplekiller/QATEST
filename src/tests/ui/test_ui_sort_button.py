"""
정렬 기능 테스트 모듈
마켓컬리 검색 결과 페이지의 다양한 정렬 옵션이 정상 동작하는지 검증
"""
import allure
from src.pages.kurly_main_page import KurlyMainPage
from src.pages.kurly_search_page import KurlySearchPage
import pytest


@pytest.mark.ui
@pytest.mark.parametrize("sort_type", ["recommend", "new", "low_price", "high_price"])
@allure.title("정렬 옵션 테스트: {sort_type}")
@allure.feature("검색 및 필터링")
@allure.story("상품 정렬")
@allure.severity(allure.severity_level.NORMAL)
def test_all_sort_options(driver, sort_type):
    """
    검색 결과에서 모든 정렬 옵션이 정상 동작하는지 확인

    테스트 시나리오:
        1. 마켓컬리 메인 페이지 접속
        2. 특정 키워드('과자')로 검색
        3. 정렬 옵션 선택 (추천순/신상품순/낮은가격순/높은가격순)
        4. 정렬이 올바르게 적용되었는지 확인

    Args:
        driver: WebDriver fixture
        sort_type: 테스트할 정렬 타입
            - recommend: 추천순
            - new: 신상품순
            - low_price: 낮은 가격순
            - high_price: 높은 가격순

    Expected:
        선택한 정렬 옵션에 따라 상품 목록이 올바르게 정렬됨
    """

    main_page = KurlyMainPage(driver)
    search_page = KurlySearchPage(driver)

    with allure.step("마켓컬리 메인 페이지로 이동"):
        main_page.open_main_page()

    with allure.step("상품 검색"):
        main_page.search_product("과자")

    with allure.step(f"정렬 옵션 '{sort_type}' 선택"):
        search_page.select_sort_option(sort_type)

    with allure.step("정렬 결과 확인"):
        assert search_page.is_sorted_correctly(sort_type), f"❌ '{sort_type}' 정렬이 올바르게 적용되지 않음"

    