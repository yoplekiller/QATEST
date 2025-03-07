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

    sheet.append([test_name, status, error_msg])

    for col in status.columns:
        max_length = 0
        col_letter = col[0].column_letter

        for cell in col:
            try:
                max_length = max(max_length, len(str(cell.value)))
            except:
                pass

        adjusted_width = (max_length + 2)
        sheet.column_dimensions[col_letter].width = adjusted_width


    wb.save(FILE_PATH)  # 변경 내용 저장
    print(f"엑셀 저장 완료: {FILE_PATH}")
