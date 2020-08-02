def findById(browser, selector, isMulti):
    if isMulti:
        return browser.find_elements_by_id(selector)
    else:
        return browser.find_element_by_id(selector)


def findByCssSelector(browser, selector, isMulti):
    if isMulti:
        return browser.find_elements_by_css_selector(selector)
    else:
        return browser.find_element_by_css_selector(selector)