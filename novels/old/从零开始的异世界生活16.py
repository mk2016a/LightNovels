import sys
sys.path.append('.')

from novels.core.epub_make import *

# change the username='', password='' in novels.core.epub_ln.py with lightnovel.cn account
# Run codes like example.py

chapter_pattern = '(第\s{0,3}?'+re_number+'\s{0,3}?[章话节]《.+?》)|(尾声)|(后记)|(序章)|(EX.+?)'
cl = '(?<=\s)(第'+re_number+'章.+)|(CONTENTS)|(后记)|(序章)(?=<)'
cl2 ='(?<=\s)\d(?=<)'

url = 'https://www.lightnovel.cn/forum.php?mod=viewthread&tid=994495&page=1&authorid=424181'
epub_make(uris=[url], book_title='16', chapter_check=True, chapter_pattern = cl, second_check=True, second_pattern=cl2)