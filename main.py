    #!/usr/bin/python

# -*- coding: utf-8 -*-

from selenium import webdriver
import unittest
import fileutil
import sys
import time
import os
import pictureutil


filelist = [
    'https://mp.weixin.qq.com/s/zL0RLdc9TQdR9-tjkMM_PA'
    
]

def save_url(driver, url, dir):
    index = 0
    driver.get(url)
    title_element = driver.find_element_by_xpath("//div//h2[@class='rich_media_title']")
    title = title_element.text
    pic_path = os.path.join(dir, 'result', title)
    fileutil.mkdirs_if_not_exist(pic_path)

    

    all_height = driver.execute_script("return document.body.scrollHeight")
    screen_height = driver.execute_script("return window.innerHeight")
    num = int(all_height / (screen_height))

    for i in range(0, num):
        time.sleep(1)
        pic_name = str(i) + '.png'
        driver.save_screenshot(os.path.join(pic_path,pic_name))
        height = screen_height * (i + 1)
        js = "window.scrollTo(0,%d)" % (height)
        driver.execute_script(js)
    
    
def package_picture(dir, save_path):
    if os.chdir(dir) == False:
        print('chdir ' + str(dir) + ' error')
        exit(-1)
    if os.path.isdir(dir) == False:
        print(str(dir) + ' is not a dir')
        exit(-1)
    
    list = os.listdir(dir)
    for i in list:
        title = i
        pic_dir = os.path.join(dir, title)
        pic_list = os.listdir(pic_dir)
        save_file = os.path.join(save_path, title + '.png')
        pictureutil.merge_pic(pic_dir, pic_list, os.path.abspath(save_file))




if __name__ == '__main__':
    driver = webdriver.Chrome()
    dir = './result'
    for item in filelist:
        save_url(driver, item, dir)
    
    package_picture(dir, os.path.join(dir))

    