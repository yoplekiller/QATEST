# 2026-11-01 Selenium 스위트 고도화: StaleElement 근본 수정 · 실패 증거 · 병렬 · Flaky 가시화

## 무엇을 / 왜

10-18 이후 정기 CI 가 14일 중 6일 빨간불이었다. 실패 로그를 모아 보니 원인이 하나가 아니라 5갈래였고, 그중 4개는 **테스트 코드 결함**, 1개는 **사이트 결함**이었다.

| # | 증상 (CI 날짜) | 원인 | 구분 | 조치 |
|---|---|---|---|---|
| 1 | `StaleElementReferenceException` in `close_cart_popup` (10-28, 10-29, 로컬 재현 100%) | 담기를 누르면 **사이트가 팝업을 0.5~0.8초 안에 스스로 닫는데**(11-01 실측) 테스트는 닫히는 중인 팝업의 닫기 버튼을 찾아서 눌렀다 | 테스트 결함 | 팝업 DOM 이 사라지는 것(`staleness_of`)을 기다리고, 안 닫혔을 때만 **새로 찾은** 닫기 버튼으로 닫음 |
| 2 | `ElementClickIntercepted` - `div.css-1rnnmfr`(딤)가 클릭을 가로챔 (10-24) | `click()` 이 clickable 만 보고 눌렀다. clickable 은 "다른 요소에 가려졌는지"를 보장하지 않음 | 테스트 결함 | 클릭 지점의 최상단 요소가 자기 자신인지(`elementFromPoint`) 확인 후 클릭, stale/가림이면 **로케이터로 다시 찾아** 재시도 |
| 3 | 수량 테스트 "초기 2, 기대 3" (10-24) | ① 옵션 선택 헬퍼가 단일 상품에도 +를 눌러 1→2 로 만들었음(1,080원→2,160원 실측) ② 수량 클릭 함수가 예외를 삼키고(`return False`) 반영 여부를 확인 안 함 ③ 수량 표시 로케이터가 실제로는 빈 아이콘 div 를 가리킴 | 테스트 결함 | 첫 옵션 수량이 0일 때만 선택, 클릭마다 수량이 실제로 ±1 됐는지 확인(안 되면 값과 함께 실패), 로케이터 수정 |
| 4 | "3번째 장바구니 담기 버튼을 찾을 수 없음" (10-28) | 검색 결과 버튼 로케이터가 `'장바구니'` 포함 버튼을 다 잡아서, 팝업이 열려 있으면 **팝업 안 버튼까지 세었다** | 테스트 결함 | 팝업(`role=dialog`) 안 버튼 제외, 팝업 안 요소 로케이터는 전부 dialog 기준으로 좁힘 |
| 5 | 특수문자 검색 `' OR 1=1--` "페이지가 정상적으로 로드되지 않았습니다" (10-06~) | **이 검색어에만** 사이트가 "알 수 없는 에러가 발생했습니다" 일반 에러 페이지 + 빈 title 로 응답. `'` 단독, `OR 1=1` 은 정상 검색 → 보안 필터 차단으로 추정, 사용자에게 "결과 없음" 대신 에러 노출 | **사이트 결함** | `xfail(strict=True)` known issue 로 분리. 사이트가 고치면 XPASS 로 CI 가 깨져서 알려준다 |

그 위에 운영 개선 3가지를 얹었다: **실패 증거 자동 수집 / pytest-xdist 병렬 / 재시도 통과(flaky) 별도 집계**.

## 결과

| 항목 | 전 | 후 |
|---|---|---|
| 장바구니 관련 4개 테스트 반복 실행 | 3회 모두 2건 실패 (StaleElement, **6/6 실패**) | 5회 모두 4건 통과 (**20/20 통과**) |
| 위 4개 실행 시간 | 124~167초 | 84~100초 (고정 `sleep(2)` 제거, 값 폴링) |
| 전체 UI 스위트 (직렬) | 287초 · 3 failed / 18 passed / 3 skipped | 250초 · **20 passed** / 3 skipped / 1 xfailed(known issue) · flaky 0 |
| 전체 UI 스위트 (`-n 3 --dist loadfile`) | - | **115초** (직렬 대비 -54%) · 결과 동일 · flaky 0 |

## 핵심 코드

**① 찾아둔 요소를 재사용하지 않는 클릭** (`src/pages/base_page.py`)

