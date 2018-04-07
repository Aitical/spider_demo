import pandas
import MySQLdb as mdb
import os


message = {
    'host': '127.0.0.1',
    'user': 'root',
    'passwd': ' ',
    'db': '163music',
    'charset': 'utf8mb4'  # 指定编码格式!!!
}
connection = mdb.connect(**message)
c = connection.cursor()
sql = "INSERT INTO api_songs(song_name, song_id) VALUES(%s, %s)"

filepath = '/home/aitical/Documents/163mc_spider/Songs'
files = os.listdir(filepath)
aim_data = []
for file in files:
    print(file)
    data = pandas.read_csv(filepath+'/'+file)
    aim_data.extend(list(zip(data.name, data.id)))
aim_data = list(set(aim_data))
c.executemany(sql, aim_data)
connection.commit()
connection.close()
