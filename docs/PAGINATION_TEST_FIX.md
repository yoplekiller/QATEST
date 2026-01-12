# 페이지네이션 테스트 수정 내역

**작성일:** 2026년 1월 1일
**파일:** `src/tests/api/test_movie_pagination.py`

---

## 📋 수정 개요

TMDB API의 페이지네이션 에러 처리 방식이 변경되어, 잘못된 페이지 번호에 대해 400 에러를 반환하도록 업데이트되었습니다. 이에 따라 관련 테스트를 수정했습니다.

---

## 🔍 발견된 문제

### 1. API 동작 변경
**이전 동작 (예상):**
- `page=0` → 자동으로 `page=1`로 처리
- `page=999` → 빈 결과 또는 마지막 페이지 반환

**현재 동작 (실제):**
- `page=0` → **HTTP 400 에러** 반환
- `page=999` → **HTTP 400 에러** 반환 (최대 500페이지)

### 2. 에러 응답 형식
```json
{
  "success": false,
  "status_code": 22,
  "status_message": "Invalid page: Pages start at 1 and max at 500. They are expected to be an integer."
}
```

### 3. 디버그 로그
```
DEBUG urllib3.connectionpool https://api.themoviedb.org:443
"GET /3/movie/popular?api_key=xxx&page=0 HTTP/1.1" 400 None
```

---

## 🔧 수정 내용

### 수정 1: `test_pagination_invalid_page_zero`

**위치:** Line 75-99

#### 수정 전
```python
@allure.title("잘못된 페이지 번호 - 0 이하")
@allure.description("페이지 번호가 0 이하일 때 에러 처리 또는 기본값으로 처리되는지 검증")
def test_pagination_invalid_page_zero(self, api_env, send_get_request):
    """페이지 번호 0 요청 시 처리"""

    API_KEY = api_env.api_key

    endpoint = "/movie/popular"
    params = {
        "api_key": API_KEY,
        "page": 0
    }

    with allure.step("GET 요청: page=0"):
        response = send_get_request(endpoint, params=params)  # ❌ 에러 시 예외 발생

    data = response.json()

    with allure.step("응답 검증 (페이지 1로 처리되거나 에러)"):
        # TMDB API는 page=0을 page=1로 처리함
        assert data["page"] >= 1, "페이지는 1 이상이어야 합니다"  # ❌ 잘못된 기대
```

#### 수정 후
```python
@allure.title("잘못된 페이지 번호 - 0 이하")
@allure.description("페이지 번호가 0 이하일 때 에러 응답을 반환하는지 검증")
def test_pagination_invalid_page_zero(self, api_env):
    """페이지 번호 0 요청 시 400 에러 반환"""

    API_KEY = api_env.api_key

    endpoint = "/movie/popular"
    params = {
        "api_key": API_KEY,
        "page": 0
    }

    with allure.step("GET 요청: page=0"):
        response = api_env.send_get_request_no_raise(endpoint, params=params)  # ✅ 에러 응답도 반환

    with allure.step("400 에러 응답 검증"):
        assert response.status_code == 400, f"예상: 400, 실제: {response.status_code}"  # ✅ 400 검증

    data = response.json()

    with allure.step("에러 메시지 검증"):
        assert data["success"] == False, "success 필드가 False여야 합니다"
        assert "status_code" in data, "status_code 필드가 있어야 합니다"
        assert "status_message" in data, "status_message 필드가 있어야 합니다"  # ✅ 에러 구조 검증
```

#### 주요 변경사항
1. **메서드 변경:**
   - `send_get_request()` → `api_env.send_get_request_no_raise()`
   - 이유: 400 에러 시 예외를 발생시키지 않고 응답을 반환

2. **픽스처 제거:**
   - `send_get_request` 픽스처 제거
   - `api_env` 객체에서 직접 메서드 호출

3. **검증 로직 변경:**
   - 200 응답 + page=1 처리 기대 → **400 에러 응답 검증**
   - 에러 응답 구조 검증 추가

---

### 수정 2: `test_pagination_out_of_range`

**위치:** Line 102-126

#### 수정 전
```python
@allure.title("범위 초과 페이지 번호")
@allure.description("존재하지 않는 큰 페이지 번호 요청 시 처리 검증")
def test_pagination_out_of_range(self, api_env, send_get_request):
    """범위를 초과한 페이지 번호 요청"""

    API_KEY = api_env.api_key

    endpoint = "/movie/popular"
    params = {
        "api_key": API_KEY,
        "page": 999
    }

    with allure.step("GET 요청: page=999"):
        response = send_get_request(endpoint, params=params)  # ❌ 에러 시 예외 발생

    data = response.json()

    with allure.step("응답 검증"):
        # 범위 초과 시 빈 결과 또는 마지막 페이지 반환
        assert response.status_code == 200, "상태 코드는 200이어야 합니다"  # ❌ 잘못된 기대
        if data["results"]:
            assert data["page"] <= data["total_pages"], \
                "페이지 번호는 총 페이지 수를 초과할 수 없습니다"

    with allure.step("결과 항목 수 검증"):
        assert "results" in data, "검색 실패"
        assert len(data["results"]) > 0, "영화 결과가 없습니다"  # ❌ 빈 결과 가정
```

