# coding=utf-8
import contextlib
from selenium import webdriver

@contextlib.contextmanager
def get_session():
    browser = webdriver.Chrome()
    try:
        yield browser
    except Exception as e:
        print e
        raise
    finally:
        browser.close()