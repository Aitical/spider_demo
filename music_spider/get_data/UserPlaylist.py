import MySQLdb as mdb
import requests
import datetime
import time
import random

import numpy as np


class UserPlaylist(object):

    def __init__(self, music, data, cachefile):
        self.message_music = music
        self.message_data = data
        self.cachefile = './workspace/' + cachefile
        self.url = "http://music.163.com/api/user/playlist"
        self.header = {
        'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
        }

    def cache(self, user_id, status=None):

        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if 'update' == status:
            with open(self.cachefile + '/a_user_id_p.txt', 'w') as fin:
                fin.write('\n'.join(user_id))
        elif 'cache' == status:
            with open(self.cachefile + '/c_user_id_p.txt', 'a') as fin:
                fin.write(user_id + '\n')
        else:
            with open(self.cachefile+'/l_user_id_p.txt', 'a') as fin:
                fin.write(user_id + '\t' + now_time + '\n')

    def get_ids(self, status='all'):
        """
        读取song_id
        :param status: (string) 读取的目标文件cache/all
        :return: (list) [id,id,...]
        """
        if status == 'cache':
            with open(self.cachefile + '/c_user_id_p.txt',) as fin:
                data = [i.split('\t')[0] for i in fin.readlines()]

        else:  # status == 'all'
            with open(self.cachefile + '/a_user_id_p.txt',) as fin:
                data = [i.strip() for i in fin.readlines()]

        return data

    def get_next_id(self):
        """
        获取/更新id列表
        :return: (list) [id1,id2,...]
        """
        user_ids = self.get_ids()
        old_ids = self.get_ids('cache')
        next_ids = np.setdiff1d(user_ids, old_ids, assume_unique=True)
        self.cache(next_ids, 'update')
        print('total:', len(user_ids))
        print('have:', len(old_ids))
        print('next:', len(next_ids))
        return next_ids

    def save(self, data, table):
        """
        数据存储到数据库
        :param data: (list) 数据
        :param table: (string) 要存储的表名
        :return: None
        """
        message = self.message_music
        connection = mdb.connect(**message)
        if 'user_playlist' == table:
            sql = sql = "INSERT INTO api_user_playlist(user_id, playlist_id) VALUES (%s, %s)"
        elif 'creator' == table:
            sql = "INSERT INTO 163music.api_creator(user_id, authStatus, avatarUrl, backgroundUrl, birthday, " \
                  "province, city, description, detailDescription, expertTags, gender, nickname, signature) " \
                  "VALUES (%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s)"
        else:
            sql = "INSERT INTO api_playlistmessage(playlist_id, coverImgUrl, createTime, creator, description, " \
                  "name, playCount, subscribedCount, tags, trackCount) " \
                  "VALUES (%s, %s,%s, %s,%s, %s,%s, %s,%s, %s)"
        with connection.cursor() as cursor:
            cursor.executemany(sql, data)
        connection.commit()
        connection.close()
        print(len(data), 'MESSAGES INSERT INTO', table)

    def get_playlist_and_user_message(self, user_id, offset=0):
        """
        抓取playlist和user信息
        :param user_id: (string) user_id
        :param offset: (string/int) 抓取的起始号
        :return: None
        """
        playlist_data = []
        user_playlist = []
        creator_data = []
        res_status = True
        while True:
            param = {
                'offset': offset,
                'limit': '40',
                'uid': user_id
            }
            resp = requests.get(self.url, params=param, headers=self.header).json()

            if 'playlist' not in resp:
                res_status = False
                break

            playlists = resp['playlist']
            length = len(playlists)
            for playlist in playlists:
                creator = playlist['creator']
                playlist_data.append((
                    playlist['id'],
                    playlist['coverImgUrl'],
                    playlist['createTime'],
                    playlist['userId'],
                    playlist['description'],
                    playlist['name'],
                    playlist['playCount'],
                    playlist['subscribedCount'],
                    ';'.join(playlist['tags']) if playlist['tags'] is not None else None,
                    playlist['trackCount']
                ))

                user_playlist.append((
                    playlist['userId'],
                    playlist['id'],
                ))

                creator_data.append((
                    creator['userId'],
                    creator['authStatus'],
                    creator['avatarUrl'],
                    creator['backgroundUrl'],
                    creator['birthday'],
                    creator['province'],
                    creator['city'],
                    creator['description'],
                    creator['detailDescription'],
                    ';'.join(creator['expertTags']) if creator['expertTags'] is not None else None,
                    creator['gender'],
                    creator['nickname'],
                    creator['signature']
                ))
            if not resp['more'] and length < 40:
                break
            offset += 40
            time.sleep(random.randint(22, 33) / 10)

        if res_status:
            self.save(creator_data, 'creator')
            self.save(user_playlist, 'user_playlist')
            self.save(playlist_data, 'playlist_message')
            self.cache(user_id)

        return res_status

    def run(self):
        next_ids = self.get_next_id()
        for user_id in next_ids:
            status = self.get_playlist_and_user_message(user_id)
            if status:
                time.sleep(random.randint(22, 33) / 10)
                self.cache(user_id, 'cache')
            else:
                print('playlist ip failed')
                self.cache(user_id, 'failed')
                time.sleep(3*60*60)


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
    my = UserPlaylist(message_music, message_data, 'cache1')
    my.run()

