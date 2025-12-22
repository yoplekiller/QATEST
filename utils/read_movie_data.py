# import openpyxl
# import os
# from src.report.generate_excel_report import sheet
#
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# file_path = os.path.join(BASE_DIR, "src/tests/testcases", "test_case.xlsx")
#
#
# def read_search_movie_from_excel(file_path):
#     workbook_movie = openpyxl.load_workbook(file_path)
#     sheet_movie = workbook_movie["영화목록"]
#     movie_term= []
#
#     for row in sheet.iter_rows(max_row=2, values_only=True):
#         movie_id, expected_title = row
#         sheet_movie.append((movie_id, expected_title))
#     return movie_term