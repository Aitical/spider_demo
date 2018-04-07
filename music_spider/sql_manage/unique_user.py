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
sql = "SELECT user_id,pic,name FROM 163music.api_user GROUP BY user_id"
c.execute(sql)

data_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'passwd': ' ',
    'db': '163data',
    'charset': 'utf8mb4'  # 指定编码格式!!!
}
conn = mdb.connect(**message)
dd = conn.cursor()
data_sql = "INSERT INTO 163data.api_user(user_id, pic, name) VALUES (%s, %s, %s)"
dd.executemany(data_sql, c.fetchall())
conn.commit()
conn.close()
connection.close()


message = {
    'host': '127.0.0.1',
    'user': 'root',
    'passwd': ' ',
    'db': '163data',
    'charset': 'utf8mb4'  # 指定编码格式!!!
}
connection = mdb.connect(**message)
c = connection.cursor()
sql = "SELECT user_id,pic,name FROM 163data.api_user GROUP BY user_id"
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
data_sql = "INSERT INTO 163music.analysis_user(user_id, pic, name) VALUES (%s, %s, %s)"
dd.executemany(data_sql, c.fetchall())
conn.commit()
conn.close()
connection.close()