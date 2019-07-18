import sys
sys.path.append('.')

from novels.core.epub_make import *


# Epub Append
uris = [
    '/Volumes/Storage/Mine/Novels/Re：从零开始的异世界生活/Web/Web 第六章.epub',
        ]
epub_make(uris,  chapter_check=False)