import sys
sys.path.append('.')

from novels.core.epub_make import *

# Epub Make
uris = [
    'https://www.lightnovel.cn/forum.php?mod=viewthread&tid=957796&page=1&authorid=851136',
]

download_path = '/Volumes/Storage/Downloads/'
epub_make(uris,book_title='续·爆炎！2 任性妄为破坏者', chapter_check=True)