from selenium import webdriver
# from selenium.common.exceptions import StaleElementReferenceException
from utils.wait import waitByClickAndSelector
from utils.find import findByCssSelector
import time
browser = webdriver.Chrome("D:\Chrome\chromedriver.exe")

url_300 = 'http://quote.eastmoney.com/center/boardlist.html#boards-BK05001'
url_50 = "http://quote.eastmoney.com/center/boardlist.html#boards-BK06111"
url_us = ""
url_hongkong_famous = "http://quote.eastmoney.com/center/gridlist.html#hk_wellknown"
url_hongkong_red = "http://quote.eastmoney.com/center/gridlist.html#hk_redchips"
url_hongkong_blue = "http://quote.eastmoney.com/center/gridlist.html#hk_bluechips"
url_us_chinese = "http://finance.sina.com.cn/stock/usstock/cnlist.html"
path_hongkong_famous = "hongkong_famous.txt"
path_hongkong_red = "hongkong_red.txt"
path_hongkong_blue = "hongkong_blue.txt"
path_300 = "300.txt"
path_50 = "50.txt"
path_us_chinese = "us_chinese.txt"
path_us = "us.txt"

f = open(path_us_chinese, "a", encoding="utf-8")


def process(index, list):
    i = index
    res = []
    while len(list[i]) == 1:
        res.append(list[i])
        i = i + 1
    return res


def getPageInfo(baseurl):
    browser.get(baseurl)
    list = findByCssSelector(browser, "#table_wrapper-table tbody tr", True)
    for i in list:
        temp = process(2, i.text.split(" "))
        if len(temp):
            res = i.text.split(" ")[1] + "," + "".join(temp) + "\r"
            f.writelines(res)
        else:
            res = i.text.split(" ")[1] + "," + i.text.split(" ")[2] + "\r"
            f.writelines(res)
    try:
        dom = findByCssSelector(
            browser, "#main-table_paginate .next.paginate_button.disabled",
            False)
        if dom.text:
            f.close()
            return
    except Exception:
        waitByClickAndSelector(browser, 10,
                               "#main-table_paginate .next.paginate_button")
        time.sleep(5)
        getPageInfo(browser.current_url)


def getPageInfoUS():
    list = findByCssSelector(browser, "#divContainer tbody tr", True)
    for i in list:
        if i.text:
            res = i.text.split(" ")[1] + "," + i.text.split(" ")[0] + "\r"
            f.writelines(res)
    try:
        dom = findByCssSelector(browser, "#divPages .pagedisabled", True)
        if dom[len(dom) - 1].text == '下一页':
            f.close()
            return
        else:
            command = "document.querySelectorAll('#divPages a')[document.querySelectorAll('#divPages a').length-1].click()"
            browser.execute_script(command)
            time.sleep(10)
            getPageInfoUS()
    except Exception:
        command = "document.querySelectorAll('#divPages a')[document.querySelectorAll('#divPages a').length-1].click()"
        browser.execute_script(command)
        time.sleep(10)
        getPageInfoUS()


def start(isUS=True):
    if isUS:
        browser.get(url_us_chinese)
        getPageInfoUS()
    else:
        getPageInfo(url_300)


def main():
    start()


if __name__ == "__main__":
    main()
