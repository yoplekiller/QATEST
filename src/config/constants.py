"""
프로젝트 핵심 상수 정의
매직 넘버를 제거하고 중앙에서 관리하기 위한 설정 파일
"""

# ========================================
# 타임아웃 설정 (초 단위)
# ========================================
DEFAULT_TIMEOUT = 5
"""기본 대기 시간 - 대부분의 요소 탐색에 사용"""

SHORT_TIMEOUT = 3
"""짧은 대기 시간 - 빠른 요소나 팝업에 사용"""

LONG_TIMEOUT = 10
"""긴 대기 시간 - 느린 페이지 로드나 복잡한 요소에 사용"""


# ========================================
# Sleep 시간 (초 단위)
# ========================================
SHORT_SLEEP = 0.5
"""짧은 대기 - 애니메이션이나 간단한 상태 변경 대기"""

MEDIUM_SLEEP = 1
"""중간 대기 - 일반적인 페이지 전환이나 동적 콘텐츠 로드"""


# ========================================
# URL 설정
# ========================================
KURLY_BASE_URL = "https://www.kurly.com"
"""마켓컬리 메인 URL"""


# ========================================
# 경로 설정
# ========================================
SCREENSHOT_DIR = "screenshots"
"""스크린샷 저장 디렉토리"""

LOG_DIR = "logs"
"""로그 파일 저장 디렉토리"""

# Page URLs
PAGE_URLS = {
    "MAIN": "https://www.kurly.com",
    "CART": "https://www.kurly.com/cart",
    "LOGIN": "https://www.kurly.com"  # LOGIN과 MAIN이 동일
}

# 영향받는 파일:
#  - kurly_login_page.py:20 - KURLY_MAIN_URL 제거, constants 사용
#  - kurly_main_page.py:24 - KURLY_MAIN_URL 제거, constants 사용
#  - kurly_cart_page.py:22 - CART_URL 제거, constants 사용
