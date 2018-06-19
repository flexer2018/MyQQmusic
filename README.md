# MyQQmusic
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