```python
for attempt in range(3):
    try:
        element = self.wait_clickable(locator, timeout)   # 매 시도마다 새로 찾음
        self.wait_click_point_clear(element, timeout=2)   # 딤/토스트에 가려졌는지
        element.click()
        return
    except (StaleElementReferenceException, ElementClickInterceptedException) as e:
        time.sleep(0.5)                                     # 재렌더링 끝날 시간
```

**② 팝업이 "스스로 닫히는 것"을 기다리기** (`src/pages/kurly_search_page.py`)

```python
dialog = self.wait_present(self.ALT_DIALOG, timeout=5)
self.click(self.ADD_TO_CART_BUTTONS_IN_ALT)
toast_seen = ...  # '장바구니에 상품을 담았습니다' 토스트
if not self.wait_for_staleness(dialog, timeout=5):   # EC.staleness_of
    self.close_cart_popup()                            # 안 닫혔을 때만, 버튼은 새로 찾아서
return toast_seen
```

**③ 클릭이 반영됐는지 값으로 확인하는 스텝퍼**

```python
before = self.get_quantity_in_alt()
self.click(button_locator)
self._get_wait(5).until(lambda d: self._read_quantity_in_alt() == before + delta)
```

**④ 실패 증거 자동 수집** (`src/tests/conftest.py` - `pytest_runtest_makereport` 훅)
실패한 call 단계에서 스크린샷 · 현재 URL · page source · 브라우저 콘솔 로그를 Allure 에 첨부하고 `test-evidence/<테스트>/` 에도 저장 → CI 실패 시 artifact 로 업로드.

**⑤ Flaky 가시화** (`pytest_runtest_logreport` 훅)
pytest-rerunfailures 는 재시도 전 실패를 `outcome='rerun'` 으로 보고한다. 이걸 모아서 "재시도 후 통과"한 테스트를 `test_results_flaky.json` 에 남기고, 터미널 · GitHub Actions 요약 · Slack 에 **Flaky** 로 따로 표시한다. xdist 에서는 워커 리포트가 컨트롤러로 모이므로 컨트롤러에서만 파일을 쓴다.

## 검증 포인트 (어떤 assert 로 무엇을 확인하나)

| 테스트 | 전 | 후 |
|---|---|---|
| `test_add_goods_to_cart` | 페이지 소스에 "과자"가 있다 → **담기가 실패해도 통과** | 담기 성공 시에만 뜨는 토스트를 봤다 |
| `test_remove_item_from_cart` | 담은 후 개수 `> 0`, 삭제 후 `== 이전-1` | 비운 뒤 1종 담았으니 `== 1`, 삭제 후 `== 0` (값이 될 때까지 폴링) |
| `test_add_multiple_items_to_cart` | 담기 결과 확인 없음 | 상품마다 담기 토스트 확인 + 장바구니 개수 `== 3` |
| `test_quantity_buttons` | 최종 수량만 비교, 중간 클릭 씹힘은 묻힘 | 클릭마다 ±1 반영 확인, 안 되면 "X → Y 로 바뀌지 않음(현재 Z)" 로 실패 |
| `test_search_with_special_characters` | title 이 비어 있지 않다 | 에러 페이지가 아니다 + title 이 있다. `' OR 1=1--` 은 known issue(xfail strict) |

## 선택 이유

