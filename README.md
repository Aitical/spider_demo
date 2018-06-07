# 我眼中的网易云音乐

### 项目说明:

```
├── 163_spider
│   ├── README.md
│   ├── music_analysis
│   ├── music_api
│   ├── music_spider
│   └── log.md
```

项目共分为三大部分`spider`,`analysis`和`api`

#### music_spider

爬虫部分,在后台运行进行数据的抓取

采用的是`requests`+`mysql`进行数据获取和存储

#### music_analysis

数据分析部分,独立进行数据分析与处理

单独存储分析后的数据

#### music_api

web框架采用`Django2.0`,前端样式采用开源项目`Gentella`

处理`music_analysis`中的数据

更多项目说明请看后面详细信息

### 使用方法:

```shell
git clone https://github.com/Aitical/163_spider
cd 163_spider/music_spider
cp config_block.json config.json
```
配置`config.json`信息:

`DB`为存储数据库信息,

`CACHE_FILE`为运行目录(推荐`cache2`或`chahe3`)

配置完成后

启动爬虫:

```shell
python3 run.py run
```

查看运行状态:

```shell
python3 run.py status
```

查看全部命令

```shell
python3 run.py h
```

测试功能

```shell
python3 run.py test
```

注: 

test启动的功能是在开发中的测试功能,不一定可以运行,正常执行请使用run,当然也很感谢你参与test中功能的开发

前端部分采用`Django`混合开发(有待完成)

在`music_api`目录下执行

```shell
python3 manage.py runserver
```

即可看到网站效果(未完成)

### 几点说明:

项目测试环境为`Ubuntu16.04/Windows10`

项目涉及前后端,请先安装好相关依赖库

```
Django
request
BeautifulSoup
numpy
mysqlclinet
```

推荐使用`Anaconda3`的`python3.6`集成环境

注意在`Ubuntu16.04`中安装`mysqlclient`提示报错时请先安装相关系统依赖

```shell
sudo apt install libmysqlclient-dev
```

如果只使用爬虫脚本,则只需要配置好数据库后运行`music_spider`模块

### 详细说明

在爬虫模块增加了人民网文章爬虫

#### music_spider

```
.
├── config_block.json // 默认配置文件模板
├── config.json // 本机运行的配置文件信息
├── get_data  // 爬虫的代码实现部分
├── __init__.py
│   ├── test
│   │	├── Jay.py  // 抓取周董的歌曲信息(有待完成,待添加)
│   │	├── SongCommentProxy.py  // 使用代理(已完成)
│   │	├── PlayListDetail.py  // 抓取歌单详细信息(有待完成, 待添加)
│   ├── SongComment.py  // 抓取歌曲评论
│   ├── UserDetail.py  // 抓取用户基本信息
│   ├── UserPlaylist.py  // 抓取用户歌单
│   ├── Online.py  // 校园网连接检测断网重连
├── run.py	// 运行入口
├── people  // 人民网文章爬虫
│   ├── 1_news_log.txt  // 运行日志文件
│   ├── 1_running_log.txt
│   ├── 2_running_log.txt
│   ├── 3_news_log.txt
│   ├── 4_running_log.txt
│   ├── config_block.json  // 人民网爬虫配置文件模板
│   ├── config.json  // 爬虫配置文件
│   ├── create_db.py  // 数据库模型
│   ├── news.py  // 采集新闻内容
│   └── people.py   // 采集新闻url
├── sql_manage // 进行数据清洗部分(有待系统完成)
├── test  // 一些本地测试和待添加的功能(有待系统完成)
├── update_songs // 进行更新内容(有待系统完成)
└── workspace  // 爬虫运行所需的id相关信息和运行日志的存放区
    ├── cache1  // 每个区有三个部分
    │   ├── a_song_id.txt  // 所有待爬取的歌曲id信息
    │   ├── a_user_id_p.txt  // 所有待爬取的用户id信息(UserDetail)
    │   ├── a_user_id.txt  // 所有待爬取的用户id信息(UserPlaylist)
    │   ├── c_song_id.txt  // 已经爬去完成的歌曲id信息
    │   ├── c_user_id_p.txt  // 已经爬去完成的用户id信息(UserDetail)
    │   ├── c_user_id.txt  // 已经爬去完成的用户id信息(UserPlaylist)
    │   ├── l_song_id.txt  // 运行时的日志信息
    │   ├── l_user_id_p.txt
    │   └── l_user_id.txt
    ├── cache2
    ├── cache3
    └── cache4
```

#### music_api

采用的是`Django`框架,了解`Django`即可

```
.
├── analysis // 用于接受前端获取的数据分析请求(有待完成)
├── api  // 用于对数据进行api封装(有待完成)
├── front  // 用于前后端混合开发分析后的数据可视化(有待完成)
├── manage.py
├── music_api
└── templates  
```

#### music_analysis

对原始数据进行清晰和分析

分析部分自定义任意角度都可以

