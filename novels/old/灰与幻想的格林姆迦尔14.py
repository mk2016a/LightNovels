import sys
sys.path.append('.')

from novels.core.epub_make import *

# change the username='', password='' in novels.core.epub_ln.py with lightnovel.cn account
# Run codes like example.py

uris = ['https://tieba.baidu.com/p/5987991481','https://tieba.baidu.com/p/6006530874?see_lz=1']
epub_make(uris, book_title='14',chapter_check=True)