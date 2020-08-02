from selenium import webdriver
from utils.wait import waitByClickAndSelector
from utils.find import findByCssSelector
from database.mongo import initMongo, addCollect, addDB, insert
from database.mongoUp import initMongoUP, addCollectUP, addDBUP, insertUP
import time

url = "http://quote.eastmoney.com/center/hsbk.html"
base_url = "http://quote.eastmoney.com/center/boardlist.html"
browser = webdriver.Chrome("D:\Chrome\chromedriver.exe")
db_name_1 = "IndustryBank"
db_name_2 = "ConceptBank"


def getIndustryPage(url):
    addDB(db_name_1)
    writeBKInfo(url, "#hybkzf_simple-table tbody tr")
    list = findByCssSelector(browser, "#hybkzf_simple-table tr .mywidth3 a",
                             True)
    bklist = []
    for i in list:
        link = i.get_attribute("href")
        code = link.split("/")[-1].split(".")[1] + ""
        name = i.get_attribute("title")
        if name and code[0:2] == "BK":
            bklist.append({"name": name, "code": code})
    for j in bklist:
        addCollect(j["name"])
        code = j["code"]
        bk_url = base_url + "#boards-" + code
        browser.get(bk_url)
        getBKPage()


def getConceptPage(url):
    addDBUP(db_name_2)
    writeBKInfo(url, "#gnbkzf_simple-table tbody tr", False)
    list = findByCssSelector(browser, "#gnbkzf_simple-table tr .mywidth3 a",
                             True)
    bklist = []
    for i in list:
        link = i.get_attribute("href")
        code = link.split("/")[-1].split(".")[1] + ""
        name = i.get_attribute("title")
        if name and code[0:2] == "BK":
            bklist.append({"name": name, "code": code})
    for j in bklist:
        addCollectUP(j["name"])
        code = j["code"]
        bk_url = base_url + "#boards-" + code
        browser.get(bk_url)
        getBKPage(False)


def getBKPage(isIndustry=True):
    time.sleep(5)
    list = findByCssSelector(browser, "#table_wrapper-table tbody tr", True)
    temps = []
    for i in list:
        textlist = i.text.split(" ")
        name = ""
        skipNum = 0
        k = 0
        for j in textlist:
            if k >= 2:
                if textlist[k + 1] == "股吧":
                    name = name + j
                    break
                else:
                    name = name + j
                    skipNum = k - 1
            k = k + 1
        item = {
            "代码": textlist[1],
            "名称": name,
            "最新价": textlist[6 + skipNum],
            "涨跌幅": textlist[7 + skipNum],
            "涨跌额": textlist[8 + skipNum],
            "成交量手": textlist[9 + skipNum],
            "成交额": textlist[10 + skipNum],
            "振幅": textlist[11 + skipNum],
            "最高价": textlist[12 + skipNum],
            "最低价": textlist[13 + skipNum],
            "今开": textlist[14 + skipNum],
            "昨收": textlist[15 + skipNum],
            "换手率": textlist[17 + skipNum],
            "市盈率": textlist[18 + skipNum]
        }
        temps.append(item)
    now = time.strftime("%Y-%m-%d", time.localtime())
    sql = {"日期": now, "结果": temps}
    if isIndustry:
        insert(sql)
    else:
        insertUP(sql)
    try:
        findByCssSelector(browser, "#main-table_paginate .next", False)
        try:
            dom = findByCssSelector(browser,
                                    "#main-table_paginate .next.disabled",
                                    False)
            if dom.text:
                return
        except Exception:
            waitByClickAndSelector(browser, 10, "#main-table_paginate .next")
            getBKPage(isIndustry)
    except Exception:
        return


def writeBKInfo(url, selector, isIndustry=True):
    now = time.strftime("%Y-%m-%d", time.localtime())
    if isIndustry:
        addCollect(now)
    else:
        addCollectUP(now)
    browser.get(url)
    list = findByCssSelector(browser, selector, True)
    items = []
    for i in list:
        temps = i.text.split(" ")
        item = {
            "排名": temps[0],
            "板块名称": temps[1],
            "涨跌幅": temps[5],
            "换手率": temps[6],
            "涨跌家数": temps[7],
            "领涨股票": temps[8],
            "领涨跌幅": temps[9]
        }
        items.append(item)
    now = time.strftime("%Y-%m-%d", time.localtime())
    sql = {"日期": now, "结果": items}
    if isIndustry:
        insert(sql)
    else:
        insertUP(sql)


def main():
    mongoClinet_1 = initMongo()
    getIndustryPage(url)
    mongoClinet_1.close()
    mongoClinet_2 = initMongoUP()
    getConceptPage(url)
    mongoClinet_2.close()
    browser.close()


if __name__ == "__main__":
    main()