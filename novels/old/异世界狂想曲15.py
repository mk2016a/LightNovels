import sys
sys.path.append('.')

from novels.core.epub_make import *

# change the username='', password='' in novels.core.epub_ln.py with lightnovel.cn account
# Run codes like example.py

chapter_pattern = '(第\s{0,3}?'+re_number+'\s{0,3}?[章话节]《.+?》)|(尾声)|(后记)|(EX.+?)'

urls = ['https://tieba.baidu.com/p/5945463835?see_lz=1']
epub_make(uris=urls, book_title='15', chapter_check=True, chapter_pattern = chapter_pattern)