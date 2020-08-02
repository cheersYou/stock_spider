from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys 键盘事件 Keys.ENTER
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import time
'''
单个元素
find_element_by_id === find_element(By.ID, id)
find_element_by_name
find_element_by_xpath
find_element_by_link_text
find_element_by_partial_link_text
find_element_by_tag_name
find_element_by_class_name
find_element_by_css_selector
'''
'''
多个元素
find_elements_by_id
find_elements_by_name
find_elements_by_xpath
find_elements_by_link_text
find_elements_by_partial_link_text
find_elements_by_tag_name
find_elements_by_class_name
find_elements_by_css_selector
'''
'''
send_keys(text) 输入文字
clear() 清空文字
click() 点击按钮
execute_script('script code') 执行里面代码
'''
'''
ele.get_attribute('attr_name') 获取元素属性信息
ele.text 获取元素文本信息
ele.id
ele.location
ele.tag_name
ele.size
'''
'''
browser.switch_to.frame('iframeResult') 切换到页面子frame里面
wait = WebDriverWait(browser, 10) 最大等待时间10s
wait.until(EC.presence_of_element_located((By.ID, 'q'))) 元素出现
EC.element_to_be_clickable 元素可点击
browser.back() 浏览器页面后退
browser.forward() 浏览器页面前进
browser.get_cookies() 获取浏览器cookies
browser.add_cookie({'name': 'name', 'domain': 'www.zhihu.com', 'value': 'germey'}) 添加cookies
browser.delete_all_cookies() 删除cookies
'''
browser = webdriver.Chrome("D:\Chrome\chromedriver.exe")
url = 'https://m.cn.investing.com/equities/icbc-ss-historical-data'
text = "宋城演艺"
date = "2017-01-01"
try:
    browser.get(url)
    wait_1 = WebDriverWait(browser, 10)
    a_click = wait_1.until(
        EC.element_to_be_clickable((By.ID, "navTopMenuIcoSearch")))
    a_click.click()
    input_text = browser.find_element_by_css_selector(
        "#topHeaderSearchInput #searchInput")
    input_text.send_keys(text)
    wait_2 = WebDriverWait(browser, 10)
    li_click = wait_2.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".searchResults .searchItem")))
    li_click.click()
    browser.get(browser.current_url)
    time.sleep(5)
    aa_click = browser.find_element_by_css_selector(
        ".subCatMenuInstWrapper #historical-data a")
    browser.get(aa_click.get_attribute("href"))
    wait_3 = WebDriverWait(browser, 10)
    icon_click = wait_3.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, ".js-datepicker.pullRight")))
    icon_click.click()
    command = "document.getElementById('startDate').setAttribute('value','" + date + "')"
    browser.execute_script(command)
    button_click = browser.find_element_by_id("datepickerBtn")
    button_click.click()
    time.sleep(10)
    try:
        tr = browser.find_elements_by_css_selector(
            ".scrollTbl .js-history-data tr")
        for item in tr:
            print(item.text)
    except StaleElementReferenceException:
        print("元素未找到")
finally:
    browser.close()
