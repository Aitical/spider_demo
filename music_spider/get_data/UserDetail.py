import MySQLdb as mdb
import requests
import datetime
import time
import random
from bs4 import BeautifulSoup
import re
import numpy as np


class UserDetail(object):
    def __init__(self, music, data, cachefile):
        self.message_music = music
        self.message_data = data
        self.cachefile = './workspace/' + cachefile
        self.url = 'https://music.163.com/user/home'
        self.header = {
        'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
        }

    def get_text(self, find):
        if find is not None:
            return find.text[5:]
        else:
            return None

    def get_loaction(self, resp):
        loc = re.compile('<span>所在地区：(.+)</span>')
        location = re.search(loc, resp)
        if location is not None:
            location = location.groups()[0]
            if '-' in location:
                location = location.split(' - ')
                return location[0], location[1]
            else:
                return location, location
        else:
            return None, None

    def get_age(self, age):
        if age is not None:
            timestamp = age['data-age']
            return timestamp
        else:
            return None

    def get_user_detail(self, user_id):

        param = {
            'id': user_id
        }
        resp = requests.get(self.url, headers=self.header, params=param)
        soup = BeautifulSoup(resp.text, 'lxml')
        # 必填字段
        user_name = soup.find('span', attrs={'class': 'tit f-ff2 s-fc0 f-thide'}).text
        level = soup.find('span', attrs={'class': 'lev u-lev u-icn2 u-icn2-lev'}).text  # 等级
        event_count = soup.find('strong', attrs={'id': 'event_count'}).text
        follow_count = soup.find('strong', attrs={'id': 'follow_count'}).text
        fan_count = soup.find('strong', attrs={'id': 'fan_count'}).text
        sex = 0 if soup.find('i', attrs={'class': 'icn u-icn u-icn-01'}) is not None else 1  # 0是男 1是女

        # 可选字段
        self_des = self.get_text(soup.find('div', attrs={'class': 'inf s-fc3 f-brk'}))
        province, city = self.get_loaction(resp.text)
        age = self.get_age(age=soup.find('span', attrs={'id': 'age'}))

        data = [(
            user_id,
            user_name,
            level,
            sex,
            event_count,
            follow_count,
            fan_count,
            city,
            age,
            self_des,
            province,
        )]
        return data

    def save(self, data):
        """
        存入数据库
        :param data: (list) 二维数组
        :return: None
        """
        sql = "INSERT INTO api_userdetail" \
              "(user_id, user_name, level, sex, event_count, follow_count, fan_count, loc_city, age, self_desc, loc_province) " \
              "VALUES (%s, %s,%s, %s,%s, %s,%s, %s,%s, %s, %s)"

        message = self.message_music
        connection = mdb.connect(**message)
        c = connection.cursor()
        c.executemany(sql, data)
        c.close()
        connection.commit()
        connection.close()

    def get_ids(self, status='all'):
        """
        读取song_id
        :param status: (string) 读取的目标文件cache/all
        :return: (list) [id,id,...]
        """
        if status == 'cache':
            with open(self.cachefile + '/c_user_id.txt',) as fin:
                data = [i.split('\t')[0] for i in fin.readlines()]

        else:  # status == 'all'
            with open(self.cachefile + '/a_user_id.txt',) as fin:
                data = [i.strip() for i in fin.readlines()]

        return data

    def cache(self, user_id, status=None):
        """
        记录爬取信息
        用于增量抓取和断点继续
        :param user_id: (string/list) user_id
        :param status: (string) update/None
        :return: None
        """
        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if 'update' == status:
            with open(self.cachefile + '/a_user_id.txt', 'w') as fin:
                fin.write('\n'.join(user_id))
        elif 'cache' == status:
            with open(self.cachefile + '/c_user_id.txt', 'a') as fin:
                fin.write('\n'.join(user_id)+'\n')
        elif 'error' == status:
            with open(self.cachefile+'/l_user_id.txt', 'a') as fin:
                fin.write(user_id + '\t' + status + '\t' + now_time + '\n')
        else:
            with open(self.cachefile+'/l_user_id.txt', 'a') as fin:
                fin.write(user_id + '\t' + now_time + '\n')

    def run(self):
        data = []
        ids = []
        user_ids = self.get_ids()
        old_ids = self.get_ids(status='cache')
        next_ids = np.unique(np.setdiff1d(user_ids, old_ids, assume_unique=True))
        self.cache(next_ids, 'update')
        print('users')
        print('total:', len(user_ids))
        print('have:', len(old_ids))
        print('next:', len(next_ids))
        for user_id in next_ids:
            count = 0
            while True:
                try:
                    ids.append(user_id)
                    self.cache(user_id)
                    data.extend(self.get_user_detail(user_id))
                    time.sleep(random.randint(7, 17) / 10)
                    break
                except AttributeError:
                    self.cache(user_id, 'error')
                    if count == 3:
                        break
                    count += 1
                    time.sleep(1)

            if len(ids) != 0 and len(ids) % 100 == 0:
                self.save(data)
                self.cache(ids, 'cache')
                data = []
                ids = []


if __name__ == '__main__':
    message_music = {
        'host': '127.0.0.1',
        'user': 'root',
        'passwd': ' ',
        'db': '163res',
        'charset': 'utf8mb4'  # 指定编码格式!!!
    }

    message_data = {
        'host': '127.0.0.1',
        'user': 'root',
        'passwd': ' ',
        'db': '163res',
        'charset': 'utf8mb4'  # 指定编码格式!!!
    }
    my = UserDetail(message_music, message_data, 'cache1')
    my.run()
    print('finished!')

