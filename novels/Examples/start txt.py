import sys
sys.path.append('.')

from novels.core.epub_txt import *

chapter_pattern = '第'+re_number+'{1,6}章'

# Epub Txt
files = '/Volumes/Storage/Downloads/OVERLORD(WEB版).txt'

et = Epub_Txt(files, chapter_check=True, codes='GBK')
et.make_epub(chapter_pattern=chapter_pattern)