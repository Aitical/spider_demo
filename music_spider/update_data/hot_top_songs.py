import requests
import re
import MySQLdb as mdb
from bs4 import BeautifulSoup
import time


def save_top_songs(data):

    message = {
        'host': '127.0.0.1',
        'user': 'root',
        'passwd': ' ',
        'db': '163music',
        'charset': 'utf8mb4'  # 指定编码格式!!!
    }
    conn = mdb.connect(**message)
    dd = conn.cursor()
    sql = "INSERT INTO 163music.api_songs(song_name, song_id) VALUES (%s, %s)"
    dd.executemany(sql, data)
    dd.close()
    conn.commit()
    conn.close()
    print(len(data))


def update_top_songs():
    songs = []
    page_ids = ['19723756', '3779629', '2884035', '3778678']
    for page_id in page_ids:
        url = 'https://music.163.com/discover/toplist?id='+page_id

        header = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
        }

        resp = requests.get(url, headers=header).text

        href_content = re.compile('/song\?id=([0-9]+)')

        soup = BeautifulSoup(resp, 'lxml')
        all_a = soup.find_all('a', attrs={'href': href_content})

        for item in all_a:
            songs.append((
                item['href'][9:],
                item.text
            ))
        time.sleep(3)

    save_top_songs(songs)

def main():
    update_top_songs()

if __name__ == '__main__':
    main()