import openpyxl
import os

FILE_PATH = "test_results.xlsx"

def save_test_result(test_name, status, error_msg=""):

    if not os.path.exists(FILE_PATH):
        wb = openpyxl.Workbook()
        sheet = wb.active
        sheet.append(["테스트 이름","결과","오류 메시지"])
        wb.save(FILE_PATH)

    wb = openpyxl.load_workbook(FILE_PATH)
    sheet = wb.active

    print(f"🟢 엑셀 저장 중: {test_name} - {status}")  # 디버깅 로그 추가
    sheet.append([test_name, status, error_msg])
    wb.save(FILE_PATH)  # 변경 내용 저장
    print(f"✅ 엑셀 저장 완료: {FILE_PATH}")
