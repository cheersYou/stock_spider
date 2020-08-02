from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
import time


def waitByLocateAndID(browser, t, selector):
    try:
        wait = WebDriverWait(browser, t)
        ele = wait.until(EC.presence_of_element_located((By.ID, selector)))
        return ele
    except TimeoutException as e:
        print(e)


def waitByClickAndID(browser, t, selector):
    try:
        wait = WebDriverWait(browser, t)
        ele = wait.until(EC.element_to_be_clickable((By.ID, selector)))
        ele.click()
    except TimeoutException as e:
        print(e)
    except ElementClickInterceptedException as e:
        print("元素不能点击:", e)


def waitByLocateAndSelector(browser, t, selector):
    try:
        wait = WebDriverWait(browser, t)
        ele = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
        return ele
    except TimeoutException as e:
        print(e)


def waitByClickAndSelector(browser, t, selector):
    try:
        wait = WebDriverWait(browser, t)
        ele = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
        ele.click()
    except Exception:
        time.sleep(10)
        waitByClickAndSelector(browser, t, selector)
