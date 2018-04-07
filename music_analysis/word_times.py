import MySQLdb as mdb



def search_song(song_id):

    message = {
        'host': '127.0.0.1',
        'user': 'root',
        'passwd': ' ',
        'db': '163data',
        'charset': 'utf8mb4'  # 指定编码格式!!!
    }
    connection = mdb.connect(**message)

    with connection.cursor() as cursor:
        sql = 'SELECT * FROM 163data.api_comment where song_id='+song_id
        cursor.execute(sql)
    connection.commit()
    connection.close()

