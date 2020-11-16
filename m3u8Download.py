# -*- coding:utf-8 -*-
import os
import shutil
import requests
import datetime
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex


def download(url):
	# 指定存储目录
    download_path = os.getcwd() + "/Downloads"
    if not os.path.exists(download_path):
        os.mkdir(download_path)

    # 新建日期文件夹
    download_path = os.path.join(
        download_path, datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
    # print download_path
    os.mkdir(download_path)

    # 获取第一层M3U8文件内容
    all_content = requests.get(url).text
    if "#EXTM3U" not in all_content:
        raise BaseException("非M3U8的链接")

 	# 第一层
    if "EXT-X-STREAM-INF" in all_content:
        file_line = all_content.split("\n")
        for line in file_line:
            if '.m3u8' in line:
            	# 拼出第二层m3u8的URL
                url = url.rsplit("/", 1)[0] + "/" + line
                all_content = requests.get(url).text

    file_line = all_content.split("\n")

    unknow = True
    key = ""
    # 第二层
    for index, line in enumerate(file_line):
    	# 找解密Key
        if "#EXT-X-KEY" in line:
            method_pos = line.find("METHOD")
            comma_pos = line.find(",")
            method = line[method_pos:comma_pos].split('=')[1]
            print("Decode Method：", method)

            uri_pos = line.find("URI")
            quotation_mark_pos = line.rfind('"')
            key_path = line[uri_pos:quotation_mark_pos].split('"')[1]

            # 拼出key解密密钥URL
            key_url = url.rsplit("/", 1)[0] + "/" + key_path
            res = requests.get(key_url)
            key = res.content
            print("key：", key)

        # 找ts地址并下载
        if "EXTINF" in line:
            unknow = False
            # 拼出ts片段的URL
            pd_url = url.rsplit("/", 1)[0] + "/" + file_line[index + 1]

            res = requests.get(pd_url)
            c_fule_name = file_line[index + 1].rsplit("/", 1)[-1]

            # AES 解密
            if len(key):
                cryptor = AES.new(key, AES.MODE_CBC, key)
                with open(os.path.join(download_path, c_fule_name + ".mp4"), 'ab') as f:
                    f.write(cryptor.decrypt(res.content))
            else:
                with open(os.path.join(download_path, c_fule_name), 'ab') as f:
                    f.write(res.content)
                    f.flush()
    if unknow:
        raise BaseException("未找到对应的下载链接")
    else:
        print("下载完成")
    merge_file(download_path)
    delete_ts(download_path)


def merge_file(path):
    path_list = []
    for file in os.listdir(path):
        if file.endswith('.ts'):
            path_list.append(file)
    path_list.sort()
    li = [os.path.join(path, filename) for filename in path_list]
    input_file = '|'.join(li)
    output_file = path + '.mp4'
    command = 'ffmpeg -i "concat:{}" -acodec copy -vcodec copy -absf aac_adtstoasc {}'.format(input_file, output_file)
    os.system(command)

def delete_ts(path):
    try:
        shutil.rmtree(path)
        print('ts文件已经删除')
    except:
        print('ts文件删除失败')

if __name__ == '__main__':
    print("爬取开始")
    start_url="http://acg17.com/tag/pixiv/"
    # 创建并修改至下载路径
    firstpath=r'D:'
    secondpath=r'D:\PythonDownload'
    thirdpath=r'D:\PythonDownload\m3u8'
    os.chdir(firstpath)
    if not os.path.exists(secondpath):
        os.mkdir(secondpath)
    if not os.path.exists(thirdpath):
        os.mkdir(thirdpath)
    os.chdir(thirdpath)
    retval=os.getcwd()

    url="https://vedu.csdn.net/media/m3u8_new_tmp/10085/2253d7de848351de21e59953dec373a4-215004.m3u8"
    download(url)

    print("爬取完成")
    input()
    os.system("pause")
