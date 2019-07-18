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


uris = ['https://tieba.baidu.com/p/6115629129']

chapter_pattern = '((第'+re_number+'章.*?)|(Prologue)|(Epilogue)|(角色介绍)|(后记))(?=<)'

epub_make(uris, book_title='【BD附赠特典】OVERLORD——亡国的吸血姬', chapter_check=True, chapter_pattern=chapter_pattern)