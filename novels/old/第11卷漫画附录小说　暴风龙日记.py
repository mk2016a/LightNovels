import sys
sys.path.append('.')

from novels.core.epub_make import *

chapter_pattern = '◆[^◆]{0,10}◆'

uris = 'https://tieba.baidu.com/p/6096449622?see_lz=1',        # 11
epub_make(uris, book_title='第11卷漫画附录小说　暴风龙日记', chapter_check=True, chapter_pattern=chapter_pattern)
