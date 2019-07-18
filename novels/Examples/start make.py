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

epub_make('https://www.qinxiaoshuo.com/book/平凡职业造就世界最强')

epub_make('https://www.qinxiaoshuo.com/book/OVERLORD')

epub_make('https://www.qinxiaoshuo.com/book/问题儿童都来自异世界？')

epub_make('https://www.qinxiaoshuo.com/book/Last%20Embryo%28问题儿童都来自异世界？%20第二部%29')

epub_make('https://www.qinxiaoshuo.com/book/末日时在做些什么？能再一次相见吗？')

'''

chapter_pattern = '(?<=\u3000\u3000)(('+re_number+'{1,2}话)|(序幕)|(目次)|(终章))[^<>]{0,9}'

epub_make('https://www.lightnovel.cn/forum.php?mod=viewthread&tid=984941&page=1&authorid=398034', chapter_check=True, chapter_pattern=chapter_pattern)