import sys
sys.path.append('.')

from novels.core.epub_wk import *

url = 'https://www.wenku8.net/book/2080.htm'
print(url)
wk = WK8(url)
wk.makeEpub()