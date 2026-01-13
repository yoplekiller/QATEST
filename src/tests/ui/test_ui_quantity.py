import allure
import pytest



@pytest.mark.ui
@allure.feature("상품 관리")
@allure.story("수량 조절")
@allure.severity(allure.severity_level.NORMAL)
class TestQuantity:

    @allure.title("수량 증가/감소 버튼 동작 확인")
    @allure.description("""
    **목적:** 상품 상세 팝업에서 수량 조절 버튼이 정상 작동하는지 확인

    **테스트 단계:**
    1. 마켓컬리 메인 페이지 접속
    2. '과자' 검색
    3. 세 번째 상품의 장바구니 추가 버튼 클릭
    4. 수량 올리기 버튼 2회 클릭
    5. 수량 내리기 버튼 1회 클릭
    6. 최종 수량이 2인지 확인

    **예상 결과:** 수량이 올바르게 조절됨 (최종 수량: 2)
    """)
    def test_quantity_buttons(self, kurly_main_page, kurly_search_page):
        """
        수량 증가/감소 버튼이 정상 작동하는지 확인
        """
    
        with allure.step("마켓컬리 메인 페이지로 이동"):
            kurly_main_page.open_main_page()

        with allure.step("'과자' 검색"):
            kurly_main_page.search_goods("과자")

        with allure.step("세 번째 상품의 장바구니 추가 버튼 클릭"):
            kurly_search_page.click_nth_add_button(3)


        with allure.step("수량 2회 증가"):
            kurly_search_page.quantity_up_in_alt(times=2)

        with allure.step("수량 1회 감소"):
            kurly_search_page.quantity_down_in_alt(times=1)


        with allure.step("최종 수량 확인"):
            assert kurly_search_page.is_diplayed_quantity_in_alt(2), "❌ 수량이 예상과 다릅니다"

            allure.attach(
                "수량 조절 버튼이 정상적으로 작동했습니다",
                name="테스트_결과",
                attachment_type=allure.attachment_type.TEXT
            )
