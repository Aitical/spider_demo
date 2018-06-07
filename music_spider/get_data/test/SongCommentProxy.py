import MySQLdb as mdb
import requests
import datetime
import numpy as np
from Crypto.Cipher import AES
import base64


class SongCommentProxy(object):
    """
    抓取歌曲评论
    """
    # 第二个参数
    second_param = "010001"
    # 第三个参数
    third_param = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
    # 第四个参数
    forth_param = "0CoJUm6Qyw8W8jud"

    def __init__(self, music, data, cachefile, comment_count=True, hotcomment=True, time_t=200):
        """
        初始化
        :param music: (dict) 163music信息
        :param data:  (dict) 163data信息
        :param cachefile: (string)缓存的路径
        :param comment_count: (bool) 默认开启记录歌曲评论
        :param hotcomment: (bool) 默认开启抓取热评
        :param time_t: (int) 切换代理ip时间间隔(秒)
        """
        with open('./workspace/ips.csv') as fin:
            self.ips = [i.split(',')[1] for i in fin.readlines()[1:]]
        self.time_t = time_t
        self.start_time = datetime.datetime.now()
        self.message_music = music
        self.message_data = data
        self._cookies = [
            '_iuqxldmzr_=32; _ntes_nnid=335cac0c45f3c4a2936fe11b8c3fa4fa,1522327951584; _ntes_nuid=335cac0c45f3c4a2936fe11b8c3fa4fa; __utmc=94650624; _ngd_tid=5h%2FgzWeXegeNP7Sh8iFAE4gH2FsYOEIW; c98xpt_=30; __utmz=94650624.1523022908.9.7.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); jsessionid-cpta=dIHB5nrm%2FF4%2FvXv%2FV96fRVAOSWeSVNp7qFqWOrhPNVY%5CPmNd16M8nyojuyCXoG7PDCNHrpBqicXqhWFTb19J73mQh%2F%2FKBqCgK%2FBqjOrfpxe8BavIt%5CyZC%2FW3C7z4bdUTNoz5YlMqocS%5CjI4g64etw7bmXeynSq%2BeQn2ykFbWnEX5Jcbn%3A1523068200266; JSESSIONID-WYYY=THlvDXIuX%2FOZQWvHArXZ%5CZuzVJeZP%2BanvjbZtaUOiOhAn8dx%5CGKsb86A%2B%2B%2BK90JmlkAVjMwua53t%5CMZAdJsp%5C%5CDSTjukNH5WiIUdiqk%2FbHNg4ryGXHFxUHqfoaFm%2BKZAIHBon%2B%2FEMsB3V6Be55PZ%2FnWyH6tGa7OvUtA%2BWhf%2BJDdqfmpc%3A1523279172933; __utma=94650624.913370056.1522327952.1523263260.1523277373.14; __remember_me=true; MUSIC_U=c5e4d9f1810e8c6350df923f848c2fc75053be85f4706fa62cbf3bf924296ae08425462745d48420ea15978500376ec9b9639ef2c859b2fdaf9e62a8590fd08a; __csrf=501f0edace04c46b2cef649de9267d83; __utmb=94650624.5.10.1523277373',
            '_iuqxldmzr_=32; _ntes_nnid=335cac0c45f3c4a2936fe11b8c3fa4fa,1522327951584; _ntes_nuid=335cac0c45f3c4a2936fe11b8c3fa4fa; __utmc=94650624; _ngd_tid=5h%2FgzWeXegeNP7Sh8iFAE4gH2FsYOEIW; c98xpt_=30; __utmz=94650624.1523022908.9.7.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); jsessionid-cpta=dIHB5nrm%2FF4%2FvXv%2FV96fRVAOSWeSVNp7qFqWOrhPNVY%5CPmNd16M8nyojuyCXoG7PDCNHrpBqicXqhWFTb19J73mQh%2F%2FKBqCgK%2FBqjOrfpxe8BavIt%5CyZC%2FW3C7z4bdUTNoz5YlMqocS%5CjI4g64etw7bmXeynSq%2BeQn2ykFbWnEX5Jcbn%3A1523068200266; JSESSIONID-WYYY=THlvDXIuX%2FOZQWvHArXZ%5CZuzVJeZP%2BanvjbZtaUOiOhAn8dx%5CGKsb86A%2B%2B%2BK90JmlkAVjMwua53t%5CMZAdJsp%5C%5CDSTjukNH5WiIUdiqk%2FbHNg4ryGXHFxUHqfoaFm%2BKZAIHBon%2B%2FEMsB3V6Be55PZ%2FnWyH6tGa7OvUtA%2BWhf%2BJDdqfmpc%3A1523279172933; __utma=94650624.913370056.1522327952.1523263260.1523277373.14; MUSIC_U=a30f98e438ea5a6ea1525a4b980a06613f236de481255cfbfbf6ec64162bf88df98a533c421ef62638f396a18ff6d6857b43f3d2e9ad3f5c8bafcdfe5ad2b092; __remember_me=true; __csrf=8c74705413eb91552fc41a03e64bcf22; __utmb=94650624.8.10.1523277373',
            '_iuqxldmzr_=32; _ntes_nnid=335cac0c45f3c4a2936fe11b8c3fa4fa,1522327951584; _ntes_nuid=335cac0c45f3c4a2936fe11b8c3fa4fa; __utmc=94650624; _ngd_tid=5h%2FgzWeXegeNP7Sh8iFAE4gH2FsYOEIW; c98xpt_=30; __utmz=94650624.1523022908.9.7.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); JSESSIONID-WYYY=THlvDXIuX%2FOZQWvHArXZ%5CZuzVJeZP%2BanvjbZtaUOiOhAn8dx%5CGKsb86A%2B%2B%2BK90JmlkAVjMwua53t%5CMZAdJsp%5C%5CDSTjukNH5WiIUdiqk%2FbHNg4ryGXHFxUHqfoaFm%2BKZAIHBon%2B%2FEMsB3V6Be55PZ%2FnWyH6tGa7OvUtA%2BWhf%2BJDdqfmpc%3A1523279172933; __utma=94650624.913370056.1522327952.1523263260.1523277373.14; MUSIC_U=71eb672d3ef77ccfa72f7eacdb36561299dcb9d14e06692f95ef4a9c73880ff474a709967c9e9688f680d4ee2ef5a860b3af0e6aecb05e55d881482c625a2ba0c3061cd18d77b7a0; __remember_me=true; __csrf=8f532b7c0be5d69627b82857ce559c3c; jsessionid-cpta=AvdbDtdOlDj4odEdGkM%2F5PlJdx%5CuAEI9hVldQu5ApjdrvbQBKtyAxY%5CNK2Iv7%5CoZC3HBo1xH9PAfXDJMLZc2eK5RxrtAWz6Snv%2BArOTn52PxJol%5Cou%2F%5CzoSvhWDJO7eoNMydSPREXOOV%2Bhy7R%2FbuKLlEaZHlV%5CmTmfOpGB%2B69vJ3Gaw6%3A1523278526000; NETEASE_WDA_UID=1424762937#|#1523277634477; __utmb=94650624.11.10.1523277373',
            'JSESSIONID-WYYY=9yC2qo%2BHK2DsBTFPTOsQcPBFwbo2jpDwP%2FQINIlnMRtMSfyWe%2Fsf5yaYva7%2FsOvoe3lO3OmH1BGZtDr8H%5Co0mF%2Fyfs7IeifEjr8r6U6RTRQQ%2F%5C%2FPHH5784BE%5CJKtEY3EzHrr4zi98zi5YHmJE%2B%2BfR%2B3c9l8qAJvjb1NDvqeVcUkoluA%2F%3A1523279558919; _iuqxldmzr_=32; _ntes_nnid=d391a7c1e00da9483ac5c33f6246c666,1523277758938; _ntes_nuid=d391a7c1e00da9483ac5c33f6246c666; __utma=94650624.1927432476.1523277759.1523277759.1523277759.1; __utmc=94650624; __utmz=94650624.1523277759.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _ngd_tid=SPC36qvBQ2E8%2FBpVLRFDn5dixs4wIgNu; __remember_me=true; jsessionid-cpta=AL7pql3NW3VB4RSrm8LY%5C1ISd9x5p72V2vIqtWrV1Al8uyFXeHSfrlKtq8cyZ82BldTdn0CmxnNZGv0Ra4Muz7k29GzdeWygacW9UEziHML9Lb4%2BpXik0y4aw%2FM5cCpnVT7hL9g7KPo2oWCSq46%5Cnvf%5C0cEzrrS9PiRD5bTiA7cX2a2U%3A1523278697522; c98xpt_=30; NETEASE_WDA_UID=1424757989#|#1523277823050; MUSIC_U=2ddcae69ee4c5d34f7cdaa0dc5d8ad5299dcb9d14e06692f68b356e2a828f22ea8b75bbf16269ceb6c713c89ab5a4cc3e0548fa671bde16c86e425b9057634fc; __csrf=6c2e50941180216bc5ef42179ece465c; __utmb=94650624.4.10.1523277759',
        ]
        self._comment_count = comment_count
        self._hotcomment = hotcomment
        self.cachefile = './workspace/' + cachefile
        self.header = {
            'Accept': "*/*",
            'Accept-Encoding': "gzip, deflate",
            'Accept-Language': "zh-CN,zh;q=0.8",
            'Connection': "keep-alive",
            'Content-Length': "416",
            'Content-Type': "application/x-www-form-urlencoded",
            'Cookie': "_ntes_nnid=61528ed156a887c721f86bb28fb76864,1498012702495; _ntes_nuid=61528ed156a887c721f86bb28fb76864; playerid=72107504; JSESSIONID-WYYY=CBWAZVhlvjI8K2BH6zzZ%2Fg7D3eSt8d%2FBbX7cS%2FugonhTD4v%5CEMovRW%2FMMKaSSHsbxNWkASNlyqAs0kkNffuzVgNTeYe74hbWl3pCJPmdH3C5qpONJgrwkH9PNx1o6MOzdTdNKpYzw7HJZhbXXwAJ%2Fup%2F57wI2qFQTsvNi1rzWEr9vJug%3A1498075419550; _iuqxldmzr_=32; __utma=94650624.1764604869.1498012703.1498069886.1498074715.8; __utmb=94650624.3.10.1498074715; __utmc=94650624; __utmz=94650624.1498074715.8.5.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; MUSIC_U=0a56e5572596ab32367822d83962fb422c20eaf414934908a7ce96b1372782ad5962f7c16f34c1c6a337c009e727897da70b41177f9edcea; __remember_me=true; __csrf=880488a01f19e0b9f25a81842477c87b",
            'Host': "music.163.com",
            'Origin': "http://music.163.com",
            'Referer': "http://music.163.com/",
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }

    def get_encSecKey(self):
        encSecKey = "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"
        return encSecKey

    def AES_encrypt(self, text, key, iv):
        pad = 16 - len(text) % 16
        text = text + pad * chr(pad)
        encryptor = AES.new(key, AES.MODE_CBC, iv)
        encrypt_text = encryptor.encrypt(text)
        encrypt_text = base64.b64encode(encrypt_text).decode('utf-8')
        return encrypt_text

    def get_params(self, page):
        iv = "0102030405060708"
        first_key = self.forth_param
        second_key = 16 * 'F'
        if page == 1:
            # offset的取值为:(评论页数-1)*20,total第一页为true，其余页为false
            # first_param = '{rid:"", offset:"0", total:"true", limit:"20", csrf_token:""}' # 第一个参数
            first_param = '{rid:"", offset:"0", total:"true", limit:"20", csrf_token:""}'
            h_encText = self.AES_encrypt(first_param, first_key, iv)
        else:
            offset = str((page - 1) * 20)
            first_param = '{rid:"", offset:"%s", total:"%s", limit:"20", csrf_token:""}' % (offset, 'false')
            h_encText = self.AES_encrypt(first_param, first_key, iv)
        h_encText = self.AES_encrypt(h_encText, second_key, iv)
        return h_encText

    def get_proxy(self):
        i = int((datetime.datetime.now() - self.start_time).seconds // self.time_t) % len(self.ips)
        return {'http': self.ips[i]}

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

    def get_all_comments(self, song_id):
        """
        获取歌曲评论信息
        :param song_id: (string) 歌曲id
        :return: None
        """
        song_id = song_id if isinstance(song_id, str) else str(song_id)
        all_comments_list = []  # 存放所有评论
        all_users_list = []  # 存放评论的用户信息
        url = 'https://music.163.com/weapi/v1/resource/comments/R_SO_4_' + song_id + '?csrf_token='
        total = 0
        i = 0
        pages = 1

        while i < pages:
            start = i * 20
            params = self.get_params(i + 1)
            encSecKey = self.get_encSecKey()
            i += 1
            param = {
                "params": params,
                "encSecKey": encSecKey
            }
            resp = requests.post(url, headers=self.header, data=param, proxies=self.get_proxy())
            data = resp.json()
            if 'msg' in data:
                self.cache(song_id, 'error')
                print('ip failed')
                exit()

            if pages == 1:
                comments_num = data['total']
                if comments_num % 20 == 0:
                    pages = comments_num / 20
                else:
                    pages = int(comments_num / 20) + 1
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
            #time.sleep(random.randint(12, 23) / 10)
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
    my = SongCommentProxy(message_music, message_data, 'cache1')
    my.run()

