import sys
sys.path.append('.')

from novels.core.epub_make import *


# Epub Append
file = [
    '/Volumes/Storage/Mine/Novels/Re：从零开始的异世界生活/Web/Web 第六章.epub',
        ]

urls = [

]

uris = file + [bd_see_lz(url) for url in urls]

epub_make(uris,  chapter_check=False)