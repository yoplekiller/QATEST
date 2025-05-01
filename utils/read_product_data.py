import openpyxl
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(BASE_DIR, "src/tests/testcases", "test_case.xlsx")


#상품 목록
def read_search_terms_from_excel(file_path):
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook["상품목록"]
    search_terms = []

    for row in sheet.iter_rows(min_row=2, values_only=True):
        tc_id, search_term = row
        search_terms.append((tc_id, search_term))

    return search_terms


