from django.db import models

class Playlist(models.Model):
    playlist_id = models.CharField(max_length=100)
    name = models.CharField(max_length=200)

class Songs(models.Model):
    song_name = models.CharField(max_length=300, default='&&')
    song_id = models.CharField(max_length=100)

class Comment(models.Model):
    song_id = models.CharField(max_length=100)
    content = models.TextField()
    comment_id = models.CharField(max_length=100)
    user_id = models.CharField(max_length=100)
    pub_time = models.DateTimeField()
    liked_count = models.IntegerField(default=0)

class User(models.Model):
    user_id = models.CharField(max_length=100)
    pic = models.CharField(max_length=200)
    name = models.CharField(max_length=200)

class CommentCount(models.Model):
    song_id = models.CharField(max_length=100)
    total = models.IntegerField()
    state = models.IntegerField(default=0)

class HotComment(models.Model):
    song_id = models.CharField(max_length=100)
    content = models.TextField()
    comment_id = models.CharField(max_length=100)
    user_id = models.CharField(max_length=100)
    pub_time = models.DateTimeField()
    liked_count = models.IntegerField(default=0)

class UniqueComment(models.Model):
    song_id = models.CharField(max_length=100)
    content = models.TextField()
    comment_id = models.CharField(max_length=100)
    user_id = models.CharField(max_length=100)
    pub_time = models.DateTimeField()
    liked_count = models.IntegerField(default=0)

class UserDetail(models.Model):
    user_id = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100, null=True)
    level = models.IntegerField(default=0)
    sex = models.IntegerField(default=0)
    event_count = models.IntegerField(default=0)
    follow_count = models.IntegerField(default=0)
    fan_count = models.IntegerField(default=0)
    loc_province = models.CharField(max_length=100, null=True)
    loc_city = models.CharField(max_length=100, null=True)
    age = models.CharField(max_length=20, null=True, default='#')
    self_desc = models.TextField(null=True)

class Proxy(models.Model):
    proxy_id = models.CharField(max_length=100, default='0')
    ip = models.CharField(max_length=100, default='0.0.0.0')
    port = models.CharField(max_length=10, default='80')
    ip_position = models.CharField(max_length=100, null=True)
    responseTime = models.IntegerField(default=0)
    createTime = models.DateTimeField()
    updateTime = models.DateTimeField()

class Mogu_Proxy(models.Model):
    ip = models.CharField(max_length=100, default='0.0.0.0')
    port = models.CharField(max_length=10, default='80')
    status = models.IntegerField(default=1)
    ping = models.IntegerField(default=0)

class PlaylistMessage(models.Model):
    playlist_id = models.CharField(max_length=100, default='0')
    coverImgUrl = models.CharField(max_length=100, default='http://')
    createTime = models.CharField(max_length=100, default='0')
    creator = models.CharField(max_length=100, default='0')
    description = models.TextField(default='', null=True)
    name = models.CharField(max_length=200)
    playCount = models.IntegerField(default=0)
    subscribedCount = models.IntegerField(default=0)
    tags = models.CharField(max_length=200, null=True)
    trackCount = models.IntegerField(default=0)

class Creator(models.Model):
    user_id = models.CharField(max_length=100, default='0')
    authStatus = models.IntegerField(default=0)
    avatarUrl = models.CharField(max_length=200, default='http://', null=True)
    backgroundUrl = models.CharField(max_length=200, default='http://', null=True)
    birthday = models.CharField(max_length=100, default='0', null=True)
    province = models.IntegerField(null=True)
    city = models.IntegerField(null=True)
    description = models.TextField(null=True)
    detailDescription = models.TextField(null=True)
    expertTags = models.CharField(max_length=200, default='', null=True)
    gender = models.IntegerField()
    nickname = models.CharField(max_length=100, default='')
    signature = models.TextField(null=True)

class User_Playlist(models.Model):
    user_id = models.CharField(max_length=100)
    playlist_id = models.CharField(max_length=100)

