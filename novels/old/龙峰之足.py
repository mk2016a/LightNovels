# -*- coding: utf-8 -*-

import sys
sys.path.append('.')
import codecs
print(sys.getdefaultencoding())

from novels.core.epub_make import *
from novels.tools.masiro_list import *

'''
m = MasiroList('https://masiro.moe/forum.php?mod=forumdisplay&fid=66')

title, list = m.getList()

print(title)

new_list = [link for link, title, date in list]
if new_list != []:
    epub_make(new_list, title)


file = ['/Volumes/Storage/Mine/Novels/龙峰之足/龙峰之足 Web.epub']

urls = [
    'https://tieba.baidu.com/p/6212313840',
    'https://tieba.baidu.com/p/6214082444',
    'https://tieba.baidu.com/p/6214644040',
    'https://tieba.baidu.com/p/6215679898',
    'https://tieba.baidu.com/p/6216675279',
    'https://tieba.baidu.com/p/6217230214',
    'https://tieba.baidu.com/p/6217708225',
    'https://tieba.baidu.com/p/6219523284',
    'https://tieba.baidu.com/p/6219483400',
    'https://tieba.baidu.com/p/6220026864',
    'https://tieba.baidu.com/p/6220482157',
    'https://tieba.baidu.com/p/6220849759',
    'https://tieba.baidu.com/p/6221588804',
    'https://tieba.baidu.com/p/6222172941',
    'https://tieba.baidu.com/p/6222544532',
    'https://tieba.baidu.com/p/6223711983',
    'https://tieba.baidu.com/p/6224634335',
    'https://tieba.baidu.com/p/6225081372',
    'https://tieba.baidu.com/p/6225246378',     # 460
    'https://tieba.baidu.com/p/6225485335',
    'https://tieba.baidu.com/p/6225906469',
    'https://tieba.baidu.com/p/6226018836',
    'https://tieba.baidu.com/p/6228023104',
    'https://tieba.baidu.com/p/6228918377',
    'https://tieba.baidu.com/p/6229477203',
    'https://tieba.baidu.com/p/6230508369',
    'https://tieba.baidu.com/p/6230518890',
    'https://tieba.baidu.com/p/6231554092',
    'https://tieba.baidu.com/p/6237412706',
    'https://tieba.baidu.com/p/6237551516',
    'https://tieba.baidu.com/p/6237564248',
    'https://tieba.baidu.com/p/6237952607',
    'https://tieba.baidu.com/p/6239065082',
    'https://tieba.baidu.com/p/6239302724',
    'https://tieba.baidu.com/p/6240143862',
    'https://tieba.baidu.com/p/6239842877',
    'https://tieba.baidu.com/p/6240126126',
    'https://tieba.baidu.com/p/6241723134',
    'https://tieba.baidu.com/p/6241729864',
    'https://tieba.baidu.com/p/6243503176',
    'https://tieba.baidu.com/p/6243656268',
    'https://tieba.baidu.com/p/6243661656',
    'https://tieba.baidu.com/p/6243670221',
    'https://tieba.baidu.com/p/6243077208',
    'https://tieba.baidu.com/p/6243444858',
    'https://tieba.baidu.com/p/6245046038',     #487
]

uris = file + urls

epub_make(uris, time_stamp=False)

'''

file = '/Volumes/Storage/Mine/Novels/龙峰之足/龙峰之足 Web.epub'
url = 'https://masiro.moe/forum.php?mod=forumdisplay&fid=66'
m = MasiroList(url)

local_date = datetime.fromtimestamp(os.path.getmtime(file)).date()
print('local date: ', local_date)

title, list = m.getList()
new_list = []
for link, title, date in list:
    if date > local_date:
        new_list.append(link)

if new_list != []:
    epub_make([file]+new_list, time_stamp=False)