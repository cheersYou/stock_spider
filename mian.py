import urllib.request
from bs4 import BeautifulSoup

url = "https://m.cn.investing.com/equities/icbc-ss-historical-data"
headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36"
}


def startRequest(url, data, headers, method):
    return urllib.request.Request(url=url,
                                  data=data,
                                  headers=headers,
                                  method=method)


def getHtml():
    try:
        request = startRequest(url, None, headers, "GET")
        res = urllib.request.urlopen(request)
        parseHtml(res.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(e)


def parseHtml(res):
    # 解析器：html.parser lxml html5hib
    source = BeautifulSoup(res, "lxml")
    target = source.select(".scrollTblWrap .js-history-data")
    print(target)


def main():
    getHtml()


if __name__ == "__main__":
    main()
