# QA 자동화 포트폴리오 프로젝트

## 💡 프로젝트 요약
반복적인 수동 테스트를 자동화하기 위해 Python 기반으로 구현한 QA 테스트 자동화 포트폴리오입니다.
실제 웹 서비스인 마켓컬리를 대상으로 웹/앱 테스트 스크립트를 구성하였고,
별도로 **영화 정보 API(TMDB)**를 활용한 API 테스트도 포함되어 있습니다.
테스트 결과는 Allure Report로 시각화되며, Slack으로 자동 보고됩니다.

## 🧰 Tech Stack
- Python / Selenium / Pytest
- Appium (Android)
- Allure Report
- Slack Bot 알림 자동화
- GitHub Actions (CI/CD)

## ▶ 실행 방법
### 1️⃣ 필수 패키지 설치
```bash
pip install -r requirements.txt
```
### 2️⃣ 테스트 실행 (Allure 결과 생성)
```
pytest --alluredir=./reports
```
### 3️⃣ Allure Report 확인
```
allure serve ./reports
```

## 📊 테스트결과 — Allure Report
📄 [Allure Report 보기](https://yoplekiller.github.io/QATEST/allure-report/main/index.html)

## 🔄 CI/CD 워크플로 (GitHub Actions)
Push
 ⬇
Pytest 실행
 ⬇
Allure Report 생성
 ⬇
Slack 자동 알림


## 🧪 테스트 시나리오 요약

🛒 마켓컬리 (UI)
항목	검증 내용
로그인	정상 로그인 / 오류 메시지 확인
상품 검색	검색 결과 정확성 및 이동
카테고리 검색	리스트 정상 노출
장바구니	담기 → 추가 확인 → 페이지 이동
검색 예외 처리	공백/결과 없는 검색 처리 확인

🎬 영화 API
항목	검증 내용
상세 조회	특정 영화 ID 응답 필드 검증
인기 영화 목록	응답 코드 / 데이터 개수
ID 기반 상세조회	결과 매핑 정확성

-------------------------------------------------------


## 🔮 TODO
- ⬜ OWASP ZAP 도구를 활용한 보안 테스트 통합
- ⬜ API 테스트 케이스 추가 및 에러 시나리오 강화
- ⬜ Docker 환경 최적화 및 다중 서비스 분리 실행
- ⬜ 테스트 실패 시 자동 이슈 생성 기능 연동 (ex. GitHub Issues, Jira)
- ⬜ APPIUM 테스트 기기 및 케이스 추가
- ⬜ SQL을 이용한 DB 자동화 테스트 구현



## 📹 테스트 자동화 시연 영상

### 1. 🖥️ **로컬 자동화 실행**  
[마켓컬리 주문 플로우 자동화 구현 영상 보기 (YouTube)](https://www.youtube.com/watch?v=TqsvT2RsYEs)


