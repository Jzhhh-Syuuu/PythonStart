
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
# available since 2.4.0
from selenium.webdriver.support.ui import WebDriverWait
# available since 2.26.0
from selenium.webdriver.support import expected_conditions as EC
import csv
import re
import sys
import os
import random


class Boss:
    def __init__(self):
        # 设置 chrome 无界面化模式
        self.chrome_options = webdriver.ChromeOptions()
        # self.chrome_options.add_argument('--headless')
        # self.chrome_options.add_argument('--disable-gpu')
        # self.chrome_options.add_argument('no-sandbox')
        self.driver = webdriver.Chrome(chrome_options=self.chrome_options)

    def get_url(self, search='python'):
        """
        获取搜索职位的url, demo里面默认搜索python
        :param search:
        :return:
        """
        gangwei_lst = [".net"]
        for search in gangwei_lst:
            xuhao = 1
            # 创建文件
            wr.csv_init(search)
            for y in range(1, 11):
                try:
                    self.driver.switch_to.window(sreach_window)
                except:
                    pass
                url = 'https://www.zhipin.com/c101020100/?query=' + \
                    str(search) + '&page=' + str(y) + '&ka=page-' + str(y)
                self.driver.get(url)

                # 获取当前窗口
                sreach_window = self.driver.current_window_handle
                # 每页有 30 条内容
                for x in range(1, 31):
                    data = []
                    try:
                        self.driver.find_element_by_xpath(
                            "//*[text()='没有找到相关职位，修改筛选条件试一下']")
                    except:
                        self.driver.switch_to.window(sreach_window)
                        try:
                            xpath_yanzhengma = self.driver.find_element_by_id(
                                "verifyMessage").text
                            print(xpath_yanzhengma)
                            if "当前IP地址可能存在异常访问行为，完成验证后即可正常使用" in xpath_yanzhengma:
                                print('输入验证码验证')
                                os.system("pause")
                        except:
                            pass

                        # 公司名称
                        try:
                            xpath_gongsi_name = '//*[@id="main"]/div/div[2]/ul/li[' + str(
                                x) + ']/div/div[1]/div[2]/div/h3/a'
                            WebDriverWait(self.driver, 60, 0.5).until(
                                EC.presence_of_element_located((By.XPATH, xpath_gongsi_name)))
                            gongsi_name = self.driver.find_element_by_xpath(
                                xpath_gongsi_name).text

                        except:
                            print('爬取完成！')

                        # 薪资
                        try:
                            xpath_xinzi = '//*[@id="main"]/div/div[2]/ul/li[' + \
                                str(x) + ']/div/div[1]/div[1]/a/div[2]/span'
                            WebDriverWait(self.driver, 3, 0.5).until(
                                EC.presence_of_element_located((By.XPATH, xpath_xinzi)))
                            xinzi = self.driver.find_element_by_xpath(
                                xpath_xinzi).text

                        except:
                            xinzi = ""

                        # 岗位名称
                        try:
                            xpath_gangwei = '//*[@id="main"]/div/div[2]/ul/li[' + \
                                str(x) + ']/div/div[1]/div[1]/a/div[1]/span[1]'
                            WebDriverWait(self.driver, 3, 0.5).until(
                                EC.presence_of_element_located((By.XPATH, xpath_gangwei)))
                            gangwei = self.driver.find_element_by_xpath(
                                xpath_gangwei).text
                        except:
                            gangwei = ""

                        # 公司大小
                        try:
                            xpath_size = '//*[@id="main"]/div/div[2]/ul/li[' + \
                                str(x) + ']/div/div[1]/div[2]/div/p'
                            WebDriverWait(self.driver, 3, 0.5).until(
                                EC.presence_of_element_located((By.XPATH, xpath_size)))
                            type_size = self.driver.find_element_by_xpath(
                                xpath_size).text
                            gongsi_size = re.findall(
                                r'\d+-\d+人', type_size)[0]  # 正则表达式提取数字，返回一个列表

                            if gongsi_size == '':
                                gongsi_size = re.findall(
                                    r'\d+', type_size)  # 正则表达式提取数字，返回一个列表
                                gongsi_type = type_size.split(gongsi_size)[0]
                            else:
                                gongsi_type = type_size.split(gongsi_size)[0]
                        except:
                            gongsi_size = ""
                            gongsi_type = ""

                        # 公司福利
                        try:
                            xpath_fuli = '//*[@id="main"]/div/div[2]/ul/li[' + \
                                str(x) + ']/div/div[2]/div[2]'
                            WebDriverWait(self.driver, 1, 0.5).until(
                                EC.presence_of_element_located((By.XPATH, xpath_fuli)))
                            gongsi_fuli = self.driver.find_element_by_xpath(
                                xpath_fuli).text

                        except:
                            gongsi_fuli = ""

                        # 工作经验
                        try:
                            xpath_jingyan = '//*[@id="main"]/div/div[2]/ul/li[' + \
                                str(x) + ']/div/div[1]/div[1]/a/div[2]/p'
                            WebDriverWait(self.driver, 1, 0.5).until(
                                EC.presence_of_element_located((By.XPATH, xpath_jingyan)))
                            jingyan_xueli = self.driver.find_element_by_xpath(
                                xpath_jingyan).text
                            xueli = ['硕士', '大专', '本科', '博士', '专科']
                            for xue in xueli:
                                if xue in jingyan_xueli:
                                    gongsi_jingyan = jingyan_xueli.split(xue)[
                                        0]
                                    gongsi_xueli = jingyan_xueli.split(
                                        gongsi_jingyan)[1]
                                    break
                        except:
                            gongsi_jingyan = ""
                            gongsi_xueli = ""

                        # 详情页
                        try:
                            time.sleep(random.randint(1, 4))
                            xpath_dingwei = '//*[@id="main"]/div/div[2]/ul/li[' + \
                                str(x) + ']/div/div[1]'
                            WebDriverWait(self.driver, 1, 0.5).until(
                                EC.presence_of_element_located((By.XPATH, xpath_dingwei)))
                            continue1 = self.driver.find_element_by_xpath(
                                xpath_dingwei)
                            continue1.click()

                            all_window = self.driver.window_handles
                            for handle in all_window:
                                if handle != sreach_window:
                                    self.driver.switch_to.window(handle)
                                    # 岗位描述
                                    try:
                                        xpath_miaoshu = '//*[@id="main"]/div[3]/div/div[2]/div[2]/div[1]/div'
                                        WebDriverWait(self.driver, 5, 0.5).until(
                                            EC.presence_of_element_located((By.XPATH, xpath_miaoshu)))
                                        miaoshu = self.driver.find_element_by_xpath(
                                            xpath_miaoshu).text

                                    except:
                                        miaoshu = ""

                                    # 工作地址
                                    try:
                                        dizhi = self.driver.find_element_by_class_name(
                                            "location-address").text

                                    except:
                                        dizhi = ""
                                    self.driver.close()  # 关闭当前标识的窗口
                        except:
                            miaoshu = ""
                            dizhi = ""
                        data.append(xuhao)
                        data.append(gongsi_name)
                        data.append(gongsi_size)
                        data.append(gongsi_type)
                        data.append(gangwei)
                        data.append(gongsi_xueli)
                        data.append(gongsi_jingyan)
                        data.append(miaoshu)
                        # 年龄为空
                        data.append("")
                        # 工作时间为空
                        data.append("")
                        data.append(gongsi_fuli)
                        data.append(xinzi)
                        data.append(dizhi)
                        # 备注
                        data.append("")
                        wr.write(data)
                        print("已完成" + str(xuhao) + "条")
                        time.sleep(random.randint(1, 5))
                        xuhao += 1
                    else:
                        self.driver.refresh()


