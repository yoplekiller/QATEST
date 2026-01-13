"""
검색 기능 테스트 (POM 패턴 적용)
Page Object Model을 사용하여 리팩토링된 검색 테스트
"""
import allure
import pytest


@pytest.mark.ui
@allure.feature("상품 검색")
@allure.story("검색 기능")
@allure.severity(allure.severity_level.CRITICAL)
class TestSearch:

    @allure.title("정상적인 검색어로 상품 검색")
    @allure.description("""
    **목적:** 유효한 검색어로 검색 시 적절한 검색 결과가 표시되는지 확인

    **테스트 단계:**
    1. 마켓컬리 메인 페이지 접속
    2. 검색창에 검색어 입력 (예: "사과")
    3. 검색 버튼 클릭
    4. 검색 결과 확인

    **예상 결과:** 검색어와 관련된 상품이 1개 이상 표시됨
    """)
    @pytest.mark.parametrize("keyword", ["사과", "우유", "계란"])
    def test_search_valid_keyword(self, kurly_main_page, kurly_search_page, keyword):
        """
        유효한 검색어로 검색 시 결과가 표시되는지 확인
        """
       
        with allure.step("마켓컬리 메인 페이지로 이동"):
            kurly_main_page.open_main_page()
            
       
        with allure.step(f"'{keyword}' 검색"):
            kurly_main_page.search_goods(keyword)
           

        
        with allure.step("검색 결과 확인"):
            kurly_search_page.take_screenshot(f"{keyword}_검색_결과")
            results_count = kurly_search_page.get_goods_count()
            assert kurly_search_page.is_check_url(keyword), "❌ 검색 결과 페이지로 이동하지 않았습니다"
            

            allure.attach(
                f"검색 결과 개수: {results_count}",
                name="검색_결과_개수",
                attachment_type=allure.attachment_type.TEXT
            )

            assert results_count > 0, f"❌ '{keyword}' 검색 결과가 없습니다"

    @allure.title("빈 검색어로 검색 시도")
    @allure.description("""
    **목적:** 빈 검색어로 검색 시 적절한 처리가 되는지 확인

    **테스트 단계:**
    1. 마켓컬리 메인 페이지 접속
    2. 검색창에 아무것도 입력하지 않음
    3. 검색 버튼 클릭
    4. 에러 처리 또는 기본 페이지 유지 확인

    **예상 결과:** 검색이 실행되지 않거나 에러 메시지 표시
    """)
    def test_search_with_empty_keyword(self, kurly_main_page):
        """
        빈 검색어로 검색 시 적절한 처리가 되는지 확인
        """
        
        kurly_main_page.open_main_page()
        initial_url = kurly_main_page.get_current_url()

        
        with allure.step("빈 검색어로 검색 시도"):
            kurly_main_page.enter_search_keyword("")
            kurly_main_page.click_search_button()

       
        with allure.step("에러 처리 확인"):
            kurly_main_page.take_screenshot("빈_검색어_검색")

            current_url = kurly_main_page.get_current_url()
            # URL이 변경되지 않았거나, 검색 결과 페이지에서 "결과 없음" 표시
            assert initial_url == current_url or kurly_main_page.is_search_keyword_required_popup_displayed(), \
                "❌ 빈 검색어에 대한 적절한 처리가 없습니다"

    @allure.title("존재하지 않는 상품명으로 검색")
    @allure.description("""
    **목적:** 존재하지 않는 상품명으로 검색 시 '결과 없음' 메시지가 표시되는지 확인

    **테스트 단계:**
    1. 마켓컬리 메인 페이지 접속
    2. 검색창에 존재하지 않는 상품명 입력
    3. 검색 버튼 클릭
    4. "검색 결과가 없습니다" 메시지 확인

    **예상 결과:** 검색 결과가 없다는 메시지가 표시됨
    """)
    @pytest.mark.parametrize("keyword", ["xyzabc123", "!@#$%", "가나다라마바사아자차카타파하"])
    def test_search_non_existent_good(self,kurly_main_page, kurly_search_page, keyword):
        """
        존재하지 않는 상품명으로 검색 시 적절한 메시지가 표시되는지 확인
        """
       
        kurly_main_page.open_main_page()

        
        with allure.step(f"'{keyword}' 검색"):
            kurly_main_page.search_goods(keyword)
        
        with allure.step("검색 결과 없음 확인"):
            kurly_search_page.take_screenshot(f"{keyword}_검색_결과_없음")

            results_count = kurly_search_page.get_goods_count()
            has_no_results_message = kurly_search_page.is_no_result_message_displayed()

            allure.attach(
                f"검색 결과 개수: {results_count}\n결과 없음 메시지: {has_no_results_message}",
                name="검색_결과_정보",
                attachment_type=allure.attachment_type.TEXT
            )

            assert results_count == 0 or has_no_results_message, \
                f"❌ '{keyword}' 검색 시 결과가 없어야 하는데 {results_count}개가 표시됨"

    @allure.title("검색 후 첫 번째 상품 클릭")
    @allure.description("""
    **목적:** 검색 결과에서 상품을 클릭하여 상세 페이지로 이동할 수 있는지 확인

    **테스트 단계:**
    1. 마켓컬리 메인 페이지 접속
    2. 검색창에 검색어 입력
    3. 검색 실행
    4. 첫 번째 검색 결과 클릭
    5. 상세 페이지로 이동 확인

    **예상 결과:** 상품 상세 페이지로 정상 이동
    """)
    def test_search_and_click_first_result(self, kurly_main_page, kurly_search_page):
        """
        검색 후 첫 번째 결과를 클릭하여 상세 페이지로 이동
        """
        
        with allure.step("메인 페이지에서 검색"):
            kurly_main_page.open_main_page()
            kurly_main_page.search_goods("사과")
            # 검색 페이지로 이동 대기
            kurly_search_page.wait_until_url_contains("/search", timeout=10)

        
        with allure.step("첫 번째 검색 결과 클릭"):
            initial_url = kurly_search_page.get_current_url()
            kurly_search_page.click_first_good()

        
        with allure.step("상세 페이지 이동 확인"):
            kurly_search_page.take_screenshot("상품_상세_페이지")

            current_url = kurly_search_page.get_current_url()
            assert current_url != initial_url, \
                "❌ 상품 클릭 후 페이지가 변경되지 않았습니다"

    @allure.title("특수문자 검색 처리")
    @allure.description("""
    **목적:** 특수문자를 포함한 검색어에 대한 적절한 처리 확인

    **테스트 단계:**
    1. 마켓컬리 메인 페이지 접속
    2. 특수문자가 포함된 검색어 입력
    3. 검색 실행
    4. 에러 없이 검색이 완료되는지 확인

    **예상 결과:** 에러 없이 검색이 수행되며, 결과가 있거나 "결과 없음" 메시지 표시
    """)
    @pytest.mark.parametrize("keyword", ["<script>", "' OR 1=1--", "사과!@#"])
    def test_search_with_special_characters(self, kurly_main_page, keyword):
        """
        특수문자를 포함한 검색어 처리 확인
        """
        # Given: 메인 페이지로 이동
        kurly_main_page.open_main_page()

        # When: 특수문자 포함 검색어로 검색
        with allure.step(f"특수문자 포함 검색어 '{keyword}' 검색"):
            kurly_main_page.search_goods(keyword)

        # Then: 에러 없이 검색이 완료되어야 함
        with allure.step("검색 처리 확인"):
            kurly_main_page.take_screenshot(f"특수문자_검색_{keyword}")

            # 페이지가 정상적으로 로드되었는지 확인
            page_title = kurly_main_page.get_title()
            assert page_title, "❌ 페이지가 정상적으로 로드되지 않았습니다"
