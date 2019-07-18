import sys
sys.path.append('.')

from novels.core.epub_make import *

# change the username='', password='' in novels.core.epub_ln.py with lightnovel.cn account
# Run codes like example.py

chapter_length = 1

re_number = '[1234567890０１２３４５６７８９0零一二三四五六七八九十百①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳]'

chapter_pattern = '((第\s{0,3}?'+re_number+'{1,3}\s{0,3}?[章话节])|(CONTENTS)|(插曲)|(序章'+re_number+'{0,1})|(闲话'+re_number+'{0,1}))\s{1,3}[^\t\n]*'

second_pattern = '\d{1,2}-\d{1,2}.+'

urls = ['https://www.lightnovel.cn/forum.php?mod=viewthread&tid=791827&page=1&authorid=83311']
epub_make(uris=urls, book_title='01', chapter_check=True, chapter_pattern = chapter_pattern, chapter_length=chapter_length)

urls = ['https://www.lightnovel.cn/forum.php?mod=viewthread&tid=812103&page=1&authorid=83311']
epub_make(uris=urls, book_title='02', chapter_check=True, chapter_pattern = chapter_pattern, chapter_length=chapter_length)

urls = ['https://www.lightnovel.cn/forum.php?mod=viewthread&tid=842268&page=1&authorid=83311']
epub_make(uris=urls, book_title='03', chapter_check=True, chapter_pattern = chapter_pattern, chapter_length=chapter_length)

urls = ['https://www.lightnovel.cn/forum.php?mod=viewthread&tid=879579&page=1&authorid=892814']
epub_make(uris=urls, book_title='04', chapter_check=True, chapter_pattern = chapter_pattern, chapter_length=chapter_length)

urls = ['https://www.lightnovel.cn/forum.php?mod=viewthread&tid=879583&page=1&authorid=892814']
epub_make(uris=urls, book_title='05', chapter_check=True, chapter_pattern = chapter_pattern, chapter_length=chapter_length)

urls = ['https://www.lightnovel.cn/forum.php?mod=viewthread&tid=890035&page=1&authorid=398034']
epub_make(uris=urls, book_title='06', chapter_check=True, chapter_pattern = chapter_pattern, chapter_length=chapter_length)
