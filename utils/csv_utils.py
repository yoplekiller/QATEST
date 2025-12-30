from datetime import datetime
import csv
import os

"""CSV 파일 관련 유틸리티 함수들"""
def get_timestamped_filename(base_name: str, extension: str = "csv") -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{base_name}_{timestamp}.{extension}"

# 저장할 영화 정보 리스트를 CSV 파일로 저장하는 함수
def save_movies_to_csv(movies, filename, folder="results"):
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)
    with open(filepath, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["id", "title", "vote_average", "release_date"])
        for movie in movies:
            writer.writerow([
                movie.get("id"),
                movie.get("title"),
                movie.get("vote_average"),
                movie.get("release_date")
            ])