- **로케이터 재조회 vs 요소 재사용**: React 는 상태가 바뀌면 DOM 노드를 교체한다. 예전 참조를 계속 쓰면 stale 이 나므로, 요소가 아니라 **로케이터를 들고 다니다가 쓸 때 찾는다**. 테스트 쪽에 있던 `'stale' in str(e)` 문자열 매칭 재시도 루프는 지웠다(page object 가 책임).
- **`staleness_of` 로 닫힘 확인**: "닫기 버튼이 안 보인다"는 숨김(display:none)과 제거를 구분 못 하고, 이번처럼 사이트가 스스로 닫는 경우엔 버튼을 누를 필요가 없다. 처음에 잡아둔 dialog 노드가 DOM 에서 빠지는 것을 기다리는 게 의도와 정확히 맞는다.
- **dialog 기준 로케이터 (`//*[@role='dialog']//...`)**: 팝업 뒤 검색 결과 카드에도 비슷한 버튼이 있어서, 범위를 좁히지 않으면 "첫 번째로 매칭되는 것"이 엉뚱한 요소가 된다. role 속성은 해시 클래스(`css-xxxx`)보다 잘 안 바뀐다.
- **고정 sleep → 값 폴링**: 장바구니 개수는 진입 직후 0 이었다가 비동기로 채워진다. 기대값이 있으면 그 값이 될 때까지 폴링하는 게 빠르고(보통 1초 안) 느린 날에도 안 깨진다.
- **`xfail(strict=True)`**: 그냥 skip 하면 사이트가 고쳐져도 모른다. strict xfail 은 실패하면 known issue 로 통과 처리하고, 예상과 달리 통과하면(XPASS) 실패로 바꿔 알린다.
- **`--dist loadfile`**: 드라이버가 module scope 이고 같은 파일 안 테스트끼리 장바구니 상태를 이어 쓰므로 파일 단위로 워커에 배정한다. 워커마다 브라우저가 따로라 비회원 장바구니 쿠키도 격리된다. 실사이트 부담을 생각해 워커는 3개.
- **재시도 1회 + 별도 표시**: 실사이트라 네트워크 일시 오류는 생긴다. 재시도 없이 매번 빨간불이면 진짜 회귀가 묻히고, 재시도만 하면 불안정성이 숨는다 → 재시도는 하되 "재시도 후 통과"는 통과로 세지 않고 Flaky 로 따로 보고한다. Jira 자동 등록은 최종 `failed` 만 대상이라 flaky 로 티켓이 생기지 않는다.

## 면접 예상 질문 & 답

**Q. StaleElementReferenceException 은 왜 생기고 어떻게 해결했나요?**
A. 찾아둔 WebElement 가 가리키는 DOM 노드가 재렌더링으로 교체되면 생깁니다. 이번엔 장바구니 담기 후 사이트가 팝업을 스스로 닫는데 테스트가 닫히는 중인 팝업의 닫기 버튼을 누르려다 났습니다. 재시도로 덮지 않고 실제 동작을 확인해서, 팝업 노드가 사라지는 걸 `staleness_of` 로 기다리게 바꿨고, 공통 `click()` 은 매 시도마다 로케이터로 새로 찾도록 했습니다. 수정 전 3회 모두 실패하던 테스트가 수정 후 5회 모두 통과했습니다.

**Q. element_to_be_clickable 인데도 클릭이 가로채이는 이유는?**
A. clickable 은 보이고 활성화됐는지만 봅니다. 딤 레이어나 토스트가 위에 떠 있으면 클릭 좌표의 최상단 요소가 다른 요소라 가로채입니다. 그래서 `document.elementFromPoint` 로 클릭 지점의 최상단 요소가 대상인지 확인한 뒤 클릭합니다.

**Q. 재시도(rerun)를 넣으면 flaky 가 숨지 않나요?**
A. 그래서 재시도 후 통과한 테스트를 `rerun` 리포트로 따로 모아서 CI 요약과 Slack 에 Flaky 로 표시합니다. 통과로 세지 않고 "원인 확인 필요" 목록으로 남깁니다.

**Q. 사이트 결함과 테스트 결함은 어떻게 구분했나요?**
A. 실패를 로컬에서 재현하고 DOM 을 직접 조사했습니다. 특수문자 검색은 `'` 단독과 `OR 1=1` 은 정상이고 `' OR 1=1--` 조합에서만 에러 페이지가 떠서 사이트 동작으로 판단해 strict xfail 로 남겼고, 나머지 4건은 로케이터 범위·대기 방식·헬퍼 로직 문제라 테스트 코드를 고쳤습니다.

**Q. 병렬 실행할 때 주의한 점은?**
A. 테스트 간 공유 상태입니다. 드라이버가 module scope 라 같은 파일 테스트는 같은 브라우저를 쓰고 장바구니 상태를 이어 쓰기 때문에 `--dist loadfile` 로 파일 단위 배정을 했고, 워커마다 브라우저가 따로라 장바구니 쿠키가 섞이지 않습니다. 결과 파일(flaky 집계)은 컨트롤러에서만 쓰게 했습니다.

**Q. 기존 테스트에서 발견한 "검증이 약한" 부분은?**
A. 장바구니 담기 테스트가 "페이지 소스에 검색어가 있다"만 확인해서 담기가 실패해도 통과할 수 있었습니다. 담기 성공 시에만 뜨는 토스트로 검증하도록 바꿨고, 수량 클릭 함수가 예외를 삼키고 `False` 를 반환하는데 테스트가 반환값을 안 봐서 클릭 실패가 묻히던 것도 고쳤습니다.
