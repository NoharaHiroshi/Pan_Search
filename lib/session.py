# coding=utf-8
import contextlib
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


@contextlib.contextmanager
def get_session(url):
    cap = webdriver.DesiredCapabilities.PHANTOMJS
    cap["phantomjs.page.settings.loadImages"] = False
    cap["phantomjs.page.settings.localToRemoteUrlAccessEnabled"] = False
    browser = webdriver.PhantomJS(desired_capabilities=cap)
    try:
        browser.get(url)
        WebDriverWait(browser, 10, 0.5).until_not(EC.visibility_of(browser.find_element_by_id('inifiniteListViewTips')))
        yield browser
    except Exception as e:
        print e
    finally:
        browser.quit()
