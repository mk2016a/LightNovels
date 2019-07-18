import sys
sys.path.append('.')

from novels.core.epub_qin import *

url = 'https://www.qinxiaoshuo.com/book/为了女儿，我说不定连魔王都能干掉%28为了女儿击倒魔王%29'
print(url)
qin = Qin(url)
qin.makeEpub()