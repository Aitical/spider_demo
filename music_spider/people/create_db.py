# -*- coding: utf-8 -*- 
# @Time : 18-5-20 下午8:30 
# @Author : Aries 
# @File : create_db.py 
# @Software: PyCharm

from peewee import *

# 数据库的配置文件
# 注意端口号是用数字
config = {
    'database': 'people',
    'user': '#',
    'password': '#',
    'host': '#',
    'port': 3306,
    'charset': 'utf8'
}

# 创建数据库实体
mysql_db = MySQLDatabase(**config)


class Search(Model):
    """
    创建Search表,存储搜索结果信息
    """
    title = CharField(max_length=200, default='#$%^')
    summary = TextField()
    href = CharField(max_length=200, default='#$%^')
    pub_time = DateTimeField()

    class Meta:
        database = mysql_db


class News(Model):
    """
    创建新闻内容表
    """
    title = CharField(max_length=200, default='#$%^')
    keywords = TextField()
    summary = TextField()
    content = TextField()
    pub_time = CharField(max_length=20, default='#$%^')
    editor = CharField(max_length=200, default='#$%^')

    class Meta:
        database = mysql_db


if __name__ == '__main__':

    mysql_db.connect()
    mysql_db.create_tables([News])
    mysql_db.commit()
    mysql_db.close()