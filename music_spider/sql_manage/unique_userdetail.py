import pandas
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
sql = "SELECT user_id, user_name, level, event_count, follow_count, fan_count, loc_city, age, self_desc, loc_province  FROM 163music.api_userdetail WHERE user_name != '0'"
c.execute(sql)





message = {
    'host': '127.0.0.1',
    'user': 'root',
    'passwd': ' ',
    'db': '163data',
    'charset': 'utf8mb4'  # 指定编码格式!!!
}
conn = mdb.connect(**message)
dd = conn.cursor()
data_sql = "INSERT INTO 163data.api_userdetail(user_id, user_name, level, event_count, follow_count, fan_count, loc_city, age, self_desc, loc_province)    VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s, %s)"
dd.executemany(data_sql, c.fetchall())
conn.commit()
conn.close()
connection.close()

