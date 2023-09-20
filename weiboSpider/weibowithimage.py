from urllib.parse import urlencode
from pyquery import PyQuery as pq
from hashlib import md5
import requests
import re
import os

base_url='https://m.weibo.cn/api/container/getIndex?'
headers={
    'Host':'m.weibo.cn',
    'Referer':'https://m.weibo.cn/u/3624694175',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.84',
    'X-Requested-With':'XMLHttpRequest'
}

#获取一个ajax的响应
def get_page(page):
    params={#构造getindex连接，要换不同的用户时，需要更换对应的uid和conternerid
        'type':'uid',
        'value':'{}'.format(uid),#uid value
        'containerid':'107603{}'.format(uid),
        'page':page
    }
    url=base_url+urlencode(params)#构造ajax的getindex url
    try:
        response=requests.get(url,headers=headers)#获取url的响应
        if response.status_code==200:
            return response.json()#返回响应的内容，并转成json格式，也就是再浏览器F12观察到的结构
    except requests.ConnectionError as e:
        print('Error',e.args)
        
#保存每个card的图片
def save_image(item):
    if item:
        text=re.sub(r'[\\/\:\*\?\"\<\>\|\n]','',pq(item.get('text')).text())[0:128]
        #这里以微博内容作为文件名，所以要去掉文件命名非法符号，然后长度要在0：128之间
        if not os.path.exists('result/'+text):#如果不存在目标文件夹
            os.mkdir('result/'+text)#新建文件夹
        images=item.get('pic_ids')#获取id
        for image in images:
            try:
                response=requests.get('https://wx1.sinaimg.cn/large/'+image+'.jpg')
                #根据url获取图片
                if response.status_code==200:
                    file_path='result/{0}/{1}.{2}'.format(text,md5(response.content).hexdigest(),'jpg')
                    #保存到对应的文件夹
                if not os.path.exists(file_path):
                    with open(file_path,'wb') as f:
                        f.write(response.content)
                else:
                    print('downloaded ever',file_path)
            except requests.ConnectionError:
                print('falied')
                
def parse_page(json):
    if json:
        items=json.get('data').get('cards')
        for item in items:
            item=item.get('mblog')
            save_image(item)


#主函数

uid=3624694175 #修改这里来改变用户

if not os.path.exists('result'):#创建工作路径下的一个子目录存取图片
    os.mkdir('result')
 
for page in range(1,11):#修改这里来改变获取微博数（页）
    json=get_page(page)
    results=parse_page(json)
    if results:
        for result in results:
            print(result)