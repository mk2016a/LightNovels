import sys
sys.path.append('.')

from novels.core.epub_1k import *

url = 'http://www.1ksy.com/27_27601'
e1 = Ep1k(url)
e1.makeEpub()