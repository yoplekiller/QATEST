# get_now_playing.py 리팩토링 요약

## 수정 일시
2025-12-30

## 수정 파일
`scripts/get_now_playing.py`

## 수정 내용

### 1. 코드 스타일 개선 (PEP 8)
- **Line 12**: `params={` → `params = {`
  - 할당 연산자 양쪽에 공백 추가

- **Line 18**: `response=` → `response = {`
  - 할당 연산자 양쪽에 공백 추가

### 2. 불필요한 주석 제거
- **Line 23**: `# scripts 폴더 기준` 주석 제거
  - 코드가 self-explanatory하므로 불필요한 주석 삭제

### 3. 버그 수정
- **Line 27**: `open("testdata/now_playing.csv", ...)` → `open(csv_path, ...)`
  - 정의된 `csv_path` 변수를 사용하지 않고 하드코딩된 경로를 사용하던 문제 수정
  - 이제 `BASE_DIR` 기반의 상대 경로를 올바르게 사용

## 수정 전/후 비교

### 수정 전
```python
params={
    "api_key": API_KEY,
    "language": "en-US",
    "page": 1
}

response= requests.get(BASE_URL + endpoint, params)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # scripts 폴더 기준
csv_path = os.path.join(BASE_DIR, "..", "testdata", "now_playing.csv")
os.makedirs(os.path.dirname(csv_path), exist_ok=True)

with open("testdata/now_playing.csv", mode="w", encoding="utf-8", newline="") as f:
```

### 수정 후
```python
params = {
    "api_key": API_KEY,
    "language": "en-US",
    "page": 1
}

response = requests.get(BASE_URL + endpoint, params)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "..", "testdata", "now_playing.csv")
os.makedirs(os.path.dirname(csv_path), exist_ok=True)

with open(csv_path, mode="w", encoding="utf-8", newline="") as f:
```

## 개선 효과
- PEP 8 코딩 스타일 준수로 가독성 향상
- 불필요한 주석 제거로 코드 간결성 향상
- 정의된 변수를 올바르게 사용하여 유지보수성 향상
