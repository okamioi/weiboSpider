# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 20:59:53 2017

@author: Administrator
"""

import requests
import json
import time
import random
import pymysql.cursors
import csv

header = ['followingId','followingName','followingUrl','followersCount','followCount']
def crawlDetailPage(url,page):
    #读取微博网页的JSON信息
    headers = {
    'authority': 'weibo.com',
    'x-requested-with': 'XMLHttpRequest',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'content-type': 'application/x-www-form-urlencoded',
    'accept': '*/*',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://weibo.com/1192329374/KnnG78Yf3?filter=hot&root_comment_id=0&type=comment',
    'accept-language': 'zh-CN,zh;q=0.9,en-CN;q=0.8,en;q=0.7,es-MX;q=0.6,es;q=0.5',
    'cookie': ''
    }   
    req = requests.get(url,headers=headers)
    
    jsondata = req.text
    data = json.loads(jsondata)

    #获取每一条页的数据
    content = data['data']
    if content:
        # if content['cards']:
        #     content = content['cards']
        if content.get('cards'):
            content=content['cards']
    # print(content)

    #循环输出每一页的关注者各项信息
            for i in content:
                followingId = i['user']['id']
                followingName = i['user']['screen_name']
                followingUrl = i['user']['profile_url']
                followersCount = i['user']['followers_count']
                followCount = i['user']['follow_count']

                print("---------------------------------")
                print("用户ID为:{}".format(followingId))
                print("用户昵称为:{}".format(followingName))
                print("用户详情链接为:{}".format(followingUrl))
                print("用户粉丝数:{}".format(followersCount))
                print("用户关注数:{}".format(followCount))
                
                '''
                csv
                '''
                follow_list=[
                {'followingId':followingId,
                'followingName': followingName,
                'followingUrl': followingUrl,
                'followersCount': followersCount,
                'followCount': followCount
                }
                ]
                header = ['followingId','followingName','followingUrl','followersCount','followCount']
                with open('followlist.csv', 'a', newline='',encoding='utf-8') as f:
                    writer = csv.DictWriter(f,fieldnames=header) # 提前预览列名，当下面代码写入数据时，会将其一一对应。
                    # writer.writeheader()  # 写入列名
                    writer.writerows(follow_list)
            



        '''
        数据库操作
        '''

        # #获取数据库链接
        # connection  = pymysql.connect(host = 'localhost',
        #                           user = '',
        #                           password = '',
        #                           db = '',
        #                           charset = 'utf8mb4')
        # try:
        #     #获取会话指针
        #     with connection.cursor() as cursor:
        #         #创建sql语句
        #         sql = "insert into `following` (`followingId`,`followingName`,`followingUrl`,`followersCount`,`followCount`) values (%s,%s,%s,%s,%s)"

        #         #执行sql语句
        #         cursor.execute(sql,(followingId,followingName,followingUrl,followersCount,followCount))

        #         #提交数据库
        #         connection.commit()
        # finally:
        #     connection.close()
uids= ['7487619146','5831481714','5396590503','5926660141','5837469270','2029906001','1779654914','6791517858','5746403289','6049590367',
          '1992246393','1588741002','1787697542','3937348351','5463794433','2309846073','3205933003','5898166253','2630758923','7188822978',
          '2380578741','6053945839','7776360186','5820991439','2681397883','6361168292','7793180113','6618239676','1706488054','7684701433']
for uid in uids:
    for i in range(1,11):
        print("正在获取第{}页的关注列表:".format(i))
        #微博用户关注列表JSON链接
    
        
        url = "https://m.weibo.cn/api/container/getSecond?containerid=100505{}_-_FOLLOWERS&page=".format(uid) + str(i)
        crawlDetailPage(url,i)
        #设置休眠时间
        # t = random.randint(2,5)
        # print("休眠时间为:{}s".format(t))
        # time.sleep(t)
        pass
    null_list=[
        {'followingId':uid,
        'followingName': '',
        'followingUrl': ' ',
        'followersCount': ' ',
        'followCount': ' ' 
        }
        ]
    with open('followlist.csv', 'a', newline='',encoding='utf-8') as f:
                writer = csv.DictWriter(f,fieldnames=header) # 提前预览列名，当下面代码写入数据时，会将其一一对应。
                # writer.writeheader()  # 写入列名
                writer.writerows(null_list)
