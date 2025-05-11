# QA 자동화 포트폴리오 프로젝트

## 📌 프로젝트 개요
- 반복적인 수동 테스트를 자동화하기 위해 Python 기반으로 구현한 QA테스트 자동화 포트폴리오입니다.
- 실제 웹 서비스(마켓컬리)를 대상으로 Selenium 테스트를 수행하였고,
- 별도의 영화 홈페이지(https://www.themoviedb.org/) API를 활용한 테스트 자동화도 포함하였습니다.
- 테스트 결과는 Allure Report로 시각화되고, Excel파일로 저장되며, Slack으로 자동 보고됩니다.

## 담당 역할
- 테스트 자동화 설계 및 구현
- GitHub Actions 기반 CI 파이프라인 구성
- Excel 자동 리포트 및 테스트 결과 Slack 메시지 전송 기능 구현

## 🧩 프로젝트 구성
### 1. 마켓컬리 웹 테스트(Selenium)
- 상품 검색, 상품 추가, 상품 카테고리 버튼, 장바구니 버튼, 실패 케이스, 로그인 실패케이스 구현
- 주요 테스트 포인트: UI 요소 정상 작동, XPath 접근, 상품 정보 확인

### 2. 영화 API 테스트
- TMDB 또는 유사한 무료 영화 API 기반
- 영화 정보 검색, 장르별 분류, 상세 조회 등 다양한 GET 요청 검증
- 상태 코드, 응답 시간, 필수 데이터 키 확인 등 포함
- SLA 응답 속도 확인

## 🔧 사용 기술
- Python 3
- Selenium (웹 자동화)
- requests (API 테스트)
- openpyxl (Excel 리포트 자동 저장)
- Slack Webhook (알림 자동화)
- Docker / Docker Compose (환경 통합)
- GitHub Actions (CI 연동)
- Allure Report(테스트 결과 시각화)

## 📁 디렉토리 구조
<pre>├── .github/
│   └── workflows/
│       ├── selenium-test.yaml  # Selenium UI 테스트용 CI 설정
│       └── docker-test.yaml  # Docker 기반 테스트 CI 설정
│
├── allure-results/                  # Allure 결과 저장 폴더
│
├── src/
│   ├── report/
│   │   └── generate_excel_report.py  # Excel 리포트 생성 모듈
│   └── tests/
│       ├── testcases/              # 테스트 목록( ex) test_ui_search 상품목록)
│       ├── ui_tests/               # UI 테스트 스크립트
│       ├── api_tests/              # API 테스트 스크립트
│       └── conftest.py             # Pytest 공통 fixture
│
├── utils/                           # 공통 유틸 함수 모음
├── config/                          # 설정 파일 (config.yaml 등)
│
├── report.xml                       # 테스트 결과 요약 파일 (JUnit 형식)
├── README.md                        # 프로젝트 설명 문서
├── requirements.txt                 # 의존성 설치 목록
├── pytest.ini                       # Pytest 설정
├── docker-compose.yml               # Docker 서비스 정의
├── Dockerfile                       # Docker 이미지 빌드 정의
├── docker-clean.sh                  # 도커 환경 초기화 스크립트
├── .nojekyll                        # GitHub Pages 설정용 파일
└── .gitignore                       # Git 추적 제외 파일
</pre>

## ✅ 주요 기능
- 테스트 결과를 Excel로 정리
- 테스트 완료 시 Slack으로 자동 전송
- Docker로 통합 실행 환경 구성

## 🤸 실행 방법
### &nbsp; PyCharm에서 실행하기
1. 이 프로젝트를 PyCharm으로 열기
2. 가상환경(venv)설정 또는 Python 인터프리터 선택
3. 'requirements.txt' 설치
4. 실행할 테스트 선택
- 'pytest src/tests/ui_tests/' 디렉토리 내 테스트 파일 실행
-  API 테스트는 현재 GitHub Actions 환경에서만 실행됩니다. (API 키 보안상 로컬 실행 제한)

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
- [UI + API 테스트케이스 엑셀 보기](./docs/테스트설계_포트폴리오.xlsx)

