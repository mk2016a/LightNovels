import sys
sys.path.append('.')

from novels.core.epub_make import *

# change the username='', password='' in novels.core.epub_ln.py with lightnovel.cn account
# Run codes like example.py

#uris = input('Uris are:\n').split(',')
#print(uris)

uris = [
    #'https://www.lightnovel.cn/thread-946682-1-1.html',
    'https://www.lightnovel.cn/thread-922142-1-1.html',
]
chapter_pattern = "(「年歲尚幼者」-someday, I will be-)|(「亡國姬勇者」-about a wild flower-)|(「食人鬼吐露心聲」-your happiness-)|(「藍天的黃金妖精」-girl's pride-)|(「閃閃發亮的劍」-shall you save us?-)|(無法延後的後記/肯定仍是後記)"
chapter_pattern = convert_chinese(chapter_pattern)
second_pattern = '(?<=>)\s*?'+re_number+'\..*?(?=<)'


epub_make(uris, book_title='台版EX卷特典', chapter_check=True, chapter_pattern=chapter_pattern, second_pattern=second_pattern)