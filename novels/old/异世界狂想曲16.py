import sys
sys.path.append('.')

from novels.core.epub_make import *

# change the username='', password='' in novels.core.epub_ln.py with lightnovel.cn account
# Run codes like example.py

chapter_pattern = '(第\s{0,3}?'+re_number+'\s{0,3}?[章话节]《.+?》)|(尾声)|(后记)|(序章)|(EX.+?)'

urls = ['https://masiro.moe/forum.php?mod=viewthread&tid=6223&page=1&authorid=7727']
epub_make(uris=urls, book_title='16', chapter_check=True, chapter_pattern = chapter_pattern)