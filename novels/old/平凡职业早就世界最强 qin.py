import sys
sys.path.append('.')

from novels.core.epub_qin import *

url = 'https://www.qinxiaoshuo.com/book/平凡职业造就世界最强'
print(url)
qin = Qin(url)
qin.makeEpub()