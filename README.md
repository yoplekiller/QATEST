## **프로젝트: Selenium 기반 전자상거래 QA 자동화**

개요

이 프로젝트는 Selenium을 활용한 전자상거래 웹사이트의 자동화 테스트를 시연합니다. 주요 기능으로는 상품 검색, 정렬
, 가격 필터링, 장바구니 동작 테스팅 등이 포함됩니다. 이 프로젝트는 Python과 Selenium을 활용한 자동화 테스트
 기술을 포트폴리오로 보여주는 것을 목표로 하였습니다.


### **주요 기능**
- **상품 검색**: 상품 이름으로 검색 기능을 테스트.
- **정렬 옵션 검증**: "신상품순", "높은 가격순", "낮은 가격순" 등 다양한 정렬 옵션 검증.
- **가격 필터링**: 가격 범위에 따른 상품 필터링 테스트.
- **장바구니 기능 테스트**: 상품 추가 및 상품 담기 후 취소버튼, 장바구니 버튼 기능 테스트.
- **오류 처리 및 스크린샷 저장** 테스트 실행 중 디버깅과 결과 확인을 위한 스크린샷 저장.

### **사용 기술**
- **Python**: 핵심 프로그래밍 언어.
- **Selenium**: 브라우저 자동화를 위한 도구.
- **Pytest**: 테스트 프레임워크
- **ChromeDriver**: Chrome 브라우저를 제어하기 위한 WebDriver.

### **파일 구조**

project_root/<br>
├── .github/workflows/selenium-tests.yml &nbsp;&nbsp;&nbsp;&nbsp;  # GitHub Actions 워크플로우 파일 (CI/CD)<br>
├── browser_action.py &nbsp;&nbsp;&nbsp;&nbsp;# 브라우저 상호작용 관련 주요 함수<br>
├── config.py  &nbsp;&nbsp;&nbsp;&nbsp; # 기본 URL 및 설정 파일<br>
├── utilities.py        &nbsp;&nbsp;&nbsp;&nbsp; # 스크린샷 등 유틸리티 함수<br>
├── test_cart.py       &nbsp;&nbsp;&nbsp;&nbsp; # 장바구니 동작 테스트<br>
├── test_price_filter.py      &nbsp;&nbsp;&nbsp;&nbsp; # 가격 필터링 테스트<br>
├── test_search.py    &nbsp;&nbsp;&nbsp;&nbsp;  # 상품 검색 기능 테스트<br>
├── test_sorting.py       &nbsp;&nbsp;&nbsp;&nbsp; # 정렬 옵션 테스트<br>
├── requirements.txt   &nbsp;&nbsp;&nbsp;&nbsp;  # 프로젝트 의존성 목록<br>

                        


### **설치 및 설정**
#### **사전 준비**

- Python 3.11
- Google Chrome Browser
- ChromeDriver
- PyCharm

#### **설정 방법**

1. 레포지토리 클론:
   git clone https://github.com/yourusername/your-repository.git
   cd your-repository


### **테스트 실행**
#### **로컬 환경에서 실행**
개별 테스트 파일을 pytest로 실행:<br>
pytest test_search.py<br>
pytest test_sorting.py<br>
pytest test_cart.py<br>
pytest test_price_filter.py

#### **GitHub Actions을 활용한 CI/CD**
이 프로젝트는 main 브랜치에 푸시되거나 pr이 생성될 때 테스트를 실행하는 Github Actions 워크플로우
(selenium-tests.yaml)를 포함합니다. 워크플로우는 의존성을 설치하고 ChromeDriver를 설정한 후 테스트를
실행합니다.

### **실행 결과 예시**
테스트 결과 스크린샷은 디버깅 및 겸증을 위해 screenshots 디렉토리에 저장됩니다. 테스트를 실행한 후
생성된 HTML 리포트를 확인할 수 있습니다.

### **향후 개선 사항**
- 엣지 케이스를 위한 추가 테스트 케이스 작성.
- 테스트 관리 도구와 통합.
- pytest-html을 활용한 상세한 테스트 리포트 생성.
- Firefox,Safari 등 추가 브라우저를 포함한 CI/CD 파이프라인 확장.
- 로그인, 회원가입 등의 테스트 케이스 추가.

### **라이선스**

