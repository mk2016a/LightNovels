import sys
sys.path.append('.')

from novels.core.epub_make import *

chapter_pattern = '((第\s{0,3}?'+re_number+'\s{0,3}?[章话节])|(幕间)|(序章)|(终章)|(尾声)|(后记)|(EX.+?))[^。]{0,10}(?=<)'

uris = 'https://masiro.moe/forum.php?mod=viewthread&tid=7256&extra=&authorid=42&page=1',        # 14
epub_make(uris, book_title='14', chapter_check=True, chapter_pattern=chapter_pattern)

