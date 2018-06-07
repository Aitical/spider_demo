import MySQLdb as mdb
import requests
import datetime
import time
import random
import numpy as np


class SongComment(object):
    """
    抓取歌曲评论
    """
    def __init__(self, music, data, cachefile, comment_count=True, hotcomment=True):
        """
        初始化
        :param music: (dict) 163music信息
        :param data:  (dict) 163data信息
        :param cachefile: (string)缓存的路径
        """
        # self.cookies = [
        #     '_iuqxldmzr_=32; _ntes_nnid=335cac0c45f3c4a2936fe11b8c3fa4fa,1522327951584; _ntes_nuid=335cac0c45f3c4a2936fe11b8c3fa4fa; __utmc=94650624; _ngd_tid=5h%2FgzWeXegeNP7Sh8iFAE4gH2FsYOEIW; c98xpt_=30; __utmz=94650624.1523022908.9.7.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); JSESSIONID-WYYY=z5T%2Btz6SKTriSIXaw2KBIMFyU1NKblkyMMxqCZ%2BrJzOCBw4QTyZk%5CbjGa%5CTWFHN3TFPt0tyS%2Bk3HdU%2B%2Bk6sXmlUXMYyqIdmpwiAP7NvVAt0TROkqRsuIa1s6HO2zttAvlGSR%2FwmTujTevW78%2FyTt52fDcWRlFVs%5ChrvT2gXe66eOecIy%3A1523068699583; __utma=94650624.913370056.1522327952.1523022908.1523066900.10; __remember_me=true; jsessionid-cpta=dIHB5nrm%2FF4%2FvXv%2FV96fRVAOSWeSVNp7qFqWOrhPNVY%5CPmNd16M8nyojuyCXoG7PDCNHrpBqicXqhWFTb19J73mQh%2F%2FKBqCgK%2FBqjOrfpxe8BavIt%5CyZC%2FW3C7z4bdUTNoz5YlMqocS%5CjI4g64etw7bmXeynSq%2BeQn2ykFbWnEX5Jcbn%3A1523068200266; NETEASE_WDA_UID=1422500364#|#1523067306083; MUSIC_U=f36b31c39bfdb9e6428d92b86a5ad7035ad7bfae5457715220c01f2e6fbfe65494e1ecd047754f25e33205b379dcf4a533894ae9ba83d2fb305842396b5dfc01; __csrf=978d6938ae47c3133c9ad86426af5d0f; __utmb=94650624.10.10.1523066900',
        #     '_iuqxldmzr_=32; _ntes_nnid=335cac0c45f3c4a2936fe11b8c3fa4fa,1522327951584; _ntes_nuid=335cac0c45f3c4a2936fe11b8c3fa4fa; __utmc=94650624; _ngd_tid=5h%2FgzWeXegeNP7Sh8iFAE4gH2FsYOEIW; c98xpt_=30; jsessionid-cpta=PdZlHYKyNldeffLWpzq5ZJWd7k%2FI%2B2QjihA4mdwuq3J34%2B%2BHDkwEzBd4KWrItc5eTVFM1Uh8%2BZqQYFko2VbR9VjF1JLj2bTRrkdWHWgiWhMBDaIKiCq%5CUECz51fXRU%2BKPNeeTaeeyT7G0bYqfqny26kYn1p%5CFQeuBfg3%2BbWJnF51GTuB%3A1522377092742; __remember_me=true; NETEASE_WDA_UID=1413859162#|#1522376348040; __utmz=94650624.1523022908.9.7.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); JSESSIONID-WYYY=z5T%2Btz6SKTriSIXaw2KBIMFyU1NKblkyMMxqCZ%2BrJzOCBw4QTyZk%5CbjGa%5CTWFHN3TFPt0tyS%2Bk3HdU%2B%2Bk6sXmlUXMYyqIdmpwiAP7NvVAt0TROkqRsuIa1s6HO2zttAvlGSR%2FwmTujTevW78%2FyTt52fDcWRlFVs%5ChrvT2gXe66eOecIy%3A1523068699583; __utma=94650624.913370056.1522327952.1523022908.1523066900.10; MUSIC_U=2b7d2e648fd970fe9ca51a5757431b2f4af3aefa0477470af68db8afa9329fd7e4e4807cb5b1150eec3c599370197ad5975d75c3fbd629f6af9e62a8590fd08a; __csrf=387020d62ef08ec197f6e756358e234c; __utmb=94650624.5.10.1523066900',
        #     '_iuqxldmzr_=32; _ntes_nnid=335cac0c45f3c4a2936fe11b8c3fa4fa,1522327951584; _ntes_nuid=335cac0c45f3c4a2936fe11b8c3fa4fa; __utmc=94650624; _ngd_tid=5h%2FgzWeXegeNP7Sh8iFAE4gH2FsYOEIW; c98xpt_=30; __utmz=94650624.1523022908.9.7.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); JSESSIONID-WYYY=z5T%2Btz6SKTriSIXaw2KBIMFyU1NKblkyMMxqCZ%2BrJzOCBw4QTyZk%5CbjGa%5CTWFHN3TFPt0tyS%2Bk3HdU%2B%2Bk6sXmlUXMYyqIdmpwiAP7NvVAt0TROkqRsuIa1s6HO2zttAvlGSR%2FwmTujTevW78%2FyTt52fDcWRlFVs%5ChrvT2gXe66eOecIy%3A1523068699583; __utma=94650624.913370056.1522327952.1523022908.1523066900.10; jsessionid-cpta=dIHB5nrm%2FF4%2FvXv%2FV96fRVAOSWeSVNp7qFqWOrhPNVY%5CPmNd16M8nyojuyCXoG7PDCNHrpBqicXqhWFTb19J73mQh%2F%2FKBqCgK%2FBqjOrfpxe8BavIt%5CyZC%2FW3C7z4bdUTNoz5YlMqocS%5CjI4g64etw7bmXeynSq%2BeQn2ykFbWnEX5Jcbn%3A1523068200266; MUSIC_U=908e83b8c8fd5c91f9dfb19be87079cb4af3aefa0477470a31b52a8a6bbba1a2dd391d30b6661f58b48d9b66380ce10c0ee7cca2136854e441049cea1c6bb9b6; __remember_me=true; __csrf=a6c618016f9fb1ad94643aec8a6ef84b; __utmb=94650624.17.10.1523066900',
        #     '_iuqxldmzr_=32; _ntes_nnid=335cac0c45f3c4a2936fe11b8c3fa4fa,1522327951584; _ntes_nuid=335cac0c45f3c4a2936fe11b8c3fa4fa; __utmc=94650624; _ngd_tid=5h%2FgzWeXegeNP7Sh8iFAE4gH2FsYOEIW; c98xpt_=30; __utmz=94650624.1523022908.9.7.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); JSESSIONID-WYYY=z5T%2Btz6SKTriSIXaw2KBIMFyU1NKblkyMMxqCZ%2BrJzOCBw4QTyZk%5CbjGa%5CTWFHN3TFPt0tyS%2Bk3HdU%2B%2Bk6sXmlUXMYyqIdmpwiAP7NvVAt0TROkqRsuIa1s6HO2zttAvlGSR%2FwmTujTevW78%2FyTt52fDcWRlFVs%5ChrvT2gXe66eOecIy%3A1523068699583; __utma=94650624.913370056.1522327952.1523022908.1523066900.10; jsessionid-cpta=dIHB5nrm%2FF4%2FvXv%2FV96fRVAOSWeSVNp7qFqWOrhPNVY%5CPmNd16M8nyojuyCXoG7PDCNHrpBqicXqhWFTb19J73mQh%2F%2FKBqCgK%2FBqjOrfpxe8BavIt%5CyZC%2FW3C7z4bdUTNoz5YlMqocS%5CjI4g64etw7bmXeynSq%2BeQn2ykFbWnEX5Jcbn%3A1523068200266; __remember_me=true; NETEASE_WDA_UID=1422455964#|#1523067489621; MUSIC_U=66a4fdfbbcb3c6f3593e5ef0a9ac3ef65053be85f4706fa65b75ea7f098115df23858e0dd423430d583a4fa6e2db9498ee4ff258204fc789305842396b5dfc01; __csrf=7249e0dd60571932f4ca1f89f4f2d1d7; __utmb=94650624.22.10.1523066900',
        # ]
        self.message_music = music
        self.message_data = data
        self._comment_count = comment_count
        self._hotcomment = hotcomment
        self.cachefile = './workspace/' + cachefile
        self.header = {
            # 'Cookie': self.cookies[int(self.cachefile[-1])-1],
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
        }

    def save(self, data, table='comment'):
        """
        保存数据到数据库
        :param data: (list) 二位数组格式的数据
        :param table: (string) 要插入的表
        :return: None
        """
        message = self.message_music
        connection = mdb.connect(**message)
        print(len(data), 'MESSAGES INSERT INTO', table, 'SUCCESS')
        if 'user' == table:
            sql = 'INSERT INTO api_user(user_id, pic, name) VALUES(%s, %s, %s)'
        elif 'hotcomment' == table:
            sql = 'INSERT INTO api_hotcomment(song_id, content, comment_id, user_id, pub_time, liked_count) ' \
                  'VALUES (%s, %s, %s, %s, %s, %s)'
        else:
            sql = 'INSERT INTO api_comment(song_id, content, comment_id, user_id, pub_time, liked_count) ' \
                  'VALUES (%s, %s, %s, %s, %s, %s)'

        with connection.cursor() as cursor:
            cursor.executemany(sql, data)
        connection.commit()
        connection.close()

    def format_time(self, timestamp):
        """
        格式化时间格式
        :param timestamp:
        :return:
        """
        timearray = datetime.datetime.fromtimestamp(timestamp / 1000)
        return timearray.strftime("%Y-%m-%d %H:%M:%S.%f")

    def comment_count(self, song_id, total):
        message = self.message_music
        connection = mdb.connect(**message)
        # print(song_id, total)
        sql = "INSERT INTO api_commentcount(song_id, total, state) VALUES (%s, %s, %s)"
        with connection.cursor() as cursor:
            cursor.execute(sql, (song_id, total, 1))
        connection.commit()

    def get_ids(self, status='all'):
        """
        读取song_id
        :param status: (string) 读取的目标文件cache/all
        :return: (list) [id,id,...]
        """
        if status == 'cache':
            with open(self.cachefile + '/c_song_id.txt',) as fin:
                data = [i.split('\t')[0] for i in fin.readlines()]

        else:  # status == 'all'
            with open(self.cachefile + '/a_song_id.txt',) as fin:
                data = [i.strip() for i in fin.readlines()]

        return data

    def cache(self, song_id, status=None):
        """
        记录爬取信息
        用于增量抓取和断点继续
        :param song_id: (string/list) song_id
        :param status: (string) start/end
        :return: None
        """
        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if 'update' == status:
            with open(self.cachefile + '/a_song_id.txt', 'w') as fin:
                fin.write('\n'.join(song_id))
        elif 'error' == status:
            with open(self.cachefile + '/l_song_id.txt', 'a') as fin:
                fin.write(song_id + '\t' + status + '\t' + now_time + '\n')
        elif status is not None:
            status = status if isinstance(status, str) else str(status)
            with open(self.cachefile + '/l_song_id.txt', 'a') as fin:
                fin.write(song_id + '\t' + status + '\t' + now_time + '\n')
        else:
            with open(self.cachefile + '/c_song_id.txt', 'a') as fin:
                fin.write(song_id + '\t' + now_time + '\n')

    def get_hot_comments(self, song_id, data):
        """
        获取歌曲热评
        :param song_id: (string) song_id
        :param data: (list) 热评数据
        :return: None
        """
        all_comments_list = []  # 存放所有评论
        all_users_list = []
        for item in data:
            comment = item['content']  # 评论内容
            comment_id = item['commentId']  # 评论id
            likedcount = item['likedCount']  # 点赞总数
            comment_time = item['time']  # 评论时间(时间戳)
            userid = item['user']['userId']  # 评论者id
            nickname = item['user']['nickname']  # 昵称
            avatarurl = item['user']['avatarUrl']  # 头像地址
            comment_info = [str(song_id), comment, comment_id, userid, self.format_time(comment_time), likedcount]
            user_info = [str(userid), avatarurl, nickname]
            all_comments_list.append(comment_info)
            all_users_list.append(user_info)

        self.save(all_comments_list, 'hotcomment')
        self.save(all_users_list, 'user')

    def get_all_comments(self, song_id, start=0):
        """
        获取歌曲评论信息
        :param song_id: (string) 歌曲id
        :param start: (int) 开始记录数
        :return: None
        """
        song_id = song_id if isinstance(song_id, str) else str(song_id)
        all_comments_list = []  # 存放所有评论
        all_users_list = []  # 存放评论的用户信息
        url = 'http://music.163.com/api/v1/resource/comments/R_SO_4_' + song_id

        total = 0
        while True:
            param = {
                'limit': '20',
                'offset': str(start)
            }
            resp = requests.get(url, headers=self.header, params=param)
            data = resp.json()
            if 'msg' in data:
                self.cache(song_id, 'error')
                print('ip failed')
                exit()
            if self._comment_count and total == 0:
                total = data['total']
                self.comment_count(song_id, total)
                # print('total', total)

            if 'hotComments' in data and self._hotcomment and data['hotComments']:
                self.get_hot_comments(song_id, data['hotComments'])

            for item in data['comments']:
                comment = item['content']  # 评论内容
                comment_id = item['commentId']  # 评论id
                liked_count = item['likedCount']  # 点赞总数
                comment_time = item['time']  # 评论时间(时间戳)
                user_id = item['user']['userId']  # 评论者id
                nickname = item['user']['nickname']  # 昵称
                avatar_url = item['user']['avatarUrl']  # 头像地址
                comment_info = [song_id, comment, comment_id, user_id, self.format_time(comment_time), liked_count]
                user_info = [user_id, avatar_url, nickname]
                all_comments_list.append(comment_info)
                all_users_list.append(user_info)

            if start != 0 and start % 1000 == 0:
                """防止多评论中途异常终止,1000条保存一次"""
                self.save(all_comments_list)
                self.save(all_users_list, table='user')
                all_comments_list = []
                all_users_list = []
                self.cache(song_id, status=start)
                # print(start, 'success')

            if not data['more'] or start > total:
                break
            time.sleep(random.randint(12, 23) / 10)
            start += 20
            # print(start)

        self.save(all_comments_list)
        self.save(all_users_list, table='user')

    def run(self):
        """
        启动函数
        :return: None
        """
        all_id = self.get_ids()
        old_id = self.get_ids('cache')
        next_ids = np.unique(np.setdiff1d(all_id, old_id, assume_unique=True))
        # print(next_ids)
        self.cache(next_ids, status='update')
        print('songs')
        print('total:', len(all_id))
        print('have:', len(old_id))
        print('next:', len(next_ids))
        for song_id in next_ids:
            self.cache(song_id)
            self.get_all_comments(song_id)
            self.cache(song_id, status='end')


if __name__ == '__main__':
    message_music = {
        'host': '127.0.0.1',
        'user': 'root',
        'passwd': ' ',
        'db': '163music',
        'charset': 'utf8mb4'  # 指定编码格式!!!
    }

    message_data = {
        'host': '127.0.0.1',
        'user': 'root',
        'passwd': ' ',
        'db': '163data',
        'charset': 'utf8mb4'  # 指定编码格式!!!
    }
    my = SongComment(message_music, message_data, 'cache1')
    my.run()

