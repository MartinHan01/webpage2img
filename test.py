#!/usr/bin/python

# -*- coding: utf-8 -*-

from selenium import webdriver
import unittest
import fileutil
import sys
import time

def smooth_scroll_to_tail(driver, sleep_interal = 3):
    #滚动到底部
    all_height = driver.execute_script("return document.body.scrollHeight")
    screen_height = driver.execute_script("return window.innerHeight")
    num = int(all_height / (screen_height)) + 1

    pic_path = './result/image/'
    fileutil.mkdirs_if_not_exist(pic_path)
    for i in range(1, num):
        time.sleep(sleep_interal)

        current_time = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
        pic_name = current_time + '.png'
        driver.save_screenshot(pic_path + pic_name)

        
        height = screen_height * i
        js = "window.scrollTo(0,%d)" % (height)
        driver.execute_script(js)


def scrollToTail(driver):
    #滚动到底部
    js = "window.scrollTo(0,document.body.scrollHeight)" 
    driver.execute_script(js)

def scrollToTop(driver): 
    #滚动到顶部
    js = "window.scrollTo(0,0)" 
    driver.execute_script(js)




#import HTMLTestReportHTMLTestReport
# 登录
driver = webdriver.Chrome()
current_time = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
current_time1 = time.strftime("%Y-%m-%d", time.localtime(time.time()))
print(current_time)
print(current_time1)

driver.get("https://mp.weixin.qq.com/s/zL0RLdc9TQdR9-tjkMM_PA")
# 新创建路径“.”表示当前整个.py文件的路径所在的位置，“\\”路径分割符，其中的一个是“\”表示转义字符
pic_path = '.\\result\\image\\' + current_time1+'\\' + current_time + '.png'
print(pic_path)
# time.sleep(5)
print(driver.title)
# 截取当前url页面的图片，并将截取的图片保存在指定的路径下面（pic_path），注：以下两种方法都可以

smooth_scroll_to_tail(driver)

time.sleep(5)

pagesource = driver.page_source


with open("hello.html", 'wt', encoding='utf-8') as f:
    f.write(pagesource)
    f.flush()
    