#### 수정 후
```python
@allure.title("범위 초과 페이지 번호")
@allure.description("페이지 번호가 500 초과일 때 에러 응답을 반환하는지 검증")
def test_pagination_out_of_range(self, api_env):
    """범위를 초과한 페이지 번호(>500) 요청 시 400 에러 반환"""

    API_KEY = api_env.api_key

    endpoint = "/movie/popular"
    params = {
        "api_key": API_KEY,
        "page": 999
    }

    with allure.step("GET 요청: page=999"):
        response = api_env.send_get_request_no_raise(endpoint, params=params)  # ✅ 에러 응답도 반환

    with allure.step("400 에러 응답 검증"):
        assert response.status_code == 400, f"예상: 400, 실제: {response.status_code}"  # ✅ 400 검증

    data = response.json()

    with allure.step("에러 메시지 검증"):
        assert data["success"] == False, "success 필드가 False여야 합니다"
        assert data["status_code"] == 22, "status_code는 22(Invalid page)여야 합니다"  # ✅ 에러 코드 검증
        assert "Invalid page" in data["status_message"], \
            "에러 메시지에 'Invalid page'가 포함되어야 합니다"  # ✅ 메시지 검증
```

#### 주요 변경사항
1. **메서드 변경:**
   - `send_get_request()` → `api_env.send_get_request_no_raise()`

2. **픽스처 제거:**
   - `send_get_request` 픽스처 제거

3. **검증 로직 변경:**
   - 200 응답 + 빈 결과/마지막 페이지 기대 → **400 에러 응답 검증**
   - TMDB API 에러 코드 22 (Invalid page) 검증
   - 에러 메시지 내용 검증 ("Invalid page" 포함)

---

## 📊 비교 표

| 항목 | 수정 전 | 수정 후 |
|------|---------|---------|
| **사용 메서드** | `send_get_request()` | `api_env.send_get_request_no_raise()` |
| **예상 응답** | HTTP 200 (정상 처리) | HTTP 400 (에러) |
| **page=0 처리** | page=1로 자동 변환 기대 | 400 에러 반환 검증 |
| **page=999 처리** | 빈 결과 또는 마지막 페이지 기대 | 400 에러 반환 검증 |
| **에러 구조 검증** | 없음 | `success`, `status_code`, `status_message` 검증 |
| **TMDB 에러 코드** | 미검증 | 22 (Invalid page) 검증 |

---

## ✅ 테스트 목적 변경

### 수정 전: Graceful Degradation 테스트
- API가 잘못된 입력을 자동으로 보정하는지 확인
- 예: page=0 → page=1로 처리

### 수정 후: Error Handling 테스트
- API가 잘못된 입력에 대해 적절한 에러를 반환하는지 확인
- 에러 응답의 구조와 메시지가 명확한지 검증

---

## 🔗 관련 파일

- **수정 파일:** `src/tests/api/test_movie_pagination.py`
- **사용 클래스:** `utils/api_utils.py::APIEnv`
- **사용 메서드:** `send_get_request_no_raise()`

---

## 📝 참고사항

### TMDB API 페이지네이션 제약사항
- **최소 페이지:** 1
- **최대 페이지:** 500
- **유효하지 않은 페이지 요청 시:** HTTP 400 + status_code 22

### send_get_request_no_raise() 메서드
```python
@allure.step("GET 요청 보내기 (상태 코드 확인하지 않음)")
def send_get_request_no_raise(self, endpoint, params=None, headers=None):
    """상태 코드를 확인하지 않고 응답을 반환하는 GET 요청 함수"""
    full_url = self.base_url + endpoint
    response = requests.get(full_url, params=params, headers=headers)
    self.attach_response(response)
    return response  # raise_for_status() 호출하지 않음
```

**특징:**
- `response.raise_for_status()` 호출 안 함
- 4xx, 5xx 에러 응답도 정상적으로 반환
- 에러 응답 테스트에 적합

---

## 🎯 테스트 시나리오

### Test Case 1: page=0
```
Given: TMDB API에 인기 영화 목록 요청
When: page=0으로 요청
Then: HTTP 400 반환 + "Invalid page" 에러 메시지
```

### Test Case 2: page=999
```
Given: TMDB API에 인기 영화 목록 요청
When: page=999로 요청 (최대 500 초과)
Then: HTTP 400 반환 + status_code 22 + "Invalid page" 메시지
```

---

## 🚀 향후 추가 가능한 테스트

1. **음수 페이지 테스트**
   ```python
   params = {"page": -1}
   # 예상: 400 에러
   ```

2. **문자열 페이지 테스트**
   ```python
   params = {"page": "abc"}
   # 예상: 400 에러
   ```

3. **소수점 페이지 테스트**
   ```python
   params = {"page": 1.5}
   # 예상: 400 에러 또는 정수로 자동 변환
   ```

4. **경계값 테스트**
   ```python
   params = {"page": 500}  # 최대값
   params = {"page": 501}  # 최대값 + 1
   ```

---

**수정 완료일:** 2026년 1월 1일
**테스트 상태:** 미실행 (API 키 설정 필요)
