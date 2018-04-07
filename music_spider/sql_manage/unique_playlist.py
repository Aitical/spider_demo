import MySQLdb as mdb


message = {
    'host': '127.0.0.1',
    'user': 'root',
    'passwd': ' ',
    'db': '163music',
    'charset': 'utf8mb4'  # 指定编码格式!!!
}
connection = mdb.connect(**message)
c = connection.cursor()
sql = "SELECT playlist_id, name FROM 163music.api_playlistmessage GROUP BY playlist_id"
c.execute(sql)

data_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'passwd': ' ',
    'db': '163music',
    'charset': 'utf8mb4'  # 指定编码格式!!!
}
conn = mdb.connect(**message)
dd = conn.cursor()
data_sql = "INSERT INTO 163music.api_playlist(playlist_id, name) VALUES (%s, %s)"
dd.executemany(data_sql, c.fetchall())
conn.commit()
conn.close()
connection.close()
