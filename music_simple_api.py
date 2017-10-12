from selenium import webdriver
from bs4 import BeautifulSoup
import selenium.webdriver.support.ui as ui
import requests
import json
import threading
import re
import os

count = 0

preurl = 'http://music.163.com'

headers = {
	'Accept': '*/*',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'music.163.com',
    'Referer': 'http://music.163.com/search/',
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
}
cookies = {'appver':'1.5.2'}



# #准确搜索歌手,返回id的字符串
# def search_artist(name,type = 100):
#     '''
#
#     :param name:歌手姓名(准确搜索)
#     :return: 对应的歌手id(str)
#     '''
#     url = 'http://music.163.com/api/search/get'
#     data = {
#         's': name,
#         'type': type,
#         'offset': 0,
#         'total': 'true',
#         'limit': 60
#     }
#     rr = requests.post(url, data=data)
#     rr = json.loads(rr.text)
#     return rr['result']['artists'][0]['id']

#准确搜索



#通用搜索,返回歌曲和歌手信息
def search(name,type = 1):
    '''

    :param name:歌手/专辑/单曲
    :return:[{'song_name':'','artist':'','artist_id':'','song_id':''},...]
    '''
    url = 'http://music.163.com/api/search/get'
    data = {
        's': name,
        'type': type,
        'offset': 0,
        'total': 'true',
        'limit': 60
    }
    rr = requests.post(url, data=data)
    rr = json.loads(rr.text)
    result = []
    for j in rr['result']['songs']:
        song_name = j['name']
        #过滤歌曲名多余信息
        if(' - Album Version' in song_name):
            song_name = song_name[:-15]
        ##
        tmp = {'song_name':song_name,'artist':j['artists'][0]['name'],'artist_id':j['artists'][0]['id'],'song_id':j['id']}
        result.append(tmp)
    return result


# #通过歌手id获取歌手的热门单曲前50
# def get_artist_songs(artists_id):
#     '''
#
#     :param artists_id:歌手id
#     :return: 前50的热门单曲->结构[(song_id(str),song_title),...]
#     '''
#     driver = webdriver.PhantomJS(executable_path='/usr/bin/phantomjs')
#     url = 'https://music.163.com/m/artist?id={}'.format(artists_id)
#     driver.get(url)
#     driver.switch_to_frame('g_iframe')
#     wait = ui.WebDriverWait(driver, 15)#####
#     # 等待元素渲染出来
#     soup = BeautifulSoup(driver.page_source, 'lxml')
#
#     all_a = soup.find_all('a')
#     songs = []
#     for i in all_a:
#         if (i.b):
#             songs.append((i['href'][9:], i.b['title']))
#     return songs
#woc啊,垃圾博客推荐的爬取动态网页，还tm要等待渲染，老哥，url都找不准，还爬取个毛线？？？？
#已更新如下

#通过歌手id获取歌手的热门单曲前50
def get_artist_songs(artists_id):
    '''
    通过歌手id获取歌手的热门单曲前50
    :param artists_id: 歌手id=>数字字符串
    :return: 前50的单曲信息->结构[[song_id(str),song_title],...]
    '''
    url = 'https://music.163.com/artist?id={}'.format(artists_id)
    tmp_r = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(tmp_r.text, 'lxml')
    song_id = re.compile('/song\?id=[0-9]+')
    songs_list = [[songId['href'][9:], songId.text] for songId in soup.find_all('a', attrs={'href': song_id})]
    return songs_list

#处理歌词
def strip_songMessage(rawString):
    '''
    处理歌词
    :param rawString: get到的原生的歌词形式字符串
    :return: 处理后的歌词->已用回车链接,最后一句没有回车
    '''
    tmp_lst = re.split('\[.+\]', rawString)
    final_c = []
    for i in tmp_lst:
        if (i):
            final_i = i.strip()
            if (i.strip()):
                final_c.append(final_i)
    return '\n'.join(final_c)



#歌词&评论获取

