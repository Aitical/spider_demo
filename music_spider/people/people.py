# -*- coding: utf-8 -*- 
# @Time : 18-5-19 下午2:53 
# @Author : Aitical
# @File : people.py 
# @Software: PyCharm

import requests
from bs4 import BeautifulSoup
import MySQLdb as mdb
import datetime
import time
import json


DEBUG = False


class People(object):
    """
    抓取人民网文章的爬虫
    """
    def __init__(self, start_num, people_db, times):
        """
        构造函数,初始化数据库信息和请求部分
        :param start_num: 起始页码
        :param people_db: 存储的数据库信息
        """

        self.__search_url = 'http://search.people.com.cn/cnpeople/search.do'
        self.session = requests.Session()
        self.session.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Length': '103',
            'Host': 'search.people.com.cn',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        }
        # 设置page_num范围
        self.start_num = start_num
        self.__range = 134842
        self.end_num = self.__range * start_num + 1
        self.__db = people_db
        self.conn = mdb.connect(**self.__db)
        self.cache_file = str(start_num)+'_running_log.txt'
        self.error_times = times

    def _search_param(self, page_num, keyword='的'):
        """
        返回search接口的请求参数
        :param page_num:
        :param keyword:
        :return:
        """
        param = {
            'pageNum': str(page_num),
            'keyword': keyword.encode('GBK'),
            'siteName': 'news',
            'facetFlag': 'true',
            'nodeType': 'belongsId',
            'nodeId': '0'
        }
        return param

    def _save(self, data, table='search'):

        if 'search' == table:
            sql = 'INSERT INTO people.search(title, summary, href, pub_time) VALUES(%s, %s, %s, %s)'
        else:
            sql = ''

        with self.conn.cursor() as cursor:
            cursor.executemany(sql, data)
        self.conn.commit()
        print(len(data), 'MESSAGES INSERT INTO', table, 'SUCCESS', end=' ')

    def _cache(self, table_name, current_id, model='normal'):

        write_content = [table_name, str(current_id), datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
        with open(self.cache_file, 'a') as fin:
            fin.write('\t'.join(write_content)+'\n')

    def _start(self):

        try:
            with open(self.cache_file) as fin:
                file_content = fin.readlines()
                start_page = (self.start_num - 1) * self.__range if len(file_content) == 0 else int(file_content[-1].strip().split('\t')[1])

        except FileNotFoundError:
            start_page = (self.start_num - 1) * self.__range

        if DEBUG:
            print(start_page)

        return start_page

    def search(self, start_page):
        """
        搜索接口函数,抓取keyword返回的所有条目信息
        :return:
        """
        error_times = 0
        count = 0
        start = start_page + 1 if start_page != 0 else self.__range * (self.start_num - 1) + 1

        for page_num in range(start, self.end_num):

            if error_times > self.error_times:
                return

            page_content = []

            try:
                resp = self.session.post(self.__search_url, data=self._search_param(page_num))
            except requests.exceptions.ConnectionError:
                time.sleep(30)
                try:
                    resp = self.session.post(self.__search_url, data=self._search_param(page_num))
                except requests.exceptions.ConnectionError:
                    error_times += 1
                    continue

            if DEBUG:
                print(resp.cookies)

            soup = BeautifulSoup(resp.text.encode('gb2312'), 'lxml')

            div = soup.find('div', attrs={'class': 'fr w800'})
            uls = div.find_all('ul')
            for ul in uls:
                # 每一个ul就是一篇文章的基本信息
                lis = ul.find_all('li')
                # 获取到一个字段的3个信息部分,title,href, abstract, date
                title = lis[0].find('b').text
                href = lis[0].find('a')['href']
                summary = lis[1].text
                pub_time = lis[2].text.split('\xa0\xa0\xa0\xa0')[1]
                if DEBUG:
                    print(title, href, summary, pub_time)

                page_content.append((title, summary, href, pub_time))

            self._save(page_content)
            self._cache('search', page_num)
            # 显示本次运行采集到的文章
            count += 20
            print(count)

            if DEBUG:
                break

            #time.sleep(3)

    def run(self):
        _times = 0
        while _times < self.error_times:
            try:
                start_page = self._start()
                print('从', start_page, '页开始启动')
                self.search(start_page)
            except IndexError:
                _times += 1
                time.sleep(30)


if __name__ == '__main__':

    with open('config.json') as fin:
        config = json.load(fin)

    people = People(config['RUNNING_ID'], config['DB']['people'], config['ERROR_TIMES'])
    people.run()
