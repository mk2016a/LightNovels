import sys
sys.path.append('.')

from novels.core.epub_append import *


# Epub Append
url = 'https://tieba.baidu.com/p/6005227446'
file = '/Volumes/Storage/Mine/Novels/盾之勇者成名录/19 简单剧情介绍 12292105.epub'
epub_append(url, file, '19start append.py', chapter_check=True)