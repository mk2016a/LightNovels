import sys
sys.path.append('.')

from novels.core.epub_make import *

chapter_pattern = '((第\s{0,3}?'+re_number+'\s{0,3}?[章话节])|(幕间)|(序章)|(终章)|(尾声)|(后记)|(EX.+?))[^。]{0,10}(?=<)'

uris = 'https://tieba.baidu.com/p/6064749926?see_lz=1',        # 14
epub_make(uris, book_title='14', chapter_check=True, chapter_pattern=chapter_pattern)

