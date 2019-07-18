import sys
sys.path.append('.')

from novels.core.epub_make import *

# Chapter Pattern
## Numbers
re_number = '[1234567890０１２３４５６７８９一二三四五六七八九十百①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳]{1,5}?'
## chapter title split pattern core
chapter_pattern_core = ('(幕间)|(序言)|(目录)|(间章)|(尾声)|'
         '('+re_number+'章)')
## chapter title split pattern
chapter_pattern = '(?im)(?<=<strong>)('+chapter_pattern_core+')[^<>]{0,20}?(?=</strong>)'

# Epub Append
url = [
    'https://www.lightnovel.cn/thread-953759-1-1.html',
       ]

download_path = '/Volumes/Storage/Downloads/'
epub_make(url,book_title='14 ln', chapter_check=True, chapter_pattern=chapter_pattern)