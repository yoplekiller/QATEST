from typing import Optional
import requests
from utils.config_utils import get_current_env
from utils.api_utils import send_get_request



class TMDBApiClient:
     """
      TMDB API 클라이언트 클래스

      POM 패턴의 API 버전으로, 모든 API 엔드포인트를 메서드로 관리합니다.
      """
     
     def __init__(self):
          """초기화 메서드: 환경 설정 로드 및 기본 URL 설정"""
          env = get_current_env()
          self.api_key = env["api_key"]
          self.base_url = "https://api.themoviedb.org/3"

    #=========================== 영화 목록 API ===========================#

     def get_popular_movies(self, page: int =1) -> requests.Response:
         """인기 영화 목록 조회"""
         endpoint = "/movie/popular"
         params = {"api_key": self.api_key, "page": page}
         return send_get_request(endpoint, params)
     
     
     def get_top_rated_movies(self, page: int =1) -> requests.Response:
         """최고 평점 영화 목록 조회"""
         endpoint = "/movie/top_rated"
         params = {"api_key": self.api_key, "page": page}
         return send_get_request(endpoint, params)
     
     
     def get_movie_details(self, movie_id: int) -> requests.Response:
         """특정 영화 상세 정보 조회"""
         endpoint = f"/movie/{movie_id}"
         params = {"api_key": self.api_key}
         return send_get_request(endpoint, params)
     
     # ========================== 검색 API ===========================#

     def search_movie(  self, query: str, page: int =1) -> requests.Response:
         """영화 검색"""
         endpoint = "/search/movie"
         params = {"api_key": self.api_key, "query": query, "page": page}
         return send_get_request(endpoint, params)
     
     # ========================== 장르 API ===========================#
     def get_genres(self) -> requests.Response:
         """영화 장르 목록 조회"""
         endpoint = "/genre/movie/list"
         params = {"api_key": self.api_key}
         return send_get_request(endpoint, params)
     
     # ========================== Negative Test Cases ===========================#
     def get_movie_details_invalid_id(self, movie_id: str) -> requests.Response:
         """잘못된 영화 ID로 영화 상세 정보 조회 (Negative Test Case)"""
         endpoint = f"/movie/{movie_id}"
         params = {"api_key": self.api_key}
         return send_get_request(endpoint, params)
     
     def get_popular_movies_invalid_page(self, page: str) -> requests.Response:
         """잘못된 페이지 번호로 인기 영화 목록 조회 (Negative Test Case)"""
         endpoint = "/movie/popular"
         params = {"api_key": self.api_key, "page": page}
         return send_get_request(endpoint, params)
     
     # ========================== Additional Endpoints ===========================#
     def get_movie_videos(self, movie_id: int) -> requests.Response:
         """특정 영화의 비디오(예: 예고편) 조회"""
         endpoint = f"/movie/{movie_id}/videos"
         params = {"api_key": self.api_key}
         return send_get_request(endpoint, params)