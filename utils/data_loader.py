import csv
import os


#영화 id와 제목
def load_movie_test_data(filename="movie_list.csv"):
    base_dir = os.path.dirname(__file__)  # utils/
    file_path = os.path.join(base_dir, "..", "testdata", filename)

    with open(file_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [(int(row["movie_id"]), row["expected_title"]) for row in reader]


#영화 id와 장르
def load_genre_test_data(filename = "genre_expectations.csv"):
    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, "..", "testdata", filename)

    with open(file_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [
            (int(row["movie_id"]), row["expected_genres"].split("|"))
            for row in reader
            ]


