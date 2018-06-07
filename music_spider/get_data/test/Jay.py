import MySQLdb as mdb
import requests
import datetime
import time
import random
import numpy as np



class SongComment(object):
    def __init__(self, music, data):
        self.message_music = music
        self.message_data = data
        self.user_agent = [
            'Mozilla/5.0(Macintosh;U;IntelMacOSX10_6_8;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50',
            'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;Trident/4.0;SE2.XMetaSr1.0;SE2.XMetaSr1.0;.NETCLR2.0.50727;SE2.XMetaSr1.0)',
            'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;TheWorld)'
        ]
        self.cookies = [#'JSESSIONID-WYYY=P32sGYfqAvYU6H23DdiAg8%2FIMGimN3wqnOW5RlpI6MKWeIH4l5m03qxG5g7Rnbzgiv2pCfeqKfpW%2F835Mi6en4AJhOJ%2BRwounsMC6%5Ck0v28%2BO%2FIQH4tGeKsVkCaGupjhoj7Rm6m6vqXZUNBVjV1eEXI3yken8sZiwhbgD%2B2uCCMPqjyM%3A1522326512556; _iuqxldmzr_=32; _ntes_nnid=902a13702f1f47c57c8d892a48fe8e50,1522324712574; _ntes_nuid=902a13702f1f47c57c8d892a48fe8e50; __utma=94650624.1868574649.1522324713.1522324713.1522324713.1; __utmb=94650624.3.10.1522324713; __utmc=94650624; __utmz=94650624.1522324713.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; _ngd_tid=c0ILFHeC9fmKAEKzyXNBYoW3tXNIH%2Bdr; MUSIC_U=c5e4d9f1810e8c6350df923f848c2fc75053be85f4706fa6040ff8368d2198fa6c2fb1cb3845ef54304ab340c0024add55b984ecc5791ae17955a739ab43dce1; __remember_me=true; __csrf=25d7d174466104956f4a102d947372e1; jsessionid-cpta=dhOrMh5jXQkQaO4D0Xv3LSoeiOjbwLfN91VzkEhnJoPN98F3ah8cBwjHTKZ%5Cr07Y3%2FUTGhmS8y%5Cm9ovRh0np5Gr%2FKZJduaYx%2Fyd2DKYDKLzPetgd4rTQ8DAX0%5C9Pj1b%2FxfgpByDZwmKC74ttCjxdvHXUNZXpxr2wIf8ITFgTqiNYAVD5%3A1522325629212; c98xpt_=30; NETEASE_WDA_UID=1413429286#|#1522324736789',
                        #'JSESSIONID-WYYY=V4reY9co4%2FNbyaczTsxhV93Zy52QuOPuO1Zi6SoIa1SrKKwq9%2BiJMk%2BK7XCGbtn%2BtrI50BSooRo%2BeAmWAhPHMBjwysy5Kqr2nSu935vf%2F1JdHH5S%2F7ooKlqh8Gsru0vu%2Bj670Z9VZ2CvK%5CG1RiKDZU0szv5YV4Sh97WVRoIfsErpT%5C3u%3A1522326646020; _iuqxldmzr_=32; _ntes_nnid=e8e57baa6fb6e3539e0f89b823c6a7c4,1522324846040; _ntes_nuid=e8e57baa6fb6e3539e0f89b823c6a7c4; __utma=94650624.200538770.1522324846.1522324846.1522324846.1; __utmb=94650624.3.10.1522324846; __utmc=94650624; __utmz=94650624.1522324846.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; _ngd_tid=c0ILFHeC9fmKAEKzyXNBYoW3tXNIH%2Bdr; MUSIC_U=a30f98e438ea5a6ea1525a4b980a0661f5c85d16795274c610d36c0353d3b669acdae644ba873cf410a83950f1ebf67c21e270360c9f7e278bafcdfe5ad2b092; __remember_me=true; __csrf=0234c21dfd6f403152aadd37376024ca; jsessionid-cpta=kyUEIPjWvm%5CZUlSp%2FlLj8ywDer9CFJbNDjDjEFQao1zjLVyTKXg5GMxLNZj1BEnRWknndGI8ifmEofJlDGtZZky%2BfJaaTWk0JEV241wuk4q6%5CPKY5bGMB5Hx0kQ%5CauJkx%2Bf1uNOABTpj%2Fbfu301rLADn7IUABg%2FPJKqyGDpm%2FGlDimzQ%3A1522325763242; c98xpt_=30; NETEASE_WDA_UID=1413380662#|#1522324872453',
                        #'JSESSIONID-WYYY=zMs8Th5%2FD%2FeTtvgvpHxn6O50rP4wDH%2BkGpOdl%2FIFdm2awjZkBRtl4qrT4c1VAaYXBUH%2FrMJ%2Fsv04gP4Q4taBqVuv0ST53rV0jawcFNlWOAfiAe1IfOS7oiElsdK95GqcbzAAw3l3rB3as9DV0Hu%2FcuwAzobmE3ckseE5D1Yw%2FbqMlu%2Fs%3A1522329751562; _iuqxldmzr_=32; _ntes_nnid=335cac0c45f3c4a2936fe11b8c3fa4fa,1522327951584; _ntes_nuid=335cac0c45f3c4a2936fe11b8c3fa4fa; __utma=94650624.913370056.1522327952.1522327952.1522327952.1; __utmc=94650624; __utmz=94650624.1522327952.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _ngd_tid=5h%2FgzWeXegeNP7Sh8iFAE4gH2FsYOEIW; MUSIC_U=a31c40a104c2963969e31fe09bf6a05a99dcb9d14e06692f387c86f6f494b012d389189cc37e02d5f91e03a084a50452b002576125207950aae8191e03cfd4b6c3061cd18d77b7a0; __remember_me=true; __csrf=f9b2a968649759735562f965d81c259b; jsessionid-cpta=obnJI%2F7wbIyYc3pKovXtkd%5CTm4CJbAF0Y1k9pt%2BBi5mZlvjyIeh%5CF6prT0hqkaYQ%5CnGoOR%2F9ZSaHGnJQ%2BPh9O%2FNXzXMyi2TpfEjHDIuJV16qWu%2ByeTAtq6IOQjRRXJRrImkVzFEVG%5C8CSioOWUu%2BcK%2BfcyuZfi%2FMe6El36xi259jvDZY%3A1522328868118; c98xpt_=30; NETEASE_WDA_UID=1413386931#|#1522327976539; __utmb=94650624.3.10.1522327952',
                        '_iuqxldmzr_=32; _ntes_nnid=335cac0c45f3c4a2936fe11b8c3fa4fa,1522327951584; _ntes_nuid=335cac0c45f3c4a2936fe11b8c3fa4fa; __utmc=94650624; _ngd_tid=5h%2FgzWeXegeNP7Sh8iFAE4gH2FsYOEIW; c98xpt_=30; JSESSIONID-WYYY=z2WNFlNfbGai%2Btdmw2NKvDSIEOGKdYIbMBAzUUtxxJFCaZ7gTnQxAGB4eNnWdfrNTc52b3nf45%5CHH5V5DiRqXqsmsYhcE6t3nCfCREPg0dUTE3WbRiIw31svhTyz9H%5CGl8WGXP6qmrarN95X%2F7XSUyOdFroloz1%5ChwYPd4gJ0Q27YJ0F%3A1522377807514; __utma=94650624.913370056.1522327952.1522330431.1522376008.3; __utmz=94650624.1522376008.3.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); MUSIC_U=1fc7c116f1574cda91285de2db7219445ad7bfae5457715298bf5584c14d2f14ebb0aeb303e24bba2081e3371e25dfa1351b44d836dc963af2f513a9c38b5dc7; __remember_me=true; __csrf=e043b39dd9180c91dfe9c0e9ab9d6c15; jsessionid-cpta=PdZlHYKyNldeffLWpzq5ZJWd7k%2FI%2B2QjihA4mdwuq3J34%2B%2BHDkwEzBd4KWrItc5eTVFM1Uh8%2BZqQYFko2VbR9VjF1JLj2bTRrkdWHWgiWhMBDaIKiCq%5CUECz51fXRU%2BKPNeeTaeeyT7G0bYqfqny26kYn1p%5CFQeuBfg3%2BbWJnF51GTuB%3A1522377092742; NETEASE_WDA_UID=1413839268#|#1522376204076; __utmb=94650624.7.10.1522376008',
                        '_iuqxldmzr_=32; _ntes_nnid=335cac0c45f3c4a2936fe11b8c3fa4fa,1522327951584; _ntes_nuid=335cac0c45f3c4a2936fe11b8c3fa4fa; __utmc=94650624; _ngd_tid=5h%2FgzWeXegeNP7Sh8iFAE4gH2FsYOEIW; c98xpt_=30; JSESSIONID-WYYY=z2WNFlNfbGai%2Btdmw2NKvDSIEOGKdYIbMBAzUUtxxJFCaZ7gTnQxAGB4eNnWdfrNTc52b3nf45%5CHH5V5DiRqXqsmsYhcE6t3nCfCREPg0dUTE3WbRiIw31svhTyz9H%5CGl8WGXP6qmrarN95X%2F7XSUyOdFroloz1%5ChwYPd4gJ0Q27YJ0F%3A1522377807514; __utma=94650624.913370056.1522327952.1522330431.1522376008.3; __utmz=94650624.1522376008.3.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); jsessionid-cpta=PdZlHYKyNldeffLWpzq5ZJWd7k%2FI%2B2QjihA4mdwuq3J34%2B%2BHDkwEzBd4KWrItc5eTVFM1Uh8%2BZqQYFko2VbR9VjF1JLj2bTRrkdWHWgiWhMBDaIKiCq%5CUECz51fXRU%2BKPNeeTaeeyT7G0bYqfqny26kYn1p%5CFQeuBfg3%2BbWJnF51GTuB%3A1522377092742; __remember_me=true; MUSIC_U=2b7d2e648fd970fe9ca51a5757431b2f4af3aefa0477470a2ae1b1fe6a7a8370a442cb96aca31ec58926e614a2ad00bb55c222d9e5c0ebca41049cea1c6bb9b6; __csrf=459b4ce74c74d9d5d942201c71f0a7b4; NETEASE_WDA_UID=1413859162#|#1522376348040; __utmb=94650624.11.10.1522376008']
        self.header = {
            'Cache-Control': 'max-age=0',
        'User-Agent': self.user_agent[random.randint(0,3)%3],
        'Cookies': self.cookies[0],#random.randint(0,50)%5],,
        'Upgrade-Insecure-Requests': '1',
        'Host': 'music.163.com',
        }

    def mogu_proxy(self):
        message = {
        'host': '127.0.0.1',
        'user': 'root',
        'passwd': ' ',
        'db': '163data',
        'charset': 'utf8mb4'  # 指定编码格式!!!
        }
        conn = mdb.connect(**message)

        with conn.cursor() as cursor:
            sql = 'SELECT * FROM api_moguproxy'
            cursor.execute(sql)
            data = random.choice(cursor.fetchall())
        conn.commit()
        conn.close()
        proxiex = {'http': 'http://' + data[1] + ':' + data[2]}
        print(proxiex)
        return proxiex


    def saveComment(self, data):
        message = self.message_music
        connection = mdb.connect(**message)
        print(len(data), 'comments')
        with connection.cursor() as cursor:
            sql = 'INSERT INTO Jay(song_id, content, comment_id, user_id, pub_time, liked_count, replied_user_id) VALUES (%s, %s, %s, %s, %s, %s, %s)'
            cursor.executemany(sql, data)

        connection.commit()

    def saveUser(self, data):
        message = self.message_music
        connection = mdb.connect(**message)
        print(len(data), 'users')
        with connection.cursor() as cursor:
            sql = 'INSERT INTO api_user(user_id, pic, name) VALUES(%s, %s, %s)'
            cursor.executemany(sql, data)

        connection.commit()

    def formatTime(self, timeStamp):
        timeArray = datetime.datetime.fromtimestamp(timeStamp / 1000)
        return timeArray.strftime("%Y-%m-%d %H:%M:%S.%f")

    def comment_count(self, songid, total):
        message = self.message_music
        connection = mdb.connect(**message)
        print(songid, total)
        sql = "INSERT INTO api_commentcount(song_id, total, state) VALUES (%s, %s, %s)"
        with connection.cursor() as cursor:
            cursor.execute(sql, (songid, total, 1))
        connection.commit()

    def get_all_comments(self, songid, start):
        _start = start
        all_comments_list = []  # 存放所有评论
        all_users_list = []
        url = 'http://music.163.com/api/v1/resource/comments/R_SO_4_' + str(songid)

        total = 0
        while True:
            param = {
                'limit': '20',
                'offset': str(start)
            }
            resp = requests.get(url, headers=self.header, params=param,)
            data = resp.json()
            print(data.keys())
            if total == 0:
                total = data['total']
                self.comment_count(songid, total)
                print('total', total)
            
            for item in data['comments']:
                comment = item['content']  # 评论内容
                comment_id = item['commentId']  # 评论id
                likedcount = item['likedCount']  # 点赞总数
                comment_time = item['time']  # 评论时间(时间戳)
                userid = item['user']['userId']  # 评论者id
                nickname = item['user']['nickname']  # 昵称
                avatarurl = item['user']['avatarUrl']  # 头像地址
                replied_user_id = item['beReplied'][0]['user']['userId'] if  item['beReplied'] else '#'
                comment_info = [str(songid), comment, comment_id, userid, self.formatTime(comment_time), likedcount, replied_user_id]
                user_info = [str(userid), avatarurl, nickname]
                all_comments_list.append(comment_info)
                all_users_list.append(user_info)

            if start != _start and start % 1000 == 0:
                self.saveComment(all_comments_list)
                self.saveUser(all_users_list)
                with open('start.txt', 'w') as f:
                    f.write(str(start))
                all_comments_list = []
                all_users_list = []
                print(start, 'success')

            if not data['more']:
                break
            #time.sleep(random.randint(22, 33) / 10)
            start += 20
            #print(start)

        self.saveComment(all_comments_list)
        with open('start.txt', 'w') as f:
            f.write(str(start))
        self.saveUser(all_users_list)
        self.comment_count(songid, total)


    def file_start(self, song_id):
        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open('song_count.txt', 'a') as fin:
            fin.write(song_id + '\tstart\t' + now_time + '\n')

    def file_end(self, song_id):
        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open('song_count.txt', 'a') as fin:
            fin.write(song_id + '\tend\t' + now_time + '\n')

    def run(self, start):
        song_id = '186016'
        self.file_start(song_id)
        self.get_all_comments(song_id, start)
        self.file_end(song_id)
            

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
    my = SongComment(message_music, message_data)
    while True:
        with open('start.txt') as f:
            start = 0
            print(start)
        try:
            my.run(start)
        except ConnectionError:
            print("Error")
            time.sleep(1)


