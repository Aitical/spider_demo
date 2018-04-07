# import MySQLdb as mdb
#
# import json
#
#
# with open('config.json') as f:
#     data = json.load(f)
# DB = data['DB']
# message_music = DB['message_music']
# message_data = DB['message_data']
#
# connection = mdb.connect(**message_data)
# with connection.cursor() as c:
#     sql = "SELECT DISTINCT user_id FROM 163data.api_userdetail"
#     c.execute(sql)
#     songs = c.fetchall()
# data = '\n'.join([i[0] for i in songs])
# with open('c_user_id.txt', 'w') as f:
#     f.write(data)

import numpy as np

with open('c_user_id.txt') as fin:
    cache = [i.strip() for i in fin.readlines()]
with open('user_detail.txt') as fin:
    all = [i.strip() for i in fin.readlines()]

next = np.setdiff1d(all, cache, assume_unique=True)
with open('all_user.txt', 'w') as fin:
    fin.write('\n'.join(next))