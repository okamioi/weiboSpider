

import requests

import pandas as pd

from time import sleep

import json
import csv

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


def parseUid(uid):
    response = requests.get(url=f'https://weibo.com/ajax/profile/info?custom={uid}', headers=headers)
    try:
        return response.json()['data']['user']['id']
    except:
        return None


def getUserInfo(uid):
    try:
        uid = int(uid)
    except:
        # 说明是 xiena 这样的英文串
        uid = parseUid(uid)
        if not uid:
            return None
    response1 = requests.get(url=f'https://weibo.com/ajax/profile/detail?uid={uid}', headers=headers)
    response2 = requests.get(url=f'https://weibo.com/ajax/profile/info?custom={uid}', headers=headers)
    if response1.status_code == 400:
        return {
            'errorMsg': '用户可能注销或者封号',
            'location': None,
            'user_link': f'https://weibo.com/{uid}'
        }
    resp_json = response1.json().get('data', None)
    resp_json2 = response2.json().get('data', None)
    # print(resp_json2)
    if not resp_json:
        return None
    sunshine_credit = resp_json.get('sunshine_credit', None)
    if sunshine_credit:
        sunshine_credit_level = sunshine_credit.get('level', None)
    else:
        sunshine_credit_level = None
    education = resp_json.get('education', None)
    if education:
        school = education.get('school', None)
    else:
        school = None

    # location = resp_json.get('location',None)
    gender = resp_json.get('gender', None)

    birthday = resp_json.get('birthday', None)
    created_at = resp_json.get('created_at', None)
    description = resp_json.get('description', None)
    # 我关注的人中有多少人关注 ta
    followers = resp_json2.get('user', None)
    if followers:
        followers_num = followers.get('followers_count', None)
        location = followers.get('location',None)
        subscribe = followers.get('friends_count',None)
        weibo_num = followers.get('statuses_count',None)
        screen_name = followers.get('screen_name',None)
    else:
        followers_num = None
    return [
        {'screen_name':screen_name,
        'sunshine_credit_level': sunshine_credit_level,
        'school': school,
        'location': location,
        'gender': gender,
        'birthday': birthday,
        'created_at': created_at,
        'description': description,
        'followers_num': followers_num,
        'subscribe_num':subscribe,
        'weibo_num':weibo_num}
    ]




if __name__ == '__main__':
    uid= ['7487619146','5831481714','5396590503','5926660141','5837469270','2029906001','1779654914','6791517858','5746403289','6049590367',
          '1992246393','1588741002','1787697542','3937348351','5463794433','2309846073','3205933003','5898166253','2630758923','7188822978',
          '2380578741','6053945839','7776360186','5820991439','2681397883','6361168292','7793180113','6618239676','1706488054','7684701433']
    for id in uid:
        user_info = getUserInfo(id)
        # print(user_info)
        header=[
            'screen_name','sunshine_credit_level','school','location','gender','birthday','created_at','description','followers_num','subscribe_num','weibo_num'
        ]
        with open('userinfo.csv', 'a', newline='',encoding='utf-8') as f:
            writer = csv.DictWriter(f,fieldnames=header) # 提前预览列名，当下面代码写入数据时，会将其一一对应。
            # writer.writeheader()  # 写入列名
            writer.writerows(user_info)

