#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import re
import time

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

Hostreferer = {
    'User-Agent': str(UserAgent().random),
    # 'User-Agent': 'Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
    'Referer': 'http://acg17.com'
}

Picreferer = {
    'User-Agent': str(UserAgent().random),
    # 'User-Agent': 'Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
    'Referer': 'http://acg17.com'
}


def get_page_name(url):  # 获得图集最大页数和名称
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    title = soup.find('span', itemprop="name")
    return title.text


def get_html(url):  # 获得页面html代码
    req = requests.get(url, headers=Hostreferer, timeout=(3, 7))
    html = req.text
    return html


def get_img_url(url, name):
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    # img_url = soup.find_all('img', alt=name+'- ACG17.COM')
    img_url = soup.find_all('img', attrs={
                            'alt': name+'- ACG17.COM', 'referrerpolicy': not('no-referrer'), 'class': not('wxpic')})
    return img_url


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
        name = get_page_name(old_url)
        new_name = rename(name)
        if not os.path.exists(new_name):
            os.mkdir(new_name)
        else:
            print("图集--" + name + "--已存在")
            pass

        print("图集--" + name + "--开始保存")

        i = 1

        url = old_url
        img_urls = get_img_url(url, name)
        for img_url in img_urls:
            # print(img_url)
            save_img(img_url['src'], i, name)
            print('正在保存第' + str(i) + '张图片')
            i = i+1
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
    atlas = soup.find_all(attrs={'class': 'more-link'})
    atlas_list = []
    for atla in atlas:
        atlas_list.append(atla['href'])
    return atlas_list


def save_one_page(start_url):
    atlas_url = get_atlas_list(start_url)
    for url in atlas_url:
        save_one_atlas(url)


if __name__ == '__main__':
    print("爬取开始")
    start_url = "http://acg17.com/tag/pixiv/"
    # 创建并修改至下载路径
    firstpath = r'D:'
    secondpath = r'D:\PythonDownload'
    thirdpath = r'D:\PythonDownload\acg17-pixiv'
    os.chdir(firstpath)
    if not os.path.exists(secondpath):
        os.mkdir(secondpath)
    if not os.path.exists(thirdpath):
        os.mkdir(thirdpath)
    os.chdir(thirdpath)
    retval = os.getcwd()

    for count in range(1, 10):
        url = start_url + "page/" + str(count) + "/"
        save_one_page(url)
    print("爬取完成")
    input()
