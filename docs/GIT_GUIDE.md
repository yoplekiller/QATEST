# Git 사용 가이드

Git과 GitHub의 핵심 기능인 **Pull Request**와 **Issue**를 활용하여 효율적으로 협업하는 방법을 안내합니다.

---

## 목차
1. [Pull Request (PR)란?](#pull-request-pr란)
2. [Pull Request 사용 방법](#pull-request-사용-방법)
3. [Issue란?](#issue란)
4. [Issue 사용 방법](#issue-사용-방법)
5. [Issue와 PR 연결하기](#issue와-pr-연결하기)
6. [실전 워크플로우](#실전-워크플로우)
7. [자주 사용하는 Git 명령어](#자주-사용하는-git-명령어)

---

## Pull Request (PR)란?

**Pull Request**는 내가 작성한 코드 변경사항을 다른 브랜치(보통 `main`)에 병합(merge)하기 전에 **팀원들에게 검토를 요청**하는 기능입니다.

### PR의 장점
- **코드 리뷰**: 실수나 버그를 사전에 발견
- **지식 공유**: 팀원들이 코드 변경사항 파악
- **품질 관리**: CI/CD 자동 테스트 실행
- **히스토리 관리**: 왜 이 변경이 있었는지 문서화

### PR 프로세스

```
1. feature 브랜치에서 코드 작성
   ↓
2. 코드를 커밋하고 푸시
   ↓
3. Pull Request 생성 (GitHub 웹에서)
   ↓
4. 팀원들이 코드 리뷰 & 피드백
   ↓
5. 필요시 수정 후 다시 푸시
   ↓
6. 승인 후 main 브랜치에 병합(Merge)
```

---

## Pull Request 사용 방법

### 1. 새 브랜치 생성 및 작업

```bash
# main 브랜치에서 최신 상태로 업데이트
git checkout main
git pull origin main

# 새 기능 브랜치 생성
git checkout -b feature/add-login-api

# 코드 작성 후 커밋
git add .
git commit -m "feat: 로그인 API 추가"

# GitHub에 푸시
git push -u origin feature/add-login-api
```

### 2. GitHub에서 PR 생성

**웹 브라우저 방법:**
1. GitHub 저장소 페이지 접속
2. "Pull requests" 탭 클릭
3. "New pull request" 버튼 클릭
4. base: `main` ← compare: `feature/add-login-api` 선택
5. 제목과 설명 작성
6. "Create pull request" 클릭

**gh CLI 방법:**
```bash
# PR 생성 (제목과 본문 입력)
gh pr create --title "feat: 로그인 API 추가" --body "로그인 엔드포인트 구현 및 테스트 추가"

# 인터랙티브 모드로 생성
gh pr create
```

### 3. PR 템플릿 예시

```markdown
## 변경 사항
- 로그인 API 엔드포인트 추가 (`POST /api/login`)
- JWT 토큰 발급 로직 구현
- 로그인 API 테스트 코드 작성

## 테스트 방법
- [ ] 유효한 계정으로 로그인 성공
- [ ] 잘못된 비밀번호로 로그인 실패
- [ ] 존재하지 않는 계정으로 로그인 실패

## 관련 Issue
Closes #45
```

### 4. 코드 리뷰 받기

팀원들이 PR에 코멘트를 달면:
- 피드백 반영하여 코드 수정
- 같은 브랜치에 커밋 & 푸시 (PR 자동 업데이트)

```bash
# 피드백 반영
git add .
git commit -m "refactor: 코드 리뷰 반영 - 에러 핸들링 개선"
git push
```

### 5. PR 병합

승인 후:
1. GitHub에서 "Merge pull request" 클릭
2. Merge 방법 선택:
   - **Merge commit**: 모든 커밋 이력 보존
   - **Squash and merge**: 여러 커밋을 하나로 합침 (권장)
   - **Rebase and merge**: 선형 이력 유지
3. "Confirm merge" 클릭
4. 브랜치 삭제 (선택사항)

```bash
# 로컬에서 브랜치 삭제
git checkout main
git pull origin main
git branch -d feature/add-login-api
```

---

## Issue란?

**Issue**는 버그 리포트, 기능 요청, 할 일 관리를 위한 **티켓 시스템**입니다.

### Issue 유형

| 유형 | 용도 | 예시 |
|------|------|------|
| `bug` | 버그 리포트 | 로그인 시 500 에러 발생 |
| `enhancement` | 기능 개선 | 검색 속도 최적화 |
| `feature` | 새로운 기능 요청 | 다크모드 추가 |
| `documentation` | 문서 개선 | API 문서 업데이트 |
| `question` | 질문 | 배포 프로세스 문의 |

---

## Issue 사용 방법

### 1. Issue 생성

**GitHub 웹에서:**
1. Repository → "Issues" 탭
2. "New issue" 클릭
3. 제목과 내용 작성
4. Label 추가 (`bug`, `enhancement` 등)
5. Assignee 지정 (담당자)
6. "Submit new issue" 클릭

**gh CLI로:**
```bash
# Issue 생성
gh issue create --title "버그: 로그인 에러" --body "재현 방법: ..."

# 인터랙티브 모드
gh issue create

# Label과 Assignee 지정
gh issue create --title "다크모드 추가" --label "enhancement" --assignee username
```

### 2. Issue 템플릿 예시

#### 버그 리포트

```markdown
## 버그 설명
로그인 시 잘못된 비밀번호를 입력하면 500 에러가 발생합니다.

## 재현 방법
1. 로그인 페이지 접속
2. 올바른 이메일 입력
3. 잘못된 비밀번호 입력
4. "로그인" 버튼 클릭

## 예상 동작
"비밀번호가 틀렸습니다" 메시지 표시

## 실제 동작
500 Internal Server Error 페이지 표시

## 환경
- OS: Windows 11
- Browser: Chrome 120
- 버전: v1.2.3

## 스크린샷
![에러 화면](screenshot.png)
```

#### 기능 요청

```markdown
## 기능 설명
사용자가 다크모드/라이트모드를 선택할 수 있는 테마 전환 기능

## 사용 사례
- 야간에 눈의 피로를 줄이기 위해 다크모드 사용
- 개인 취향에 따라 테마 선택

## 제안 UI
- 헤더에 테마 토글 버튼 추가
- 설정 페이지에서 테마 선택 옵션 제공

## 참고 자료
- [다른 서비스 예시](https://example.com)
```

#### 작업 체크리스트

```markdown
## API 테스트 작성

- [ ] 영화 검색 API 테스트
  - [ ] 정상 케이스
  - [ ] 빈 검색어 처리
  - [ ] 특수문자 검색
- [ ] 인기 영화 API 테스트
  - [ ] 페이지네이션 테스트
  - [ ] 정렬 순서 검증
- [ ] 에러 처리 테스트
  - [ ] 401 Unauthorized
  - [ ] 404 Not Found
  - [ ] 500 Server Error
```

### 3. Issue 관리

```bash
# Issue 목록 보기
gh issue list

# 특정 상태의 Issue 보기
gh issue list --state open
gh issue list --state closed

# 내게 할당된 Issue 보기
gh issue list --assignee @me

# Label로 필터링
gh issue list --label bug

# Issue 닫기
gh issue close 123

# Issue 다시 열기
gh issue reopen 123

# Issue 상세 보기
gh issue view 123
```

---

## Issue와 PR 연결하기

PR에서 Issue를 자동으로 닫으려면 커밋 메시지나 PR 설명에 **키워드**를 사용합니다.

### 자동 닫기 키워드

| 키워드 | 의미 |
|--------|------|
| `Closes #123` | PR 병합 시 Issue #123 닫기 |
| `Fixes #123` | 버그 수정으로 Issue #123 닫기 |
| `Resolves #123` | Issue #123 해결 |

### 예시

**커밋 메시지에서:**
```bash
git commit -m "fix: 로그인 에러 수정

잘못된 비밀번호 입력 시 500 에러 대신
적절한 에러 메시지를 반환하도록 수정

Fixes #45"
```

**PR 설명에서:**
```markdown
## 변경 사항
- 로그인 에러 핸들링 개선
- 비밀번호 검증 로직 수정

## 관련 Issue
Closes #45
Closes #48
```

---

## 실전 워크플로우

### 시나리오: 새 기능 개발

```bash
# 1. Issue 생성
gh issue create --title "다크모드 기능 추가" --label "enhancement"
# → Issue #67 생성됨

# 2. 브랜치 생성 (Issue 번호 포함 권장)
git checkout -b feature/67-dark-mode

# 3. 코드 작성 및 커밋
git add .
git commit -m "feat: 다크모드 UI 구현

- 테마 토글 버튼 추가
- CSS 변수를 이용한 테마 전환
- 로컬 스토리지에 설정 저장

Related to #67"

# 4. 푸시
git push -u origin feature/67-dark-mode

# 5. PR 생성
gh pr create --title "feat: 다크모드 기능 구현" --body "
## 변경 사항
- 테마 토글 버튼 UI 추가
- 다크모드/라이트모드 CSS 구현
- 사용자 선택 저장 기능

## 스크린샷
![다크모드](dark-mode-screenshot.png)

## 테스트 방법
- [ ] 토글 버튼으로 테마 전환 확인
- [ ] 페이지 새로고침 시 설정 유지 확인
- [ ] 다크모드에서 모든 UI 가독성 확인

Closes #67
"

# 6. 코드 리뷰 받고 수정
git add .
git commit -m "refactor: 리뷰 반영 - 접근성 개선"
git push

# 7. PR 병합 (GitHub에서)
# → Issue #67 자동 닫힘

# 8. 로컬 정리
git checkout main
git pull origin main
git branch -d feature/67-dark-mode
```

---

## 자주 사용하는 Git 명령어

### 브랜치 관리

```bash
# 브랜치 목록 보기
git branch                    # 로컬 브랜치
git branch -r                 # 원격 브랜치
git branch -a                 # 모든 브랜치

# 브랜치 생성
git branch feature/new-feature
git checkout -b feature/new-feature  # 생성 + 이동

# 브랜치 이동
git checkout main
git switch main               # 최신 방법

# 브랜치 삭제
git branch -d feature/old-feature    # 병합된 브랜치만
git branch -D feature/old-feature    # 강제 삭제

# 원격 브랜치 삭제
git push origin --delete feature/old-feature
```

### 커밋 관리

```bash
# 변경사항 확인
git status                    # 상태 확인
git diff                      # 변경 내용 비교
git diff --staged             # 스테이징된 변경사항

# 커밋
git add .                     # 모든 변경사항 스테이징
git add file.py               # 특정 파일만
git commit -m "메시지"        # 커밋
git commit --amend            # 마지막 커밋 수정 (주의!)

# 커밋 히스토리
git log                       # 전체 로그
git log --oneline             # 한 줄로 보기
git log --graph               # 그래프로 보기
git log -5                    # 최근 5개만
```

### 동기화

```bash
# 원격 저장소에서 가져오기
git fetch origin              # 변경사항만 가져오기
git pull origin main          # 가져오기 + 병합

# 원격 저장소에 푸시
git push origin main          # 푸시
git push -u origin feature/new  # 최초 푸시 (upstream 설정)
git push --force              # 강제 푸시 (주의!)

# 원격 저장소 관리
git remote -v                 # 원격 저장소 확인
git remote add origin URL     # 원격 저장소 추가
```

### 변경사항 되돌리기

```bash
# 작업 디렉토리 변경사항 취소
git checkout -- file.py       # 특정 파일
git restore file.py           # 최신 방법

# 스테이징 취소
git reset HEAD file.py        # 특정 파일
git restore --staged file.py  # 최신 방법

# 커밋 되돌리기
git revert <commit-hash>      # 새 커밋으로 되돌림 (안전)
git reset --soft HEAD~1       # 커밋만 취소, 변경사항 유지
git reset --hard HEAD~1       # 커밋 + 변경사항 모두 취소 (주의!)

# 특정 커밋으로 파일 복원
git checkout <commit-hash> -- file.py
```

### 병합 및 리베이스

```bash
# 브랜치 병합
git checkout main
git merge feature/new-feature

# 충돌 해결 후
git add .
git commit

# 리베이스 (커밋 이력 정리)
git checkout feature/new-feature
git rebase main

# 충돌 해결 후
git add .
git rebase --continue
git rebase --abort            # 리베이스 취소
```

### 스태시 (임시 저장)

```bash
# 변경사항 임시 저장
git stash                     # 저장
git stash save "메시지"       # 메시지와 함께 저장

# 스태시 목록
git stash list

# 스태시 적용
git stash apply               # 최신 스태시 적용 (유지)
git stash pop                 # 최신 스태시 적용 (제거)
git stash apply stash@{1}     # 특정 스태시 적용

# 스태시 삭제
git stash drop stash@{0}      # 특정 스태시 삭제
git stash clear               # 모든 스태시 삭제
```

---

## 커밋 메시지 컨벤션

일관된 커밋 메시지 작성을 위한 **Conventional Commits** 규칙:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type 종류

| Type | 의미 | 예시 |
|------|------|------|
| `feat` | 새로운 기능 추가 | `feat: 로그인 API 추가` |
| `fix` | 버그 수정 | `fix: 로그인 에러 수정` |
| `docs` | 문서 수정 | `docs: README 업데이트` |
| `style` | 코드 포맷팅 | `style: 코드 정렬` |
| `refactor` | 코드 리팩토링 | `refactor: 함수 분리` |
| `test` | 테스트 코드 | `test: 로그인 테스트 추가` |
| `chore` | 빌드, 설정 변경 | `chore: 의존성 업데이트` |
| `perf` | 성능 개선 | `perf: 쿼리 최적화` |

### 예시

```bash
# 기본 형식
git commit -m "feat: 사용자 검색 기능 추가"

# Scope 포함
git commit -m "fix(auth): 토큰 만료 처리 개선"

# 본문 포함
git commit -m "feat: 다크모드 구현

- 테마 전환 버튼 추가
- CSS 변수 기반 테마 시스템
- 로컬 스토리지 저장

Closes #67"
```

---

## GitHub CLI (gh) 설치 및 사용

### 설치

**Windows:**
```bash
winget install GitHub.cli
```

**macOS:**
```bash
brew install gh
```

**Linux:**
```bash
sudo apt install gh
```

### 인증

```bash
gh auth login
```

### 주요 명령어

```bash
# PR 관리
gh pr list                    # PR 목록
gh pr create                  # PR 생성
gh pr view 123                # PR 상세 보기
gh pr checkout 123            # PR 브랜치로 체크아웃
gh pr merge 123               # PR 병합
gh pr close 123               # PR 닫기

# Issue 관리
gh issue list                 # Issue 목록
gh issue create               # Issue 생성
gh issue view 123             # Issue 상세 보기
gh issue close 123            # Issue 닫기

# Repository 관리
gh repo view                  # 저장소 정보
gh repo clone owner/repo      # 저장소 복제
gh browse                     # 웹 브라우저에서 열기
```

---

## 유용한 팁

### 1. Git Alias 설정

자주 사용하는 명령어를 짧게:

```bash
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.cm commit
git config --global alias.last 'log -1 HEAD'

# 사용
git st                        # git status
git co main                   # git checkout main
```

### 2. 브랜치 이름 규칙

```
feature/기능명         # 새 기능
fix/버그명            # 버그 수정
hotfix/긴급수정명     # 긴급 수정
refactor/리팩토링명   # 리팩토링
docs/문서명           # 문서
test/테스트명         # 테스트

# 예시
feature/67-dark-mode
fix/45-login-error
hotfix/security-patch
```

### 3. .gitignore 활용

불필요한 파일 추적 방지:

```gitignore
# Python
__pycache__/
*.pyc
.venv/
venv/

# IDE
.vscode/
.idea/
*.swp

# 환경 변수
.env
.env.local

# 테스트 결과
allure-results/
*.xml

# OS
.DS_Store
Thumbs.db
```

### 4. 실수 복구

```bash
# 잘못 푸시한 경우 (공유 전)
git reset --hard HEAD~1
git push --force

# 잘못 병합한 경우
git reset --hard HEAD~1

# 삭제한 브랜치 복구
git reflog                    # 커밋 해시 찾기
git checkout -b 브랜치명 <commit-hash>
```

---

## 참고 자료

- [Git 공식 문서](https://git-scm.com/doc)
- [GitHub Docs](https://docs.github.com)
- [GitHub CLI](https://cli.github.com/manual/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git 브랜치 전략](https://nvie.com/posts/a-successful-git-branching-model/)

---

## 문제 해결

### PR 충돌 해결

```bash
# main 브랜치 최신화
git checkout main
git pull origin main

# feature 브랜치로 이동하여 병합
git checkout feature/my-feature
git merge main

# 충돌 해결 후
git add .
git commit -m "merge: main 브랜치와 충돌 해결"
git push
```

### Fork한 저장소 동기화

```bash
# upstream 추가 (최초 1회)
git remote add upstream https://github.com/original/repo.git

# 동기화
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

---

**문서 업데이트**: 2024-12-30
