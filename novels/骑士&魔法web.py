import sys
sys.path.append('.')

from novels.core.epub_make import *


# Epub Append
uris = [
    '/Volumes/Storage/Mine/Novels/骑士&魔法/骑士&魔法 Web.epub',
    #'https://tieba.baidu.com/p/6078893177',             # 156
    #'https://tieba.baidu.com/p/6126554456',             # 157
]
epub_make(uris, '骑士&魔法 Web', chapter_check=False, time_stamp=False)