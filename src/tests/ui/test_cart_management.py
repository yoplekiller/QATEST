import pytest
import allure


@pytest.mark.ui
@allure.feature("장바구니 관리")
@allure.story("장바구니 상품 관리")
class TestCartManagement:
    """장바구니에서 상품 관리 기능 테스트"""

   
    @allure.title("여러 상품을 장바구니에 담기")
    @allure.description("여러 상품을 장바구니에 담고 모두 장바구니에 있는지 확인")
    # TC: TC-UI-025 (SC-UI-012)
    def test_add_multiple_items_to_cart(self, kurly_main_page, kurly_search_page, kurly_cart_page):
        """여러 상품을 장바구니에 담는 테스트"""
        try:
            with allure.step("장바구니 비우기(테스트 독립성 확보)"):
                kurly_cart_page.clear_cart()

            with allure.step("메인 페이지 접속"):
                kurly_main_page.open_main_page()

            with allure.step("'과자' 검색"):
                kurly_main_page.search_goods("과자")
                kurly_main_page.wait_until_url_contains("search", timeout=10)

            items_to_add = 3

            with allure.step(f"{items_to_add}개 상품을 장바구니에 담기"):
                # stale 대응은 page object(click_nth_add_button/add_to_cart_in_alt)가 로케이터
                # 재조회로 처리하므로, 테스트에서 'stale' 문자열을 잡아 재시도하던 루프는 제거했다.
                for i in range(2, items_to_add + 2):
                    kurly_search_page.click_nth_add_button(n=i)
                    assert kurly_search_page.add_to_cart_in_alt(), \
                        f"{i}번째 상품 담기 후 '장바구니에 상품을 담았습니다' 토스트가 보이지 않음"

            with allure.step("장바구니로 이동"):
                kurly_main_page.go_to_cart()

            with allure.step(f"장바구니에 {items_to_add}개 상품이 있는지 확인"):
                # 개수는 진입 직후 0이었다가 비동기로 채워짐 - 고정 sleep 대신 기대값까지 폴링
                cart_count = kurly_cart_page.wait_for_item_count(items_to_add)

                allure.attach(
                    f"예상: {items_to_add}개, 실제: {cart_count}개",
                    name="장바구니 상품 수",
                    attachment_type=allure.attachment_type.TEXT
                )

                assert cart_count == items_to_add, \
                    f"장바구니 상품 개수 불일치. 예상: {items_to_add}, 실제: {cart_count}"
        except Exception as e:
            kurly_cart_page.take_screenshot("장바구니_여러상품_실패")
            raise



    @allure.title("장바구니에서 상품 삭제")
    @allure.description("장바구니에 담긴 상품을 삭제하고 개수가 줄어드는지 확인")
    # TC: TC-UI-026 (SC-UI-012)
    def test_remove_item_from_cart(self, kurly_main_page, kurly_search_page, kurly_cart_page):
        """장바구니에서 상품 삭제 기능 테스트"""

        with allure.step("장바구니 비우기(테스트 독립성 확보)"):
            kurly_cart_page.clear_cart()

        with allure.step("메인 페이지 접속 및 검색"):
            kurly_main_page.open_main_page()
            kurly_main_page.search_goods("과자")
            kurly_main_page.wait_until_url_contains("search", timeout=10)


        with allure.step("상품을 장바구니에 담기"):
            kurly_search_page.click_nth_add_button(n=1)
            assert kurly_search_page.add_to_cart_in_alt(), \
                "담기 후 '장바구니에 상품을 담았습니다' 토스트가 보이지 않음"

        with allure.step("장바구니 페이지로 이동"):
            kurly_main_page.go_to_cart()

        with allure.step("장바구니에 상품이 있는지 확인"):
            # 비운 뒤 1종을 담았으므로 정확히 1이어야 한다(> 0 보다 강한 검증)
            initial_count = kurly_cart_page.wait_for_item_count(1)
            assert initial_count == 1, f"장바구니 상품 종류 수가 1이 아닙니다: {initial_count}"

            allure.attach(
                f"삭제 전 상품 개수: {initial_count}",
                name="초기 상태",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("상품 삭제"):
            kurly_cart_page.choiced_item_delete()

        with allure.step("상품이 삭제되었는지 확인"):
            final_count = kurly_cart_page.wait_for_item_count(initial_count - 1)

            allure.attach(
                f"삭제 후 상품 개수: {final_count}",
                name="최종 상태",
                attachment_type=allure.attachment_type.TEXT
            )

            assert final_count == initial_count - 1, \
                f"상품이 삭제되지 않았습니다. 이전: {initial_count}, 현재: {final_count}"