import json
from get_data import SongComment, UserDetail, UserPlaylist, Online
import threading
import sys
import time
import MySQLdb as mdb


def sql_status(config):
    connection = mdb.connect(**config)
    with connection.cursor() as c:
        sql = "SELECT COUNT(*) FROM api_comment"
        c.execute(sql)
        data = c.fetchall()[0][0]
    return data


def SongCommentStatus(filepath):
    with open(filepath + 'l_song_id.txt') as fin:
        line = fin.readlines()[-1].split('\t')
        status_song = line[-2]
    if 'error' == status_song:
        return True
    return False


if __name__ == '__main__':

    args = sys.argv
    command = args[1]
    oj = ''
    if len(args) > 2:
        oj = args[2]

    with open('config.json') as f:
        data = json.load(f)

    DB = data['DB']
    ONLINE = data['ONLINE']
    username = ONLINE['username']
    password = ONLINE['password']
    timeiterval = ONLINE['sleep']
    message_music = DB['message_music']
    message_data = DB['message_data']
    cachefile = data['CACHE_FILE']
    filepath = './workspace/' + cachefile + '/'

    if 'h' == command:
        print("""
        启动参数简述:
        run.py <command> -[method]
        
        command:
        run: 正常启动项目
        status: 查看数据库状态
        fix: 手动启动评论抓取
        test: 运行测试中的功能
        
        method:
        -o: 校园网网络检测断网重连
        """)

    if 'fix' == command:
        song_comment = SongComment.SongComment(music=message_music, data=message_data, cachefile=cachefile)
        threading.Thread(target=song_comment.run).start()

    if 'test' == command:
        from get_data.test import SongCommentProxy

        song_comment_proxy = SongCommentProxy.SongCommentProxy(music=message_music, data=message_data,
                                                               cachefile=cachefile)
        song_comment_proxy.run()

    if 'run' == command:
        """
        启动爬虫
        """
        if '-o' == oj:
            # 启动断网重连
            print('启用断网重连...')
            online = Online.Online(username, password, timeiterval)
            threading.Thread(target=online.run).start()
            time.sleep(1)

        song_comment = SongComment.SongComment(music=message_music, data=message_data, cachefile=cachefile)
        user_detail = UserDetail.UserDetail(message_music, message_data, cachefile=cachefile)
        user_playlist = UserPlaylist.UserPlaylist(message_music, message_data, cachefile=cachefile)

        print('准备启动中...')
        song = threading.Thread(target=song_comment.run)
        threading.Thread(target=user_playlist.run).start()
        threading.Thread(target=user_detail.run).start()
        song.start()
        print('启动完成')

        count = 0
        while True:
            if count < 1:
                count += 1
                time.sleep(60 * 120)
                continue
            time.sleep(60 * 120)
            song_comment_status = SongCommentStatus(filepath)
            if song_comment_status:
                count += 1
                threading.Thread(target=song_comment.run).start()

    if 'status' == command:
        """
        简单查看当前运行状态
        """
        with open(filepath + 'l_user_id.txt') as fin:
            line = fin.readlines()[-1].split('\t')
            status = line[-2]
            last_running_time = line[-1]
            print('UserDetail: \nstatus:', status, '\nlast_running_time:', last_running_time)

        with open(filepath + 'l_user_id_p.txt') as fin:
            line = fin.readlines()[-1].split('\t')
            status_user = line[-2]
            last_running_time_user = line[-1]
            print('UserPlaylist: \nstatus:', status_user, '\nlast_running_time:', last_running_time_user)

        with open(filepath + 'l_song_id.txt') as fin:
            line = fin.readlines()[-1].split('\t')
            status_song = line[-2]
            last_running_time_song = line[-1]
            print('SongComment: \nstatus:', status_song, '\nlast_running_time:', last_running_time_song)
        
        if '-db' == oj:
            # 查看数据库情况
            dat = sql_status(message_music)
            print('SongComment:', dat)