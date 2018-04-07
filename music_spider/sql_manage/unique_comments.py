import MySQLdb as mdb


message = {
    'host': '10.40.37.170',
    'user': 'aitical',
    'passwd': 'wugang19980730',
    'db': '163music',
    'charset': 'utf8mb4'  # 指定编码格式!!!
}
connection = mdb.connect(**message)
c = connection.cursor()
sql = "SELECT song_id, content, comment_id, user_id, pub_time, liked_count FROM 163music.api_comment GROUP BY comment_id"
c.execute(sql)





data_config = {
    'host': '10.40.37.170',
    'user': 'aitical',
    'passwd': 'wugang19980730',
    'db': '163data',
    'charset': 'utf8mb4'  # 指定编码格式!!!
}
conn = mdb.connect(**message)
dd = conn.cursor()
data_sql = "INSERT INTO 163data.api_comment(song_id, content, comment_id, user_id, pub_time, liked_count) VALUES (%s, %s, %s, %s, %s, %s)"
dd.executemany(data_sql, c.fetchall())
conn.commit()
conn.close()
connection.close()



print("Jay")
message = {
    'host': '10.40.37.170',
    'user': 'aitical',
    'passwd': 'wugang19980730',
    'db': '163music',
    'charset': 'utf8mb4'  # 指定编码格式!!!
}
connection = mdb.connect(**message)
c2 = connection.cursor()
sql = "SELECT song_id, content, comment_id, user_id, pub_time, liked_count FROM Jay GROUP BY comment_id"
c2.execute(sql)





data_config = {
    'host': '10.40.37.170',
    'user': 'aitical',
    'passwd': 'wugang19980730',
    'db': '163data',
    'charset': 'utf8mb4'  # 指定编码格式!!!
}
conn = mdb.connect(**message)
dd = conn.cursor()
data_sql = "INSERT INTO 163data.api_comment(song_id, content, comment_id, user_id, pub_time, liked_count) VALUES (%s, %s, %s, %s, %s, %s)"
dd.executemany(data_sql, c2.fetchall())
conn.commit()
conn.close()
connection.close()





message = {
    'host': '10.40.37.170',
    'user': 'aitical',
    'passwd': 'wugang19980730',
    'db': '163data',
    'charset': 'utf8mb4'  # 指定编码格式!!!
}
connection = mdb.connect(**message)
c = connection.cursor()
sql = "SELECT song_id, content, comment_id, user_id, pub_time, liked_count FROM 163data.api_comment GROUP BY comment_id"
c.execute(sql)
connection.close()


data_config = {
    'host': '10.40.37.170',
    'user': 'aitical',
    'passwd': 'wugang19980730',
    'db': '163music',
    'charset': 'utf8mb4'  # 指定编码格式!!!
}
conn = mdb.connect(**message)
dd = conn.cursor()
data_sql = "INSERT INTO 163music.analysis_comment(song_id, content, comment_id, user_id, pub_time, liked_count) VALUES (%s, %s, %s, %s, %s, %s)"
dd.executemany(data_sql, c.fetchall())
conn.commit()
conn.close()
connection.close()