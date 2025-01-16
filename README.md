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
````
project_root/<br>
├── .github/workflows/selenium-tests.yml  # GitHub Actions 워크플로우 파일 (CI/CD)
├── browser_action.py # 브라우저 상호작용 관련 주요 함수
├── config.py  # 기본 URL 및 설정 파일
├── utilities.py # 스크린샷 등 유틸리티 함수
├── conftest.py  # 브라우저 초기화 함수 
├── test_cart.py  # 장바구니 동작 테스트
├── test_category_filter.py  # 가격 필터링 테스트
├── test_header.py  # 홈페이지 헤더 버튼 동작 테스트
├── test_search.py  # 상품 검색 기능 테스트
├── test_sorting.py  # 정렬 옵션 테스트
├── requirements.txt # 프로젝트 의존성 목록
````
                        


### **설치 및 설정**
#### **사전 준비**

- Python 3.11
- Google Chrome Browser
- ChromeDriver
- PyCharm

#### **설정 방법**

1. 레포지토리 클론:<br>
   ````
   git clone https://github.com/yourusername/your-repository.git
   cd your-repository

2. 의존성 설치:<br>
   ````
   pip install -r requirements.txt
3. `config.py`파일에서 기본 URL을 업데이트 (기본값:`http://www.kurly.com/main`).
4. ChromeDriver가 설치되어 있고, `browser_action.py`또는 시스템 환경 변수에 경로가 설정되어있는지 확인.

### 테스트 결과 리포트 생성

`pytest-html` 플러그인을 사용해 테스트 결과를 HTML로 시각화할 수 있습니다.

#### 설치 방법
   ```
   pip install pytest-html
   ```
#### 리포트 생성 방법
  ```
  pytest --html=report.html --self-contained-html
  ```
### **테스트 실행**
#### **로컬 환경에서 실행**
개별 테스트 파일을 pytest로 실행:<br>
````
pytest test_search.py
pytest test_sorting.py
pytest test_cart.py
pytest test_category_filter.py
pytest test_header.py
````

### **GitHub Actions을 활용한 CI/CD**
이 프로젝트는 main 브랜치에 푸시되거나 pr이 생성될 때 테스트를 실행하는 Github Actions 워크플로우
(selenium-tests.yaml)를 포함합니다. 워크플로우는 의존성을 설치하고 ChromeDriver를 설정한 후 테스트를
실행합니다.

1. **테스트 리포트 업로드:**
- Artifact 코드를 추가하여 HTML 테스트 리포트가 GitHub Actions의 Artifacts 섹션으로 업로드되어 확인할 수 있습니다.
 
2. **테스트 자동 실행:**
- CI/CD 파이프라인에서 테스트를 6시간 간격으로 자동 실행하도록 설정하였습니다.
````
schedule:
 - cron: '0 */6 * * *'
````
3. **반복 테스트 실행:**
- CI/CD 파이프라인에서
- repeat-test.yaml 파일을 이용하여 반복 테스트 실행


### **실행 결과 예시**
테스트 결과 스크린샷은 디버깅 및 겸증을 위해 screenshots 디렉토리에 저장됩니다. 테스트를 실행한 후
생성된 HTML 리포트를 확인할 수 있습니다.

### **향후 개선 사항**
- 테스트 관리 도구와 통합.
- pytest-html을 활용한 상세한 테스트 리포트 생성.
- firefox, edge 등 추가 브라우저를 포함한 CI/CD 파이프라인 확장.
- 로그인, 회원가입 등의 테스트 케이스 추가.

### **기여 방법**
1. **레포지토리 포크(Fork):** 
 - Github에서 이 프로젝트를 포크하여 자신의 계정으로 복사하세요
2. **클론(Clone):**
- 포크한 레포지토리를 로컬 환경에 클론합니다:
  ````
  git clone https://github.com/yourusername/your-repository.git
  cd your-repository

3. **새로운 브랜치 생성:**
- 기능 추가나 버그 수정을 위한 브랜치를 생성하세요:
  ````
  git check -b new-feature-branch
  
4. **변경 사항 커밋:**
- 작업한 내용을 커밋하고 로컬 브랜치에 저장합니다:
  ````
  git add .
  git commit -m "Add new feature or fix bug"

5. **푸시(Push)**
- 변경 사항을 Github에 푸시합니다:
  ````
  git push origin new-feature-branch

6. **Pull Request 생성:**
- Github에서 원본 레포지토리로 Pull Request(PR)을 생성하여 변경 사항을 제출하세요.

7. **검토 및 병합:**
- 프로젝트 관리자가 PR을 검토하고 병합합니다.


### **라이선스**
이 프로젝트는 Apache 2.0 라이선스를 따릅니다. 자세한 내용은 LICENSE 파일을 참조하세요.
