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
    # TC: TC-UI-021, TC-UI-022 (SC-UI-012)
    def test_quantity_buttons(self, kurly_main_page, kurly_search_page):
        """
        수량 증가/감소 버튼이 정상 작동하는지 확인
        """
        try:
            with allure.step("마켓컬리 메인 페이지로 이동"):
                kurly_main_page.open_main_page()

            with allure.step("'과자' 검색"):
                kurly_main_page.search_goods("과자")
                kurly_main_page.wait_until_url_contains("search", timeout=10)

            with allure.step("세 번째 상품의 장바구니 추가 버튼 클릭"):
                kurly_search_page.click_nth_add_button(3)
                kurly_search_page.wait_visible(kurly_search_page.ADD_TO_CART_BUTTONS_IN_ALT, timeout=10)
                # 옵션형 상품(예: "~종 (택1)")은 아무 옵션도 선택 안 하면 수량이
                # 0으로 남아있어 스텝퍼 클릭 시 레이아웃이 바뀌며 클릭이 씹히는
                # 문제가 있었음(실측, 2026-09-20) - 미리 첫 옵션을 선택해 단일
                # 상품과 동일한 조건으로 맞춘다.
                kurly_search_page.select_first_option_if_needed()

            with allure.step("초기 수량 확인"):
                # 옵션형 상품은 0, 단일 상품은 1부터 시작하는 등 상품에 따라
                # 시작 수량이 달라서(실사이트 확인, 2026-09-20) 고정값 대신
                # 실제 시작값 기준 상대 변화(+2-1=+1)로 검증한다.
                initial_quantity = int(kurly_search_page.get_text(kurly_search_page.QUANTITY_DISPLAY_IN_ALT))

            with allure.step("수량 2회 증가"):
                kurly_search_page.quantity_up_in_alt(times=2)

            with allure.step("수량 1회 감소"):
                kurly_search_page.quantity_down_in_alt(times=1)

            with allure.step("최종 수량 확인"):
                expected_quantity = initial_quantity + 1
                assert kurly_search_page.is_diplayed_quantity_in_alt(expected_quantity), \
                    f"❌ 수량이 예상과 다릅니다 (초기: {initial_quantity}, 기대: {expected_quantity})"

                allure.attach(
                    "수량 조절 버튼이 정상적으로 작동했습니다",
                    name="테스트_결과",
                    attachment_type=allure.attachment_type.TEXT
                )
        except Exception as e:
            kurly_search_page.take_screenshot("수량조절_실패")
            raise
