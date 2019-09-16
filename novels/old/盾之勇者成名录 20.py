import sys
sys.path.append('.')

from novels.core.epub_make import *

# Numbers
re_number = '[1234567890０１２３４５６７８９一二三四五六七八九十百①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳]{1,5}?'
# chapter title split pattern core
chapter_pattern_core = ('([间终]\s{0,5}?章)|'
         '(第\s{0,3}?'+re_number+'\s{0,3}?[章话节])|'
         '((?<=\W)'+re_number+'\s{0,3}?[章话节])|'
         '(web.{0,5}?'+re_number+')|'
         '((Chapter)|(CH).{0,5}?'+re_number+')|'
         '((?<=\W)序幕)|(?<=\W)(尾声)|(?<=\W)(后记)|(?<=\W)(目录)|(?<=\W)(Epilogue)|(?<=\W)(CONTENTS)|(?<=\W)(角色介绍)|(?<=\W)(幕间)')
# chapter title split pattern
chapter_pattern = '(?im)('+chapter_pattern_core+')[^<>]{0,30}?(?=<)'

chapter_pattern = '(?m)(台版盾勇..卷.{1,4}章)(?=<)'

urls = [
    'https://tieba.baidu.com/p/5994400912', # 20c
    'https://tieba.baidu.com/p/6186319098', # 20
    'https://tieba.baidu.com/p/6042079527', # 21c
    'https://tieba.baidu.com/p/6232812971', # 22c

]

uris = [bd_see_lz(url) for url in urls]

epub_make(uris, book_title='20', chapter_check=False, chapter_pattern=chapter_pattern)
