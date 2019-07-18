import sys
sys.path.append('.')

from novels.core.epub_make import *

# change the username='', password='' in novels.core.epub_ln.py with lightnovel.cn account
# Run codes like example.py

#uris = input('Uris are:\n').split(',')
#print(uris)

'''
uris = [
    'https://tieba.baidu.com/p/5972159545',     #   序章
    'https://tieba.baidu.com/p/6051288645',     #   1
]

chapter_pattern = '((第\s{0,3}?'+re_number+'{1,3}?\s{0,3}?章)|(尾声)|(后记)|(序章)).*?(?=<)'

second_pattern = '(第'+re_number+'{1,3}?节).*?(?=<)'

epub_make(uris, book_title='07', chapter_check=True, chapter_pattern=chapter_pattern, second_pattern=second_pattern)
'''

chapter_pattern = 'CHAPTER[^<]+'
second_pattern = '\d(?=<)'

uris = ['https://tieba.baidu.com/p/6165113628']

#epub_make(uris, book_title='09 加奈美东行记', chapter_pattern=chapter_pattern, chapter_check=True, time_stamp=False, second_check=True, second_pattern=second_pattern)

chapter_pattern = '◆\s?\d\d'

uris = ['https://tieba.baidu.com/p/6157684930']

epub_make(uris, book_title='10 开拓智域', chapter_pattern=chapter_pattern, chapter_check=True, time_stamp=False)

chapter_pattern = '◆\s?Chapter.{3,4}'

uris = ['https://tieba.baidu.com/p/4300925967']

epub_make(uris, book_title='11 大亨领主克拉斯提', chapter_pattern=chapter_pattern, chapter_check=True, time_stamp=False)

uris = ['https://tieba.baidu.com/p/6169299024']

epub_make(uris, book_title='12 圆桌崩坏', chapter_pattern=chapter_pattern, chapter_check=True, time_stamp=False)

uris = ['https://tieba.baidu.com/p/5027257434']

#epub_make(uris, book_title='13 夜啼鸟之歌', chapter_pattern=chapter_pattern, chapter_check=True, time_stamp=False)

uris = ['https://tieba.baidu.com/p/5481984724']

#epub_make(uris, book_title='14 黄昏的孤儿', chapter_pattern=chapter_pattern, chapter_check=True, time_stamp=False)
