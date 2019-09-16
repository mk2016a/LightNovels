import sys
sys.path.append('.')

from novels.core.epub_make import *

sp = '(?<=>)\s*?(\d{1,2})\s*?(?=<)'
download_path = '/Volumes/Storage/Downloads/'
'''
# Epub Make
uris = ['https://www.lightnovel.cn/forum.php?mod=viewthread&tid=940611&page=1&authorid=981224',]
epub_make(uris,book_title='Extra 让笨蛋登上舞台吧 1', chapter_check=True, second_check=True, second_pattern=sp)

# Epub Make
uris = ['https://www.lightnovel.cn/forum.php?mod=viewthread&tid=961756&page=1&authorid=981224',]
epub_make(uris,book_title='Extra 让笨蛋登上舞台吧 2', chapter_check=True, second_check=True, second_pattern=sp)

# Epub Make
uris = ['https://www.lightnovel.cn/forum.php?mod=viewthread&tid=890665&page=1&authorid=851136',]
sp1 = '(?<=>)\s*?(\d\.)\s*?(?=<)'
#epub_make(uris,book_title=convert_chinese('一季动画BD特典1‧~為白虎奉上加護~'), chapter_check=True, chapter_pattern=sp1)

#epub_make('https://www.lightnovel.cn/thread-895669-1-1.html', convert_chinese('一季动画BD特典2‧阿克塞爾的爆裂偵探'), chapter_check=True, chapter_pattern=sp)

cp1 = convert_chinese('^((屠龍者惠惠)|(藝術就是爆裂)|(紅瞳的初學者殺手)|(偶爾來次這樣的爆裂約會)|(開膛手惠惠))(?=<)')
epub_make('https://www.lightnovel.cn/forum.php?mod=viewthread&tid=888365&page=1&authorid=851136', book_title='九卷台版特典', chapter_check=True, chapter_pattern=cp1)

cp2 = convert_chinese('(吉祥物的真面目……)|(惡魔的禁書)|(VS!)|(紅魔族的抑制力)|(少女的價值在於……)|(阿克塞爾第一的……)')
#epub_make('https://www.lightnovel.cn/forum.php?mod=viewthread&tid=900371&page=1&authorid=851136', book_title=convert_chinese('續‧為美好的世界獻上爆炎！台版首刷特典'), chapter_check=True, chapter_pattern=cp2)


#epub_make('https://www.lightnovel.cn/forum.php?mod=viewthread&tid=880034&page=1&authorid=599122', book_title='为美好的世界献上爆焰3 虎之穴&GAMERS加笔短篇小册子')

#epub_make('https://www.lightnovel.cn/forum.php?mod=viewthread&tid=994851&page=1&authorid=413289', convert_chinese('續‧為美好的世界獻上爆焰！1 Gamers特典短篇 武鬥派公主的治安活動'))

#epub_make('https://www.lightnovel.cn/forum.php?mod=viewthread&tid=995036&page=1&authorid=413289', convert_chinese('3 Animate 偶爾做些像是女神的事'))

'''