from selenium import webdriver
from bs4 import BeautifulSoup
import selenium.webdriver.support.ui as ui
import requests
import json
import threading
import re

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


#准确搜索歌手,返回id的字符串
def search_artist(name):
    '''

    :param name:歌手姓名(准确搜索)
    :return: 对应的歌手id(str)
    '''
    url = 'http://music.163.com/api/search/get'
    data = {
        's': name,
        'type': 100,
        'offset': 0,
        'total': 'true',
        'limit': 60
    }
    rr = requests.post(url, data=data)
    rr = json.loads(rr.text)
    return rr['result']['artists'][0]['id']


#获取歌手的热门单曲前50

def get_artist_songs(aitists_id):
    '''

    :param aitists_id:歌手id
    :return: 前50的热门单曲->结构[(song_id(str),song_title),...]
    '''
    driver = webdriver.PhantomJS(executable_path='/usr/bin/phantomjs')
    url = 'https://music.163.com/m/artist?id={}'.format(aitists_id)
    driver.get(url)
    driver.switch_to_frame('g_iframe')
    wait = ui.WebDriverWait(driver, 15)#####
    # 等待元素渲染出来
    soup = BeautifulSoup(driver.page_source, 'lxml')

    all_a = soup.find_all('a')
    songs = []
    for i in all_a:
        if (i.b):
            songs.append((i['href'][9:], i.b['title']))
    return songs

def strip_songMessage(rawString):
    '''

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

    #获取热评
    url_comment = 'http://music.163.com/api/v1/resource/comments/R_SO_4_{}'.format(song_id)
    f_comment = open(song_message[1]+ '_hotcomment.txt', 'a')
    f_comment_total = open('commentTotal.txt','a')
    r = requests.get(url_comment, headers=headers, cookies=cookies)
    r_json = json.loads(r.text)
    f_comment_total.write(song_title+'\n\n')
    for i in r_json['hotComments']:
        f_comment.write(i['content'] + '\n\n')
        f_comment_total.write(i['content']+'\n\n')
    f_comment.close()
    f_comment_total.close()

    #歌词信息
    url_cc = 'http://music.163.com/api/song/lyric?os=pc&id={}&lv=-1&kv=-1&tv=-1'.format(song_id)
    r_cc = requests.get(url_cc,headers=headers, cookies=cookies)
    json_t = json.loads(r_cc.text)
    f_title = open(song_title+'.txt','w')
    f_title_total = open('songTotal.txt','a')
    final_cc = strip_songMessage(json_t['lrc']['lyric'])
    f_title.write(final_cc)
    f_title_total.write(final_cc+'\n')
    f_title.close()
    f_title_total.close()
    print(song_message[1],'succeeded!')

if(__name__ == '__main__'):

    artist_id = search_artist('周杰伦')
    songs_lst = get_artist_songs(artist_id)
    for i in songs_lst:
        get_commentContent(i)