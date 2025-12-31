import pytest
import allure
import time


@pytest.mark.ui
@allure.feature("장바구니 관리")
@allure.story("장바구니 상품 관리")
class TestCartManagement:
    """장바구니에서 상품 관리 기능 테스트"""

   
    @allure.title("여러 상품을 장바구니에 담기")
    @allure.description("여러 상품을 장바구니에 담고 모두 장바구니에 있는지 확인")
    def test_add_multiple_items_to_cart(self, kurly_main_page, kurly_search_page, kurly_cart_page):
          """여러 상품을 장바구니에 담는 테스트"""

          with allure.step("메인 페이지 접속"):
              kurly_main_page.open_main_page()

          with allure.step("'과자' 검색"):
              kurly_main_page.search_product("과자")

          items_to_add = 3

          with allure.step(f"{items_to_add}개 상품을 장바구니에 담기"):
              for i in range(2, items_to_add + 2):
                  retry = 0
                  while retry < 2:
                      try:
                          kurly_search_page.click_nth_add_button(n=i)
                          kurly_search_page.click_add_to_cart_in_alt()
                          time.sleep(1)  # 팝업 닫힐 때까지 대기
                          break
                      except Exception as e:
                          if 'stale element reference' in str(e).lower():
                              time.sleep(1)
                              retry += 1
                          else:
                              raise

          with allure.step("장바구니로 이동"):
              kurly_main_page.go_to_cart()
              time.sleep(2)  # 페이지 로드 대기

          with allure.step(f"장바구니에 {items_to_add}개 상품이 있는지 확인"):
              cart_count = kurly_cart_page.get_cart_item_count()

              allure.attach(
                  f"예상: {items_to_add}개, 실제: {cart_count}개",
                  name="장바구니 상품 수",
                  attachment_type=allure.attachment_type.TEXT
              )

              assert cart_count == items_to_add, \
                  f"장바구니 상품 개수 불일치. 예상: {items_to_add}, 실제: {cart_count}"


    @allure.title("장바구니에서 상품 삭제")
    @allure.description("장바구니에 담긴 상품을 삭제하고 개수가 줄어드는지 확인")
    def test_remove_item_from_cart(self, kurly_main_page, kurly_search_page, kurly_cart_page):
        """장바구니에서 상품 삭제 기능 테스트"""

        with allure.step("메인 페이지 접속 및 검색"):
            kurly_main_page.open_main_page()
            kurly_main_page.search_product("과자")

        with allure.step("상품을 장바구니에 담기"):
            kurly_search_page.click_nth_add_button(n=1)
            kurly_search_page.click_add_to_cart_in_alt()

        with allure.step("장바구니 페이지로 이동"):
            kurly_cart_page.go_to_cart()    

        with allure.step("장바구니에 상품이 있는지 확인"):
            initial_count = kurly_cart_page.get_cart_item_count()
            assert initial_count > 0, "장바구니에 상품이 없습니다"

            allure.attach(
                f"삭제 전 상품 개수: {initial_count}",
                name="초기 상태",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("첫 번째 상품 삭제"):
            kurly_cart_page.remove_first_item()
            time.sleep(1)  # 삭제 처리 대기

        with allure.step("상품이 삭제되었는지 확인"):
            final_count = kurly_cart_page.get_cart_item_count()

            allure.attach(
                f"삭제 후 상품 개수: {final_count}",
                name="최종 상태",
                attachment_type=allure.attachment_type.TEXT
            )

            assert final_count == initial_count - 1, \
                f"상품이 삭제되지 않았습니다. 이전: {initial_count}, 현재: {final_count}"