import sys
sys.path.append('.')

from novels.core.epub_make import *


# Epub Append
uris = [
    '/Volumes/Storage/Mine/Novels/异世界狂想曲/异世界狂想曲 Web.epub',
    #'https://tieba.baidu.com/p/6108396518',     # 17-13
    #'https://tieba.baidu.com/p/6115732389',     # 17-14.1
    #'https://tieba.baidu.com/p/6122012179',     # 17-14.2
    #'https://tieba.baidu.com/p/6129378533',     # 17-14.3
    #'https://tieba.baidu.com/p/6129378533?see_lz=1'     # 17-15
    #'https://tieba.baidu.com/p/6136296840?see_lz=1',    # 17-16
    #'https://tieba.baidu.com/p/6143450586?see_lz=1',    # 17-17
    #'https://tieba.baidu.com/p/6150627191',     # 17-18
    #'https://tieba.baidu.com/p/6157785199?see_lz=1',        # 17-19
    #'https://tieba.baidu.com/p/6165005933',     # 17-20
    #'https://tieba.baidu.com/p/6172197724?see_lz=1',    # 17-21
    #'https://tieba.baidu.com/p/6180658799',     # 17-22
    #'https://tieba.baidu.com/p/6186926684',     # 17-23
    #'https://tieba.baidu.com/p/6194045683',     # 17-24
]
epub_make(uris, book_title='异世界狂想曲 Web', chapter_check=False, time_stamp=False)