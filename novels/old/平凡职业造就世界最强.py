# -*- coding: utf-8 -*-

import sys
sys.path.append('.')
import codecs
print(sys.getdefaultencoding())

from novels.core.epub_make import *
from novels.tools.masiro_list import *

'''
m = MasiroList('https://masiro.moe/forum.php?mod=forumdisplay&fid=200')

title, list = m.getList()

print(title)

new_list = [link for link, title, date in list]
if new_list != []:
    epub_make(new_list, title)
    
    
file = '/Volumes/Storage/Mine/Novels/平凡职业造就世界最强/平凡职业造就世界最强 Web.epub'
urls = ['https://masiro.moe/forum.php?mod=viewthread&tid=9704&extra=page%3D7',
        'https://masiro.moe/forum.php?mod=viewthread&tid=9753&extra=page%3D6',]

epub_make([file]+urls, time_stamp=False)
'''

file = '/Volumes/Storage/Mine/Novels/平凡职业造就世界最强/平凡职业造就世界最强 Web.epub'
url = 'https://masiro.moe/forum.php?mod=forumdisplay&fid=200'
m = MasiroList(url)

local_date = datetime.fromtimestamp(os.path.getmtime(file)).date()
print('local date: ', local_date)

title, list = m.getList()
new_list = []
for link, title, date in list:
    if date > local_date:
        new_list.append(link)
        print(title, date)

if new_list != []:
    epub_make([file]+new_list)