def get_commentContent(song_message):
    '''

    :param song_message: [(song_id(str),song_title),...]
    :return: 生成{song_title}.txt & {song_title}_hotComment.txt （& 歌词汇总和评论汇总文件临时用于分析）
    '''
    song_id = song_message[0]
    song_title = song_message[1]

    #初始化文件路径
    if (os.path.isdir('./歌词') and os.path.isdir('./评论')):
        pass
    else:
        if (not os.path.isdir('./歌词')):
            os.mkdir('./歌词')
        if (not os.path.isdir('./评论')):
            os.mkdir('./评论')

    #获取热评
    url_comment = 'http://music.163.com/api/v1/resource/comments/R_SO_4_{}'.format(song_id)

    if(os.path.isfile('评论/'+song_message[1]+ '_hotcomment.txt')):
        print(song_message[1] + '\t信息已获取')
        return
    else:
        try:
            f_comment = open('评论/'+song_message[1] + '_hotcomment.txt', 'a')
            f_comment_total = open('commentTotal.txt', 'a')
        except:
            return
        r = requests.get(url_comment, headers=headers, cookies=cookies)
        r_json = json.loads(r.text)
        f_comment_total.write(song_title + '\n\n')
        for i in r_json['hotComments']:
            f_comment.write(i['content'] + '\n\n')
            f_comment_total.write(i['content'] + '\n\n')
        f_comment.close()
        f_comment_total.close()



        # 歌词信息
        url_cc = 'http://music.163.com/api/song/lyric?os=pc&id={}&lv=-1&kv=-1&tv=-1'.format(song_id)
        r_cc = requests.get(url_cc, headers=headers, cookies=cookies)
        json_t = json.loads(r_cc.text)
        if('nolyric' in json_t.keys() or 'uncollected' in json_t.keys()):
            print('无歌词信息')
        else:
            if(json_t['lrc']['version']!=0):
                f_title = open('歌词/' + song_title + '.txt', 'w')
                f_title_total = open('songTotal.txt', 'a')
                final_cc = strip_songMessage(json_t['lrc']['lyric'])
                f_title.write(final_cc)
                f_title_total.write(final_cc + '\n')
                f_title.close()
                f_title_total.close()
                print(song_message[1], 'succeeded!')
            else:
                print('无歌词信息')

#2017-10-03
#获取当前页所有的歌单
def get_palylist(page_id):
    '''
    获取当前页所有的歌单
    :param page_id:指定页数的歌单
    :return: 该页含有的所有歌单的id=>每页含有35个,已处理成直接访问歌曲内容的url
    '''
    url = 'https://music.163.com/discover/playlist/?order=hot&cat=%E5%85%A8%E9%83%A8&limit=35&offset={}'.format(page_id)
    tmp_r = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(tmp_r.text, 'lxml')
    playIdLst = [preurl + songid['href'] for songid in soup.find_all('a', attrs={'class': 'msk'}) if songid['href']]
    return playIdLst

#获取指定歌单的所有歌曲id
def get_songs_inplaylist(url):
    '''
    获取指定歌单的所有歌曲id
    :param url: 歌单的url=>注意不要直接复制浏览器的url,去掉中间的‘#/‘
    :return: 歌单含有的歌曲的id=>[id1,...]
    '''
    tmp_r = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(tmp_r.text,'lxml')
    song_id = re.compile('/song\?id=[0-9]+')
    song_messages = [[songId['href'][9:],songId.text] for songId in soup.find_all('a',attrs={'href':song_id})]
    return song_messages

def main_child(play):
    song_messages = get_songs_inplaylist(play)
    for songMessage in song_messages:
        get_commentContent(songMessage)

def  main(playLst):
    for play in playLst:
        threading.Thread(target = main_child,args = play)



if(__name__ == '__main__'):
    #获取周杰伦前50热门评论
    data = search('周杰伦')[0]
    songsLst = get_artist_songs(data['artist_id'])
    for songMessage in songsLst:
        get_commentContent(songMessage)