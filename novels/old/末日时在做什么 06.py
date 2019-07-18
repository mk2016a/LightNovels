import sys
sys.path.append('.')

from novels.core.epub_make import *

chapter_pattern = '((第\s{0,3}?'+re_number+'{1,3}?\s{0,3}?章)|(尾声)|(后记)|(序章)).*?(?=<)'

second_pattern = '(第'+re_number+'{1,3}?节).*?(?=<)'

chapter_length = 2000

# Epub Make
uris = [
    'https://www.lightnovel.cn/forum.php?mod=viewthread&tid=942686&page=1&authorid=929872',
]

download_path = '/Volumes/Storage/Downloads/'
epub_make(uris,book_title='6', chapter_check=True, modify_check=True, chapter_pattern=chapter_pattern, second_pattern=second_pattern, chapter_length=chapter_length)