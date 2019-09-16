# -*- coding: utf-8 -*-

import sys
sys.path.append('.')
import codecs
print(sys.getdefaultencoding())

from novels.core.epub_make import *
from novels.tools.masiro_list import *

'''
m = MasiroList('https://masiro.moe/forum.php?mod=forumdisplay&fid=188')

title, list = m.getList()

print(title)

new_list = [link for link, title, date in list]
if new_list != []:
    epub_make(new_list, title)

file = '/Volumes/Storage/Mine/Novels/无职转生/无职转生 Web.epub'
urls = [#'https://masiro.moe/forum.php?mod=viewthread&tid=9704&extra=page%3D7',
        #'https://masiro.moe/forum.php?mod=viewthread&tid=9753&extra=page%3D6',
        #'https://masiro.moe/forum.php?mod=viewthread&tid=9866&extra=page%3D4',
        'https://masiro.moe/forum.php?mod=viewthread&tid=9903&extra=page%3D3',]

epub_make([file]+urls, time_stamp=False)
'''


file = '/Volumes/Storage/Mine/Novels/无职转生/无职转生 Web.epub'
url = 'https://masiro.moe/forum.php?mod=forumdisplay&fid=188'
m = MasiroList(url)

local_date = datetime.fromtimestamp(os.path.getmtime(file)).date()
print('local date: ', local_date)

title, list = m.getList()
new_list = []
for link, title, date in list:
    if date > local_date:
        new_list.append(link)

if new_list != []:
    epub_make([file]+new_list)
