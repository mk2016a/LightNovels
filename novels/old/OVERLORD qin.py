import sys
sys.path.append('.')

from novels.core.epub_qin import *

url = 'https://www.qinxiaoshuo.com/book/OVERLORD'
print(url)
qin = Qin(url)
qin.makeEpub()