# 🛠 Selenium & API Test Automation  
GitHub Actions 기반의 자동화 테스트 프로젝트  

## 📌 프로젝트 개요  
이 프로젝트는 **Selenium을 활용한 UI 자동화 테스트 및 GitHub Actions 기반의 CI/CD 파이프라인 구축**을 목표로 진행 중인 프로젝트 입니다.  
현재 **API 테스트 및 Allure Report 개선 작업, 테스트 결과를 Excel에 자동 업데이트 하는 작업을 진행 중**이며, 지속적으로 업데이트될 예정입니다.  

## 🚀 기술 스택  
- **언어:** Python  
- **테스트 프레임워크:** pytest  
- **UI 자동화:** Selenium WebDriver  
- **CI/CD:** GitHub Actions  
- **테스트 리포트:** Allure Report
- **API 테스트:** pytest & requests (현재 개발 진행 중)  
- **결과 자동 업데이트:** Excel
- **환경 구성:** Docker & Local

## 🏗 주요 기능  
### **UI 자동화 테스트 (Selenium)**  
- Selenium을 활용하여 웹 애플리케이션의 주요 기능을 자동화  
- GitHub Actions에서 자동 실행하여 테스트 안정성 확보  
- 실패 Case 만들어 실패 시 스크린샷 저장 및 Allure Report 생성 (현재 일부 개선 작업 진행 중)
- 엑셀의 상품 목록과 테스트 연동시켜 코드 간소화

### **CI/CD 파이프라인 (GitHub Actions)**  
- `push` 및 `pull request` 발생 시 자동으로 테스트 실행  
- 일정 주기로 (`cron`) 테스트 실행하여 반복 테스트 진행  
- 테스트 결과를 GitHub Pages와 Slack을 통해 Report 배포

### **API 테스트**  
- pytest & request 기반 API 테스트 실행
- TMDB 사이트 API_KEY를 활용하여 API 테스트 진행
- API 테스트 케이스 추가 예정

### **Allure Report**  
- 테스트 결과를 시각화하여 GitHub Pages에 자동 배포  
- UI & API 테스트 리포트를 통합하여 확인 가능하도록 개선 예정(현재 UI 테스트 리포트만 업로드 중)

### **결과 자동 업데이트(현재 개발 중)**
- 테스트 결과를 Excel에 자동으로 업데이트 하는 기능(현재 개발 중)





## 🛠 실행 방법  
### **로컬에서 실행**  
```bash
# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # (Windows 사용자는 venv\Scripts\activate)

# 의존성 설치
venv/bin/python -m pip install -r requirements.txt allure-pytest

# Selenium UI 테스트 실행
pytest src/tests/ui_tests --alluredir=allure-results

# API 테스트 실행 (추가 예정)
pytest src/tests/api_tests --alluredir=allure-results/api

# Allure Report 생성 및 실행
allure generate allure-results -o allure-report --clean
allure open allure-report
```
### **Docker환경에서 실행**
````
# Docker 컨테이너 빌드 및 실행
docker-compose up --build -d

#실행 중인 컨테이너 내부에서 테스트 실행
docker exec -it selenium-container pytest src/tests/ui_tests --alluredir=/allure-results/docker

# 테스트 결과 확인 후 Docker 종료
docker-compose down