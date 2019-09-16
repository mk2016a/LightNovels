import sys
sys.path.append('.')

from novels.core.epub_make import *


# Epub Append
folder = '/Volumes/Storage/Mine/Novels/骑士&魔法/'
file = get_file_path(folder)
urls = [
    'https://tieba.baidu.com/p/6126554456',             # 157
    'https://tieba.baidu.com/p/6215925595',  # 158
]

urls = 'https://tieba.baidu.com/p/6252042876'       #159

if type(urls) is list:
    uris = [file] + [bd_see_lz(url) for url in urls]
elif type(urls) is str:
    uris = [file] + [bd_see_lz(urls)]

epub_make(uris, '骑士&魔法 Web', chapter_check=False)