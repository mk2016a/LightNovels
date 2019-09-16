# -*- coding: utf-8 -*-

import sys
sys.path.append('.')
import codecs
print(sys.getdefaultencoding())

from novels.core.epub_make import *
from novels.tools.masiro_list import *
'''
folder = '/Volumes/Storage/Mine/Novels/重来吧！魔王大人'

file = '/Volumes/Storage/Mine/Novels/重来吧！魔王大人/重来吧！魔王大人 Web.epub'
url = 'https://masiro.moe/forum.php?mod=forumdisplay&fid=189'
m = MasiroList(url)

local_date = datetime.fromtimestamp(os.path.getmtime(file)).date()
print('local date: ', local_date)

new_list = []
title, list = m.getList()
for link, title, date in list:
    if date > local_date:
        new_list.append(link)

if new_list != []:
    epub_make([file]+new_list)
'''

folder = '/Volumes/Storage/Mine/Novels/重来吧！魔王大人'
file = get_file_path(folder)
url = 'https://masiro.moe/forum.php?mod=forumdisplay&fid=189'

_ = Light(url)

local_date = datetime.fromtimestamp(os.path.getmtime(file)).date()
print('local date: ', local_date)

list = _.get_url_list()

new_list = [file]
for link, title, date in list:
    if date > local_date:
        print(title, date)
        new_list.append(link)

if new_list != []:
    print(new_list)
    epub_make(new_list)
