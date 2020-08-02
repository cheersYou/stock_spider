import xlwt
import xlrd
from xlutils.copy import copy
sheet = None
'''
docx模块：可读取、写入.docx文档（不支持.doc文档！！！）

xlrd模块：可读取.xls、.xlsx表格

xlwt模块：可写入.xls表格（不可写入.xlsx文件！！！）

pptx模块：可读取.pptx，可写入.ppt、.pptx（.ppt演示文稿，只能读取pptx模块自身输出的，对其他方式生成的不支持！！！）
'''


def initExcel(sheet_name):
    global sheet
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet(sheet_name)
    return workbook


def writeExcelCell(i, j, value):
    sheet.write(i, j, value)


def write_excel(path, sheet_name, value):
    index = len(value)  # 需要写入的行数
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet(sheet_name)
    for i in range(0, index):
        for j in range(0, len(value[i])):
            sheet.write(i, j, value[i][j])  # 像表格中写入数据（对应的行和列）
    workbook.save(path)  # 保存工作簿
    print("xls格式表格写入数据成功！")


def write_excel_xls_append(path, value):
    index = len(value)  # 获取需要写入数据的行数
    workbook = xlrd.open_workbook(path)  # 打开工作簿
    sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
    worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
    rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数
    new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
    new_worksheet = new_workbook.get_sheet(0)  # 获取转化后工作簿中的第一个表格
    for i in range(0, index):
        for j in range(0, len(value[i])):
            new_worksheet.write(i + rows_old, j,
                                value[i][j])  # 追加写入数据，注意是从i+rows_old行开始写入
    new_workbook.save(path)  # 保存工作簿
    print("xls格式表格【追加】写入数据成功！")


def read_excel_xls(path):
    workbook = xlrd.open_workbook(path)  # 打开工作簿
    sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
    worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
    for i in range(0, worksheet.nrows):
        for j in range(0, worksheet.ncols):
            print(worksheet.cell_value(i, j), "\t", end="")  # 逐行逐列读取数据
        print()