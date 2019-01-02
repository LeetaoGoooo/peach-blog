# Peach-Blog

![](https://img.shields.io/badge/python-3.5%20%2F%203.6-green.svg) ![](https://img.shields.io/badge/flask-1.0.2-yellow.svg) [![Build Status](https://travis-ci.org/lt94/peach-blog.svg?branch=master)](https://travis-ci.org/lt94/peach-blog)

> Peach Blog 是基于 Flask 的博客平台，目的是为了提供一种更加纯粹的内容写作与发布平台,通过几个简单命令,可以帮助用户无痛的从 Hexo 切换到 Peach Blog

# Features

1. support export hexo's posts into database
2. support export database's posts into hexo-format markdown file 
3. add new dashboard base on flask-admin
4. add markdown support to flask-admin

# Screenshots

![](http://ww1.sinaimg.cn/large/006wYWbGly1fxmgbfy4ynj311o0pamzu.jpg)

![](http://ww1.sinaimg.cn/large/006wYWbGly1fxmgahexh9j31jy1h7grc.jpg)

![](http://ww1.sinaimg.cn/large/006wYWbGly1fxpv6inei2j31lu17pn4w.jpg)

# Usages

## environment

```
pip install -r requirements.txt
```

## init database

before you execute following lines,make sure you have already create database

```
flask shell
```

you'are supposed to see, something like follow one:

```bash
Python 3.6.5
App: app [development]
Instance: path\to\instance
```

then

```
>>> from app import db
>>> db.create_all()
# create super user
>>> from app.models import User
>>> user = User(user_name='your name',password='your password', level=1)
>>> db.session.add(user)
>>> db.session.commit()
```

## export hexo's posts into database

if you want to export hexo posts into database, change the value of **config.py** on line **14** (where the hexo's posts store),then

```
flask hexo g 
```

clean the posts,just use **flask hexo c** simplely

## create log dir

```
mkdir logs
```

## run the server

```
flask run
```

## export database's posts into hexo-format markdown files

login in peach-blog admin, and step into post list pages, and then (see the picture)

![](http://ww1.sinaimg.cn/large/006wYWbGly1fxmo7x0lgjj31uq0bujsg.jpg)

the expoted post will generate under the directory where you set in **config.py**

# About Dev

欢迎关注知乎专栏:[学Python的桃子](https://zhuanlan.zhihu.com/peach-python), 后续将逐步讲解整个开发过程.