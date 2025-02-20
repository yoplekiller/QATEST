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

### **GitHub Actions - CI/CD 자동화**
이 프로젝트는 Github Actions을 활용하여 자동화 테스트를 수행하였습니다.
````
사용되는 YAML 파일
|----------------------------|--------------------------------------------|
| `.github/workflows/api-test.yaml` | API 서버를 실행하고 API 테스트 수행 |
| `.github/workflows/repeat-test.yaml` | 5회 반복 UI 테스트 수행 |
| `.github/workflows/selenium-test.yaml` | Selenium UI 테스트 자동 실행 |
| `.github/workflows/github-pages.yaml` | 테스트 리포트를 GitHub Pages에 업로드 |
````

### **Python 코드 구조**
프로젝트에서 사용되는 주요 Python 코드와 역할을 정리하였습니다.
````
테스트 관련 파일
|----------------------------|--------------------------------------------|
| `test_cart.py` | 장바구니 동작 테스트 |
| `test_category_filter.py` | 가격 필터링 테스트 |
| `test_header.py` | 홈페이지 헤더 버튼 동작 테스트 |
| `test_search.py` | 상품 검색 기능 테스트 |
| `test_sorting.py` | 정렬 옵션 테스트 |
````
````
테스트 실행 환경 및 유틸리티 파일
|----------------------------|--------------------------------------------|
| `api_server.py` | API 테스트용 서버 실행 |
| `browser_action.py` | 브라우저 상호작용 관련 주요 함수 |
| `config.py` | 기본 URL 및 설정 파일 |
| `utilities.py` | 스크린샷 저장 및 기타 유틸리티 기능 |
| `conftest.py` | 브라우저 초기화 및 공통 설정 |
````
                        


### **설치 및 설정**
#### **사전 준비**

- Python 3.13
- Google Chrome Browser
- ChromeDriver
- PyCharm

#### **설정 방법**

1. 레포지토리 클론:<br>
   ````
   git clone https://github.com/yoplekiller/QATEST.git
   cd ProjectTest

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
(selenium-tests.yaml)를 포함합니다. Workflow는 dependency을 설치하고 ChromeDriver를 설정한 후 테스트를
실행합니다.

1. **테스트 리포트 업로드:**
- Artifact 코드를 추가하여 HTML 테스트 리포트가 GitHub Actions의 Artifacts 섹션으로 업로드되어 확인할 수 있습니다.
 
2. **테스트 자동 실행:**
- CI/CD 파이프라인에서 테스트를 12시간 간격으로 자동 실행하도록 설정하였습니다.
````
schedule:
 - cron: '0 */12 * * *'
````
3. **반복 테스트 실행:**
- repeat-test.yaml 파일을 이용하여 반복 테스트 실행을 관리합니다.
- 반복 테스트 회수를 5번 실행하도록 설정하였습니다.
````
- name: Run repeated tests
      run: |
        source venv/bin/activate
        for i in {1..5}; do
          echo "Running test iteration $i..."
          pytest --html=report_$i.html --self-contained-html
          echo "Waiting for 10 seconds before next test..."
          sleep 10
        done
````


### **실행 결과 예시**
테스트 결과 스크린샷은 디버깅 및 겸증을 위해 screenshots 디렉토리에 저장됩니다. 테스트를 실행한 후
생성된 HTML 리포트를 확인할 수 있습니다.

### **테스트 리포트 확인**
- Github Pages에서 최근 테스트 리포트 확인 가능:
  [Selenium UI Test Report](https://yoplekiller.github.io/QATEST/ui_report.html)
- Slack 채널에서도 자동으로 테스트 완료 메시지를 확인할 수 있습니다.

### ** 테스트 결과 알림 (Slack Webhook)**
이 프로젝트는 Github Actions에서 실행된 테스트 결과를 **Slack 채널**로 자동 전송합니다.
Slack Webhook을 활용하여, 테스트가 실패했을 때 즉시 확인하고 대응할 수 있습니다.

**Slack 알림 예제**
✅ Selenium Test 완료 📢 Selenium UI 테스트가 끝났습니다!
📄 리포트 확인: https://yoplekiller.github.io/QATEST/reports/ui_report.html




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

### **🐳 Docker 환경 지원 (추가 예정)**
현재는 로콜에서 Python 가상 환경(venv)을 사용하여 테스트를 싱행하지만,
향후 **Docker 컨테이너**를 이용해 실행 환경을 통일할 계획입니다.

**예정된 개선 사항**
- 'Dokcerfile' 추가하여 컨테이너에서 테스트 실행
- 'docker-compose.yaml'로 **Selenium WebDriver & API 서버 자동 실행**
- Github Actions에서도 Docker 컨테이너를 활용해 더 일관된 테스트 환경 제공

**Docker 지원이 완료되면, `README.md`를 업데이트하겠습니다!**


### **라이선스**
이 프로젝트는 Apache 2.0 라이선스를 따릅니다. 자세한 내용은 LICENSE 파일을 참조하세요.
