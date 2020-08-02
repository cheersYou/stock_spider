# A股使用代码
# 港股和美股使用名字
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from utils.wait import waitByClickAndSelector, waitByClickAndID
from utils.find import findById, findByCssSelector
from database.mongo import initMongo, addCollect, addDB, insert, find
from database.csv import initCSV, writeCsvHeader, writeCsvRow
from database.excel import initExcel, writeExcelCell
from threads.Thread import MyThread
import time
import re
browser = webdriver.Chrome("D:\Chrome\chromedriver.exe")
url = 'https://m.cn.investing.com'
origin_date = "2016-01-01"
csv_dir = "./csv/"
excel_dir = "./excel/"
# db_name = "StockUSChina"
path1 = "us_chinese.txt"

# db_name = "StockHK"
path2 = "hongkong_famous.txt"
path3 = "hongkong_red.txt"
path4 = "hongkong_blue.txt"

# db_name = "Stock300"
path5 = "300.txt"

# db_name = "Stock50"
path6 = "50.txt"

# db_name = "SelfStock"
path7 = "self.txt"
csv_headers = ["日期", "收盘", "开盘", "高峰", "低峰", "交易量", "涨跌幅"]

pathlist = [path6]
# "StockUSChina","StockHK", "StockHK", "StockHK", "Stock300", "Stock50", "SelfStock"
dblist = ["Stock50"]


def getLatestRecord():
    task = MyThread(find, None, None, True)
    task.start()
    res = task.getResult()
    list = res.sort("_id").limit(1)
    for item in list:
        return item[csv_headers[0]].strip()


def clickAndQuery(text):
    try:
        browser.get(url)
        # 点击弹出搜索框
        waitByClickAndID(browser, 10, "navTopMenuIcoSearch")
        input_dom = findByCssSelector(browser,
                                      "#topHeaderSearchInput #searchInput",
                                      False)
        # 输入关键词进行搜索
        input_dom.send_keys(text)
        time.sleep(10)
        # 等待结果点击第一个
        btn = findByCssSelector(browser, ".searchResults .searchItem", False)
        if btn:
            waitByClickAndSelector(browser, 10, ".searchResults .searchItem")
            getIndexPage()
        else:
            return
    except Exception as e:
        print(e)


def getIndexPage():
    # 获取最近记录
    date = getLatestRecord()
    # 由于点击结果页面url会改变，所以获取新页面的html
    browser.get(browser.current_url)
    # 等待页面加载
    time.sleep(5)
    a_dom = findByCssSelector(browser,
                              ".subCatMenuInstWrapper #historical-data a",
                              False)
    browser.get(a_dom.get_attribute("href"))
    now = time.strftime("%Y-%m-%d", time.localtime())
    # 点击历史项
    if date:
        if now == date:
            return
        getHistoryPage(date)
    else:
        getHistoryPage(origin_date)


def executeScripts(command):
    browser.execute_script(command)


def getHistoryPage(date):
    # 等待页面加载，直到时间选择图标可用
    waitByClickAndSelector(browser, 10, ".js-datepicker.pullRight")
    # 改变开始时间
    command = "document.getElementById('startDate').setAttribute('value','" + date + "')"
    executeScripts(command)
    # 点击进行重新查询
    button_dom = findById(browser, "datepickerBtn", False)
    button_dom.click()
    # 等待数据获取刷新
    time.sleep(10)
    try:
        # 获取结果数据
        tr = findByCssSelector(browser, ".scrollTbl .js-history-data tr", True)
        dealWithResultToExcel(tr)
        for item in tr:
            dealWithResultToMongo(item)
            dealWithResultToCSV(item)
        print("数据写入完成!")
    except StaleElementReferenceException:
        print("元素未找到!")


def dealWithResultToMongo(item):
    list = item.text.split(" ")
    pattern = re.compile("[\u4e00-\u9fa5]")
    if item.text and len(list) > 0:
        str = pattern.sub("-", list[0].strip())[0:-1]
        res = str.split("-")
        temps = []
        for i in res:
            if len(i) > 0 and len(i) < 2:
                temps.append("0" + i)
            else:
                temps.append(i)
        result = "-".join(temps)
        sql = {
            "日期": result,
            "收盘": list[1],
            "开盘": list[2],
            "高峰": list[3],
            "低峰": list[4],
            "交易量": list[5],
            "涨跌幅": list[6]
        }
        insert(sql)


def dealWithResultToCSV(item):
    list = item.text.split(" ")
    if item.text and len(list) > 0:
        writeCsvRow(list)


def dealWithResultToExcel(result):
    length = len(result)
    for i in range(0, length):
        list = result[i].text.split(" ")
        if result[i].text and len(list) > 0:
            for j in range(0, len(list)):
                writeExcelCell(i, j, list[j])


def getTextList(path):
    # a w r x
    list = []
    f = open(path, "r", encoding="utf-8")
    while True:
        text = f.readline().strip("\n")
        if text == "":
            break
        textlist = text.split(",")
        if len(textlist) > 1:
            list.append(textlist)
        else:
            list.append(text)
    f.close()
    return list


def process(csv_path, excel_path, headers, name, code, identify=True):
    csvClinet = initCSV(csv_path)
    print(name)
    excelClient = initExcel(name + "(" + code + ")")
    writeCsvHeader(headers)
    addCollect(name.replace("(", "") + "(" + code + ")")
    # A股
    if identify:
        clickAndQuery(code)
    else:
        clickAndQuery(name)
    csvClinet.close()
    excelClient.save(excel_path)


def main():
    # A股有些股票在香港也上市了，所以取个别名
    mongoClinet = initMongo()
    for i in range(len(pathlist)):
        text_list = getTextList(pathlist[i])
        addDB(dblist[i])
        for item in text_list:
            # str list tuple dict set int float
            if isinstance(item, list):
                group = re.match(r"\d+", item[0], re.I)
                name = item[1].strip()
                code = item[0].strip()
                # a股
                if group and len(code) == 6:
                    csv_path = csv_dir + name + ".csv"
                    excel_path = excel_dir + name + ".xls"
                    process(csv_path, excel_path, csv_headers, name, code)
                # 港股和美股
                else:
                    csv_path = csv_dir + name + ".csv"
                    excel_path = excel_dir + name + ".xls"
                    process(csv_path, excel_path, csv_headers, name, code,
                            False)
        mongoClinet.close()
        browser.close()


if __name__ == "__main__":
    main()
