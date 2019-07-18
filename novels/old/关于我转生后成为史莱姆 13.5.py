import sys
sys.path.append('.')

from novels.core.epub_make import *

chapter_pattern = ('(魔物之国的薪酬事宜)|'
                   '(常夜之国的至高女神)|'
                   '(染上鲜红的湖畔事变)|'
                   '(街角的技术革新)|'
                   '(早起的魔国农家)|'
                   '(地狱的修炼场)|'
                   '(密探、秘密行动)|'
                   '(迷宫和冒险者)')      # 13.5

# change the username='', password='' in novels.core.epub_ln.py with lightnovel.cn account
# Run codes like example.py

#uris = input('Uris are:\n').split(',')
#print(uris)

uris = 'https://tieba.baidu.com/p/6064749926?see_lz=1',        # 13.5
epub_make(uris, book_title='14', chapter_check=True, chapter_pattern=chapter_pattern)

