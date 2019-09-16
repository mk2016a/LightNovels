import sys
sys.path.append('.')

from novels.core.epub_make import *

second_pattern = '(?<=>)\s*?(\d{1,2})\s*?(?=<)'

# Epub Make
uris = [
    'https://www.lightnovel.cn/forum.php?mod=viewthread&tid=988976&page=1&authorid=540169',
]

download_path = '/Volumes/Storage/Downloads/'
epub_make(uris,book_title='16', chapter_check=True, second_check=True, second_pattern=second_pattern)
