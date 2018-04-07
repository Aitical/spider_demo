import json
from get_data import SongComment, UserDetail, UserPlaylist
import threading


with open('config.json') as f:
    data = json.load(f)

DB = data['DB']
message_music = DB['message_music']
message_data = DB['message_data']
cachefile = data['CACHE_FILE']

song_comment = SongComment.SongComment(music=message_music, data=message_data, cachefile=cachefile)
user_detail = UserDetail.UserDetail(message_music, message_data, cachefile=cachefile)
user_playlist = UserPlaylist.UserPlaylist(message_music, message_data, cachefile=cachefile)


print('准备启动中...')

threading.Thread(target=song_comment.run).start()
threading.Thread(target=user_playlist.run).start()
threading.Thread(target=user_detail.run).start()
print('启动完成')