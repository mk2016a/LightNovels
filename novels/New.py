# -*- coding: utf-8 -*-

import sys
sys.path.append('.')

from novels.core.epub_make import *
from novels.tools.masiro_list import *

from novels.core.epub_qb import *


url = 'http://qinxiaoshuo.com/book/OVERLORD'
'''
_ = QB23('https://www.x23qb.com/book/1888/')
_.makeEpub()
'''

epub_make(url)