#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import sys
import time
from urllib import request

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


"""
	下载爱奇艺vip视频
	安装：	
		安装selenium: pip/conda install selenium
		安装PhantomJS： sudo apt-get install nodejs
				 sudo apt-get install npm
				 sudo npm -g install phantomjs-prebuilt
				 phantomjs --version
	原理：
		获取爱奇艺vip视频的url，比如：http://www.iqiyi.com/v_19rr8u7i0g.html
		通过base_url=http://www.qmaile.com/网站解析
		通过selenium 和 phantomjs 获取到真实的下载网址
		通过request.urlretrieve进行下载
"""


class DownloadVipVideo(object):
    def __init__(self, target_url):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(chrome_options=self.chrome_options)
        # self.driver = webdriver.PhantomJS()
        self.wait = WebDriverWait(self.driver, 15)
        self.base_url = 'http://www.qmaile.com/'
        self.target_url = target_url

    def get_video_url(self):
        self.driver.get(self.base_url)

        self.wait.until(EC.presence_of_all_elements_located((By.ID, 'url')))
        self.wait.until(EC.presence_of_all_elements_located((By.ID, 'bf')))

        ins = self.driver.find_element_by_id('url')
        ins.send_keys(target_url)

        button = self.driver.find_element_by_id('bf')
        button.click()

        time.sleep(10)

        self.driver.switch_to.frame(0)

        page_source = BeautifulSoup(self.driver.page_source, 'lxml')
        print(page_source)
        res_url = page_source.find(id='vod')['src']
        self.driver.close()
        return str(res_url)

    def Schedule(self, a, b, c):
        per = 100.0 * a * b / c
        if per > 100:
            per = 1
        sys.stdout.write("  " + "%.2f%% 已经下载的大小:%ld 文件大小:%ld" %
                         (per, a * b, c) + '\r')
        sys.stdout.flush()

    def video_download(self, url, filename):
        request.urlretrieve(url=url, filename=filename,
                            reporthook=self.Schedule)


if __name__ == '__main__':
     # 创建并修改至下载路径
    firstpath = r'D:'
    secondpath = r'D:\PythonDownload'
    thirdpath = r'D:\PythonDownload\iqiyi'
    os.chdir(firstpath)
    if not os.path.exists(secondpath):
        os.mkdir(secondpath)
    if not os.path.exists(thirdpath):
        os.mkdir(thirdpath)
    os.chdir(thirdpath)
    retval = os.getcwd()

    target_url = 'https://www.iqiyi.com/v_161aqcqh0b0.html'
    downloader = DownloadVipVideo(target_url)
    res_url = downloader.get_video_url()
    print('开始下载视频')
    print("下载的url：---- "+res_url)
    if res_url.index('mp4') < 0:
        print('此视频暂不支持下载')
        sys.exit()
    downloader.video_download(res_url, 'test1.mp4')
    print('下载结束')
    sys.stdout.flush()
    input()
    os.system("pause")
