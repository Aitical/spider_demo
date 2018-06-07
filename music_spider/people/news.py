# -*- coding: utf-8 -*- 
# @Time : 18-5-25 下午1:22 
# @Author : Aitical
# @File : news.py 
# @Software: PyCharm

import requests
from bs4 import BeautifulSoup
import MySQLdb as mdb
import datetime
import time
import json
import re

DEBUG = False


class News(object):
    """
    抓取文章内容的爬虫
    """
    def __init__(self, start_id, people_db, times):
        self.session = requests.Session()
        self.session.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',

            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
            'Referer': 'http://search.people.com.cn/cnpeople/news/getNewsResult.jsp'
        }
        self.__db = people_db
        self.conn = mdb.connect(**self.__db)
        self.start_id = (start_id - 1) * 10000
        self.cache_file = str(start_id - 1) + '_news_log.txt'
        self.error_times = times

    def _get_urls(self, start_id):

        sql = "SELECT href from people.search where id >= %d limit 100" % (start_id)
        print(sql)
        with self.conn.cursor() as cursor:
            cursor.execute(sql)
            res = [i[0] for i in cursor.fetchall()]
        return res

    def _save(self, data, table='news'):

        sql = 'INSERT INTO people.news (title, keywords, summary, content, pub_time, editor) ' \
              'VALUES (%s, %s, %s, %s, %s, %s)'

        with self.conn.cursor() as cursor:
            cursor.executemany(sql, data)
        self.conn.commit()
        print(len(data), 'MESSAGES INSERT INTO', table, 'SUCCESS', end=' ')

    def _cache(self, current_id):

        write_content = ['news', str(current_id), datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
        with open(self.cache_file, 'a') as fin:
            fin.write('\t'.join(write_content)+'\n')

    def _start(self):
        try:
            with open(self.cache_file) as fin:
                file_content = fin.readlines()
                start_id = self.start_id if len(file_content) == 0 else int(file_content[-1].strip().split('\t')[1])

        except FileNotFoundError:
            start_id = self.start_id

        return start_id

    def format_str(self, string):
        string.replace('\'', '$')
        string.replace('"', '#')
        return '\'' + string + '\''

    def get_news(self, urls):

        data = []
        for url in urls:
            print(url)

            try:
                resp = self.session.get(url, timeout=60)
            except requests.exceptions.ConnectTimeout:
                print('timeout')
                continue
            resp.encoding = 'gb2312'
            if resp.status_code != 200:
                print(resp.status_code)
                continue
            soup = BeautifulSoup(resp.text, 'lxml')
            try:
                keywords = soup.find('meta', attrs={'name': 'keywords'})['content'].strip().replace(' ', '#')
            except TypeError:
                keywords = '未获取'

            try:
                description = soup.find('meta', attrs={'name': 'description'})['content'].strip()
            except TypeError:
                description = '未获取'

            try:
                pub_time = soup.find('meta', attrs={'name': 'publishdate'})['content']
            except TypeError:
                pub_time = '未获取'

            try:
                title = soup.find('title').text
            except AttributeError:
                title = '未获取'

            ps = soup('p')
            contents = '\n'.join([i.text.strip() for i in ps if '\u3000' not in i.text.strip() and len(i.text) > 10 and '登录人民网通行证' not in i.text and '他账号登录' not in i.text])

            try:
                ed = re.compile('(责编：.+)')
                editor = re.search(ed, soup.text).group()
            except AttributeError:
                try:
                    ed = re.compile('(来源:.+)')
                    editor = re.search(ed, soup.text).group()
                except AttributeError:
                    editor = '未获取'
            data.append((
                title,
                keywords,
                description,
                contents,
                pub_time,
                editor
            ))
            time.sleep(3)

            if DEBUG:
                print(data)
                return False

        print(len(data), len(data[0]))
        self._save(data)

        return True

    def run(self):
        times = 1
        while True:
            start_id = self._start()
            urls = self._get_urls(start_id)
            _status = self.get_news(urls)
            if _status:
                self._cache(start_id + 100)
                print(times * 100)
                times += 1
            if DEBUG:
                break

    def __del__(self):
        self.conn.close()


if __name__ == '__main__':
    with open('config.json') as fin:
        config = json.load(fin)
    news = News(config['RUNNING_ID'], config['DB']['people'], config['ERROR_TIMES'])
    news.run()
