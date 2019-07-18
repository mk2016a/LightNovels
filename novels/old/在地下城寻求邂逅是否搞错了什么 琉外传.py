import sys
sys.path.append('.')

from novels.core.epub_make import *

# change the username='', password='' in novels.core.epub_ln.py with lightnovel.cn account
# Run codes like example.py

#uris = input('Uris are:\n').split(',')
#print(uris)
uris = [
    'https://www.lightnovel.cn/thread-851399-1-1.html',
    'https://www.lightnovel.cn/thread-854147-1-1.html',
    'https://www.lightnovel.cn/thread-856863-1-1.html',
    'https://www.lightnovel.cn/thread-860874-1-1.html',
    'https://www.lightnovel.cn/thread-863922-1-1.html',
    'https://www.lightnovel.cn/thread-866783-1-1.html',
]
epub_make(uris, book_title='琉外传', chapter_check=False)