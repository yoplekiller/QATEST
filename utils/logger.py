"""
로깅 유틸리티
실무에서 필수적인 로깅 기능 제공
"""
import logging
import os
from datetime import datetime


class TestLogger:
    """
    테스트 실행 로그를 기록하는 클래스
    실무에서는 로그 분석을 통해 디버깅 및 모니터링을 수행합니다.
    """

    @staticmethod
    def setup_logger(name="test_automation", level=logging.INFO):
        """
        로거 설정 및 반환

        Args:
            name: 로거 이름
            level: 로그 레벨 (DEBUG, INFO, WARNING, ERROR, CRITICAL)

        Returns:
            logging.Logger: 설정된 로거 인스턴스
        """
        # 로그 디렉토리 생성
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)

        # 로그 파일명 (날짜 기반)
        log_file = os.path.join(
            log_dir,
            f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        )

        # 로거 생성
        logger = logging.getLogger(name)
        logger.setLevel(level)

        # 이미 핸들러가 있으면 제거 (중복 방지)
        if logger.handlers:
            logger.handlers.clear()

        # 파일 핸들러 (파일에 저장)
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level)

        # 콘솔 핸들러 (터미널에 출력)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)

        # 포맷 설정
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # 핸들러 추가
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger


# 전역 로거 인스턴스 생성 (싱글톤 패턴)
logger = TestLogger.setup_logger()
