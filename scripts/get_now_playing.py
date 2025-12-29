import csv
import os
import requests
from src.tests.api.test_popular_movie import env, load_config

env = load_config()

BASE_URL = env["base_url"]
API_KEY = env["api_key"]
endpoint = "/movie/now_playing"

params = {
    "api_key": API_KEY,
    "language": "en-US",
    "page": 1
}

response = requests.get(BASE_URL + endpoint, params)
data = response.json()

movies = data["results"][:10]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "..", "testdata", "now_playing.csv")
os.makedirs(os.path.dirname(csv_path), exist_ok=True)

with open(csv_path, mode="w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["movie_id", "expected_title", "expected_release_date"])
    for movie in movies:
        writer.writerow([movie["id"], movie["title"], movie["release_date"]])
