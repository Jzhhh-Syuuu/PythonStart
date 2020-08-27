#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import re
import time

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

Hostreferer = {
    # 'User-Agent': str(UserAgent().random),
    'User-Agent': 'Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
    'Referer': 'https://www.mzitu.com'
}

Picreferer = {
    # 'User-Agent': str(UserAgent().random),
    'User-Agent': 'Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
    'Referer': 'http://i.meizitu.net'
}


def get_page_name(url):  # 获得图集最大页数和名称
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    span = soup.findAll('span')
    title = soup.find('h2', class_="main-title")
    return span[9].text, title.text


def get_html(url):  # 获得页面html代码
    req = requests.get(url, headers=Hostreferer, timeout=(3, 7))
    html = req.text
    return html


def get_img_url(url, name):
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    img_url = soup.find('img', alt=name)
    return img_url['src']


def save_img(img_url, count, name):
    req = requests.get(img_url, headers=Picreferer, timeout=(3, 7))
    new_name = rename(name)
    with open(new_name+'/'+str(count)+'.jpg', 'wb') as f:
        f.write(req.content)


def rename(name):
    rstr = r'[\/\\\:\*\?\<\>\|]'
    new_name = re.sub(rstr, "", name)
    return new_name


def save_one_atlas(old_url):
    try:
        page, name = get_page_name(old_url)
        new_name = rename(name)
        if not os.path.exists(new_name):
            os.mkdir(new_name)

        print("图集--" + name + "--开始保存")
        for i in range(1, int(page)+1):

            url = old_url + "/" + str(i)
            img_url = get_img_url(url, name)
            # print(img_url)
            save_img(img_url, i, name)
            print('正在保存第' + str(i) + '张图片')
            time.sleep(0.2)

        print("图集--" + name + "保存成功")
        time.sleep(0.5)
    except TimeoutError:
        print("超时")
    except Exception as err:
        print("异常:"+str(err))
        pass


def get_atlas_list(url):
    req = requests.get(url, headers=Hostreferer, timeout=(3, 7))
    soup = BeautifulSoup(req.text, 'lxml')
    atlas = soup.find_all(attrs={'class': 'lazy'})
    atlas_list = []
    for atla in atlas:
        atlas_list.append(atla.parent['href'])
    return atlas_list


def save_one_page(start_url):
    atlas_url = get_atlas_list(start_url)
    for url in atlas_url:
        save_one_atlas(url)


if __name__ == '__main__':
    print("爬取开始")
    start_url = "https://www.mzitu.com/"
    os.chdir(r'D:\JZH\新建文件夹')
    retval = os.getcwd()
    for count in range(4, 10):
        url = start_url + "page/" + str(count) + "/"
        save_one_page(url)
    print("爬取完成")
    input()
