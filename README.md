# QA 자동화 포트폴리오 프로젝트

## 📀 프로젝트 개요
반복적인 수동 테스트를 자동화하기 위해 Python 기반으로 구현한 QA 테스트 자동화 포트폴리오입니다.
실제 웹 서비스인 마켓컬리를 대상으로 Selenium UI 테스트를 수행하였고,
별도로 **영화 정보 API(TMDB)**를 활용한 API 테스트도 포함되어 있습니다.
테스트 결과는 Allure Report로 시각화되며, Excel 파일로 저장되고, Slack으로 자동 보고됩니다.

## 👨‍💻 담당 역할
테스트 자동화 설계 및 구현
GitHub Actions 기반 CI 파이프라인 구축
Excel 자동 리포트 및 Slack 테스트 결과 메시지 전송 기능 구축

## 🧱 프로젝트 구성
### 1. 마켓컬리 웹 테스트 (Selenium)
상품 검색, 장바구니 추가, 카테고리 버튼 클릭, 로그인 실패 등 다양한 시나리오 테스트
주요 테스트 포인트: UI 요소 접근, XPath 활용, 동작 여부 및 상품 정보 확인

### 2. 영화 API 테스트
TMDB(Open API) 기반 GET 요청 검증
테스트 항목: 영화 검색, 장르 분류, 상세 조회
검증 요소: 응답 코드, 응답 시간(SLA), 필수 키 존재 여부 등
-
## 🧰 사용 기술
Python, Selenium, requests, openpyxl, Slack Webhook, Docker, GitHub Actions, Allure Report


-------------------------------------------------------
## 📁 디렉토리 구조
<pre>src/
├── report/
│   └── generate_excel_report.py
├── tests/
│   ├── api_tests/
│   │   ├── test_api_sla.py
│   │   ├── test_movie_invalid_api_key.py
│   │   ├── test_movie_details.py
│   │   ├── test_popular_movie.py
│   │   └── test_search_movie.py
│   ├── ui_tests/
│   │   ├── test_blank_search.py
│   │   ├── test_fail_screenshot.py
│   │   ├── test_invalid_search.py
│   │   ├── test_ui_add_product.py
│   │   ├── test_ui_cart.py
│   │   ├── test_ui_category.py
│   │   ├── test_ui_login.py
│   │   ├── test_ui_login_success.py
│   │   ├── test_ui_quantity.py
│   │   └── test_ui_search.py
│   └── testcases/
│       └── test_case.xlsx
utils/
├── api_utils.py
├── config_utils.py
├── parse_test_result.py
├── read_movie_data.py
├── read_product_data.py
├── send_slack_result.py
└── utilities.py
</pre>
-------------------------------------
## ✅ 주요 기능
- 테스트 결과를 Excel로 정리
- 테스트 완료 시 Slack으로 자동 전송
- Docker로 통합 실행 환경 구성
--------------------------------------
## 🧪 테스트 시나리오 예시

### 🛒 마켓컬리

상품 검색 → 검색 결과 확인 및 장바구니 추가 후 이동 확인
잘못된 로그인 → 오류 메시지 노출 확인
카테고리 버튼 클릭 → 해당 리스트 정상 노출
여러 상품 검색 → 각 검색 결과 확인
공백 검색 → 동작 여부 검증
결과 없는 검색어 입력 → 참조 메시지 확인
장바구니 버튼 클릭 → 장바구니 페이지 이동 확인

### 🎥 영화 API
특정 ID 입력 후 해당 영화 검색
인기 영화 API 검증 (응답코드 200)
검색 결과의 영화 ID를 이용해 상세검색 결과 보고

## ▶ 실행 방법
### 🔧 로컬 환경 (PyCharm 기준)
프로젝트 디렉토리를 PyCharm으로 열기
Python 인터프리터 및 가상환경 설정
requirements.txt로 의존성 설치
원하는 테스트 파일 실행
UI 테스트: pytest src/tests/ui_tests/
API 테스트는 보안상 CI 환경(GitHub Actions)에서만 실행


## 🧪 테스트 시나리오 예시

### 🛒 마켓컬리
- 상품 검색 후 장바구니 추가 → 장바구니 페이지 이동 확인
- 잘못된 로그인 시도 → 오류 메시지 노출 여부 확인
- 상품 카테고리 버튼 클릭 → 해당 상품 리스트 노출 확인
- 여러가지 상품 검색 → 검색한 상품 결과 노출 확인
- 공백 검색 후 → 동작 확인
- 결과 없는 검색어 검색 후 결과 페이지 확인
- 장바구니 아이콘 버튼 클릭 → 장바구니 페이지 노출 확인

### 🎬 영화 API
- 특정 영화 ID 값 입력 → 응답 내 영화 데이터 확인
- 영화 상세 정보 요청 → 제목, 평점, 개봉일 등의 필드 확인
- 인기 영화 목록 입력 → 응답 값 200 반환되는 지 확인
- 검색된 영화에서 ID 추출 → 해당 ID로 상세조회 후 동일한 제목인지 확인


## 🔮 TODO
- ⬜ OWASP ZAP 도구를 활용한 보안 테스트 통합
- ⬜ API 테스트 케이스 추가 및 에러 시나리오 강화
- ⬜ Docker 환경 최적화 및 다중 서비스 분리 실행
- ⬜ 테스트 실패 시 자동 이슈 생성 기능 연동 (ex. GitHub Issues, Jira)



## 🤷‍♀️ 결과
📄 Allure Report 보기: https://yoplekiller.github.io/QATEST/allure-report/main/index.html

## 📹 테스트 자동화 시연 영상
- 테스트 중 노출되는 실패 케이스들은 의도적인 케이스들 입니다.

### 1. 🖥️ **로컬 자동화 실행**  
[영상 보기 (YouTube)](https://www.youtube.com/watch?v=LYsvUJvG5CI&ab_channel=%EC%9E%84%EC%9E%AC%EB%AF%BC)
 

### 2. ☁️ **CI/CD 자동 실행 (GitHub Actions)**  
[영상 보기 (YouTube)](https://www.youtube.com/watch?v=wx1F2yGFV2s&ab_channel=%EC%9E%84%EC%9E%AC%EB%AF%BC)

## 📋 테스트 케이스 문서
[UI + API 테스트케이스 엑셀 보기](./docs/테스트설계_포트폴리오용.xlsx)

