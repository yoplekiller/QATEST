# import openpyxl
#
# def read_login_data(file_path):
#     workbook = openpyxl.load_workbook(file_path)
#     sheet = workbook["로그인계정"]
#     login_data = []
#     for row in sheet.iter_rows(min_row=2, values_only=True):
#         tc_id, id, pw, expected = row
#         login_data.append((tc_id, id, pw, expected))
#
#     return login_data

#필요할 경우 사용