import time
from CONFIG import *
from selenium import webdriver


def login(url):

    # 启动chrome
    driver = webdriver.Chrome(PHOTOMJS_DIR)
    # 登陆QQ空间登陆页面
    driver.get(url)
    # 开启睡眠
    time.sleep(3)

    # 实现登陆功能
    driver.find_element_by_xpath('//div[@class="bottom hide"]/a[1]').click()
    driver.find_element_by_xpath('//input[@id="u"]').send_keys(QQUSER)
    driver.find_element_by_xpath('//input[@id="p"]').send_keys(QQPASSWORD)
    driver.find_element_by_xpath('//input[@id="login_button"]').click()
    time.sleep(3)

    # 获取cookies值，并且实际使用格式
    cookies = {}
    for item in driver.get_cookies():
        cookies[item["name"]] = item["value"]

    return cookies



