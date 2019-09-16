# -*- coding: utf-8 -*-

import sys
sys.path.append('.')
import codecs
print(sys.getdefaultencoding())

from novels.core.epub_make import *
from novels.tools.masiro_list import *
'''
# Epub Append
file = ['/Volumes/Storage/Mine/Novels/异世界狂想曲/异世界狂想曲 Web.epub',]

urls = [
    'https://tieba.baidu.com/p/6108396518',     # 17-13
    'https://tieba.baidu.com/p/6115732389',     # 17-14.1
    'https://tieba.baidu.com/p/6122012179',     # 17-14.2
    'https://tieba.baidu.com/p/6129378533',     # 17-14.3
    'https://tieba.baidu.com/p/6129378533?see_lz=1'     # 17-15
    'https://tieba.baidu.com/p/6136296840?see_lz=1',    # 17-16
    'https://tieba.baidu.com/p/6143450586?see_lz=1',    # 17-17
    'https://tieba.baidu.com/p/6150627191',     # 17-18
    'https://tieba.baidu.com/p/6157785199?see_lz=1',        # 17-19
    'https://tieba.baidu.com/p/6165005933',     # 17-20
    'https://tieba.baidu.com/p/6172197724?see_lz=1',    # 17-21
    'https://tieba.baidu.com/p/6180658799',     # 17-22
    'https://tieba.baidu.com/p/6186926684',     # 17-23
    'https://tieba.baidu.com/p/6194045683',     # 17-24
]

urls = [bd_see_lz(url) for url in urls]


urls = [
    'https://tieba.baidu.com/p/6208247139',     # 17-25
    'https://tieba.baidu.com/p/6215488000',     # 17-26
    'https://tieba.baidu.com/p/6222933382',     # 17-27
    'https://tieba.baidu.com/p/6229819904',     # 17-28
    'https://tieba.baidu.com/p/6236462524',     # 17-29
]

urls = [bd_see_lz(url) for url in urls]

urls = ['https://masiro.moe/forum.php?mod=viewthread&tid=16702&page=1&authorid=8303']

uris = file + urls


epub_make(uris, book_title='异世界狂想曲 Web', chapter_check=False, time_stamp=False)


m = MasiroList('https://masiro.moe/forum.php?mod=forumdisplay&fid=143')

title, list = m.getList()

print(title)

new_list = [link for link, title, date in list]
if new_list != []:
    epub_make(new_list[-15:], title)
    
'''

folder = '/Volumes/Storage/Mine/Novels/异世界狂想曲/'
file = get_file_path(folder)
url = 'https://masiro.moe/forum.php?mod=forumdisplay&fid=143'

_ = Light(url)

local_date = datetime.fromtimestamp(os.path.getmtime(file)).date()
print('local date: ', local_date)

_.get_url_list()
list = _.url_list

new_list = [file]
for link, title, date in list:
    if date > local_date:
        print(title, date)
        new_list.append(link)

if new_list != []:
    epub_make(new_list)

