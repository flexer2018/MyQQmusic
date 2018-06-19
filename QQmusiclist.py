# -*- coding: utf-8 -*-
"""
Created on Sat Jun 16 21:22:51 2018
用于下载QQ音乐的文件。有了这个再也不担心下载音乐要开通各种钻了。
在网上现有的代码上进行完善，自动下载320K高音质的音乐，如果没有320K的MP3，
就下载128K的中等音质的MP3
2018-06-19 增加自动生成音乐列表 txt
支持以下格式的URL
'https://y.qq.com/n/yqq/playlist/4167641069.html'
https://y.qq.com/n/yqq/playsquare/4071845186.html
播放列表和歌单可以支持
完善音乐名称有“：”字符的安全处理，文件保留字符的，防止生成相应文件报错。
借用了网上的，发现有更加坑的文件名安全
增加guid 随机数
@author: flexer
@email:
@todo: 专辑列表暂时未支持。
https://y.qq.com/n/yqq/album/002GH0pj1uSvV9.html
"""

import requests
import json
import os
import sys
import time
import random

reload(sys)
sys.setdefaultencoding( "utf-8" )

# 请输入你需要下载的链接
# cdlisturl = 'https://y.qq.com/n/yqq/playlist/4167641069.html'

if len(sys.argv) < 2:
    print u'用于下载QQ音乐的文件。有了这个再也不担心下载音乐要开通各种钻了'
    print ' NO action specified.'
    print u' 请输入参数.如下'
    print u' https://y.qq.com/n/yqq/playlist/4167641069.html'
    sys.exit()

cdlisturl = sys.argv[1]
print cdlisturl

def get_response(url):

    # 下载文件
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    response = requests.get(url=url, headers=headers)
    return response


def save_mp3(music_name, res, word):

    # 保存下载文件
    filePath = os.path.join(os.getcwd(), 'e:/music/' + directory)
    if not os.path.exists(filePath):
        print(u'保存路径不存在')
        os.makedirs(filePath)
        print(u'保存创建路径成功')
        with open('e:/music/' + directory + "/" + music_name, "wb") as file:
            file.write(res)
    else:
        with open('e:/music/' + directory + "/" + music_name, "wb") as file:
            file.write(res)
# 获取下载链接中的CDLIST，歌单的ID


cdlistid = cdlisturl.split('/')[6].split('.')[0]
# print cdlistid

# https://y.qq.com/n/yqq/playlist/2776659672.html
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36', 'Accept-Encoding': 'gzip, deflate, br', 'Accept': '*/*', 'Referer': 'https://y.qq.com/n/yqq/playlist/'+cdlistid+'.html', 'Host': 'c.y.qq.com'}
resp = requests.get('https://c.y.qq.com/qzone/fcg-bin/fcg_ucc_getcdinfo_byids_cp.fcg?type=1&json=1&utf8=1&onlysong=0&disstid='+cdlistid+'&format=jsonp&g_tk='+cdlistid+'&jsonpCallback=playlistinfoCallback&loginUin=12888097&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0', headers=header)

jsonstr = json.loads(resp.text.strip('playlistinfoCallback()[]'))
jsonstr = jsonstr['cdlist'][0]['songlist']
# 这个JSON解析是一个坑，需要注意。不是直接['cdlist']['songlist']而是['cdlist'][0]['songlist']
mids = []
songmids = []
srcs = ''
vkeys = []
songnames = []
singers = []
strMediaMid = []

for j in jsonstr:
    try:
        songmids.append(j['songmid'])
        songnames.append(j['songname'])
        singers.append(j['singer'][0]['name'])
        strMediaMid.append(j['strMediaMid'])  # 这个为关键参数
        mids.append(j['singer'][0]['mid'])
    except:
        # 处理报错
        print(' wrong')

# print j
# 设定需要下载的文件格式。分别为C400 m4a，M500 mp3 128k，M800 mp3 320k，A100 ape ,F00 Flac格式
filerate = "M800"
# 优先下载高品质 (320k mp3)
file_lowerrate = "M500"
# 替代下载品质（128k Mp3）
filetype = ".mp3"
directory = str(cdlistid)
guid = str(int(random.random() * 2147483647) * int(time.time() * 1000) % 10000000000)
for n in range(0, len(mids)):
    resp2 = requests.get('https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?&jsonpCallback=MusicJsonCallback&cid=205361747&songmid='+songmids[n]+'&filename=M500'+mids[n]+filetype+'&guid='+guid)
    #print 'https://y.qq.com/n/yqq/song/'+songmids[n]+'.html'
    json_musickey = json.loads(resp2.text)
    # 获取相应的vkey，CDN服务器的检验
    vkey = json_musickey['data']['items'][0]['vkey']
    vkeys.append(vkey)

save_mp3(str(directory)+'.txt', '音乐', directory)

target = open(str('e:/music/') + str(directory) + "/"+str(directory)+'.txt', 'w')
x = len(vkeys)
# print x
for m in range(0, x):
    mfilename = songnames[m]+' - ' + singers[m] + filetype
    #mfilename=mfilename.replace(":","_")  我自己写的文件名安全
    mfilename = mfilename.replace('|', ':').replace('\"', '').replace('\\', '').replace('“', '').replace('”', '').replace(':', '：').replace('*', '').replace('?','？')
    # 发现还有更坑的文件名，直接借用了
    print(str(m) + '***** ', (songnames[m]), ' *****  Downloading...')
    target.write(str(mfilename)+'\n')
    if (len(vkeys[m]) > 10):
        # 防止没有取到相应的vkey
        # print 'download highres'
        srcs = 'http://dl.stream.qqmusic.qq.com/' + filerate + strMediaMid[m]+filetype+'?guid='+guid+'&vkey='+vkeys[m]+'&uin=0&fromtag=53'
        srcs_lowres = 'http://dl.stream.qqmusic.qq.com/' + file_lowerrate+strMediaMid[m]+filetype+'?guid'+guid+'&vkey='+vkeys[m]+'&uin=0&fromtag=53'
        
        # urllib.urlretrieve(srcs, 'e:/music/' + directory + mfilename)

        try:
            res = get_response(srcs)
            save_mp3(mfilename, res.content, directory)
            print srcs
            print 'downloaded highres: '+res.headers["Content-Length"]
            # print res.headers["Content-Length"]
            if int(res.headers["Content-Length"]) < 100:
                res = get_response(srcs_lowres)
                save_mp3(mfilename, res.content, directory)
                print 'download lower res: ' + res.headers["Content-Length"]
                print srcs_lowres
        # 异常报错处理
        except requests.exceptions.ConnectionError:
            print ('Req ConnectionError')
            x = x - 1
        except requests.exceptions.ReadTimeout:
            print ('Req ReadTimeout')
            x = x - 1
        except requests.exceptions.ConnectTimeout:
            print ('Req ConnectTimeout')
            x = x - 1
        except requests.exceptions.ChunkedEncodingError:
            print ('Req ChunkedEncodingError')
            x = x - 1
            # 下载失败
            print(' Download wrong~')
            
target.close()
print('For Download complete '+str(x)+'files !')