class WriteDataToCSV:
    def csv_init(self, path):
        self.path = "./" + str(path) + ".csv"
        # 1. 创建文件对象
        self.f = open(self.path, 'a+', encoding='utf-8', newline="")
        # 2. 基于文件对象构建 csv写入对象
        self.csv_writer = csv.writer(self.f)
        # 3. 构建列表头
        self.csv_writer.writerow(["序号", "企业名称", "企业规模", "性质/行业", "岗位名称", "学历要求",
                                  "工作经验", "专业要求", "年龄要求", "工作时间", "社保福利", "薪酬范围",
                                  "工作地点", "备注"])
        # 4. 关闭文件
        self.f.close()

    def write(self, data):
        with open(self.path, 'a+', encoding='utf-8', newline="") as f:
            csv_writer = csv.writer(f)
            # 4. 写入csv文件内容
            csv_writer.writerow(data)

#爬取很慢 并且chormedriver会一直弹出窗口
if __name__ == '__main__':
     # 创建并修改至下载路径
    firstpath = r'D:'
    secondpath = r'D:\PythonDownload'
    thirdpath = r'D:\PythonDownload\bosszhipin'
    os.chdir(firstpath)
    if not os.path.exists(secondpath):
        os.mkdir(secondpath)
    if not os.path.exists(thirdpath):
        os.mkdir(thirdpath)
    os.chdir(thirdpath)
    retval = os.getcwd()
    wr = WriteDataToCSV()
    Boss().get_url()
    print("爬取完成")
    input()
    os.system("pause")