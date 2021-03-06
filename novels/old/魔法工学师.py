# -*- coding: utf-8 -*-

import sys
sys.path.append('.')
import codecs
print(sys.getdefaultencoding())

from novels.core.epub_make import *
from novels.tools.masiro_list import *

'''
m = MasiroList('https://masiro.moe/forum.php?mod=forumdisplay&fid=230')

title, list = m.getList()

print(title)

new_list = [link for link, title, date in list]
if new_list != []:
    epub_make(new_list, title)
'''

file = '/Volumes/Storage/Mine/Novels/魔法工学师/魔法工学师 Web.epub'
url = 'https://masiro.moe/forum.php?mod=forumdisplay&fid=230'
m = MasiroList(url)

local_date = datetime.fromtimestamp(os.path.getmtime(file)).date()
print('local date: ', local_date)

title, list = m.getList()
new_list = []
for link, title, date in list:
    if date > local_date:
        new_list.append(link)
        print(title, date)

mf = '^\d\d-\d\d.+?$'
if new_list != []:
    epub_make([file]+new_list, chapter_check=True, chapter_pattern=mf)