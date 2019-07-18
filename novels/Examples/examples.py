from novels.core.epub_make import *
from novels.core.epub_append import *


# Epub BD
url = ''
bdtb = BDTB(url)
bdtb.makeEpub()

# Epub LN
url = ''
novel = LightNovel(url)
novel.makeEpub()

# Epub Append
urls = [
    'https://tieba.baidu.com/p/5949791732?see_lz=1',	#14卷封面釋出
    'https://tieba.baidu.com/p/5979568779?see_lz=1',    #14卷 翻譯鍊成 幕間 七章
    'https://tieba.baidu.com/p/5980809799?see_lz=1',	#14卷第八章开坑渣翻
    'https://tieba.baidu.com/p/5980543069?see_lz=1',    #第十四卷 第十二章 渣翻？
    'https://tieba.baidu.com/p/5983790298?see_lz=1',	#详细剧透14卷结尾琉部分
]
#urls = ''
file = '/Volumes/Storage/Mine/Novels/无职转生/[理不尽な孫の手] 无职转生 _到了异世界就拿出真本事_ [06][少年期 归乡篇][台简].epub'
epub_append(urls, file, chapter_check=False)

# Overlord qb
urls = [
    'https://www.23qb.com/book/1230/2884198.html',
    'https://www.23qb.com/book/1230/2910568.html',
    'https://www.23qb.com/book/1230/2910569.html',
    'https://www.23qb.com/book/1230/2910570.html',
    'https://www.23qb.com/book/1230/2910571.html',
    'https://www.23qb.com/book/1230/2910572.html',
    'https://www.23qb.com/book/1230/2910573.html',
    'https://www.23qb.com/book/1230/2910574.html',
    'https://www.23qb.com/book/1230/2910575.html',
    'https://www.23qb.com/book/1230/2910576.html',
'https://www.23qb.com/book/1230/',
]
for url in urls:
    mk_qb(url)

# qb23
urls=[
    'https://www.23qb.com/book/1041/',          # re:从零开始的异世界生活
    'https://www.23qb.com/book/1888/',          # 关于我转生史莱姆这件事
    'https://www.23qb.com/book/17922/',         # 刀剑神域之剑神重生
    'https://www.23qb.com/book/666/',           # SAO刀剑神域外传 Gun Gale Online
    'https://www.23qb.com/book/8201/',          # SAO刀剑神域外传 Clover’s regret
    'https://www.23qb.com/book/1335/',          # 在地下城寻求邂逅是否搞错了什么
    'https://www.23qb.com/book/757/',           # 爆肝工程师的异世界狂想曲
    'https://www.23qb.com/book/893/',           # 为美好的世界献上祝福！
    'https://www.23qb.com/book/1889/',          # 骑士＆魔法
]
for url in urls:
    mk_qb(url)

# Epub Txt
folder = '/Volumes/Storage/Mine/Novels/无职转生/无职转生 Web 1-24'
files = []
for file in sorted(os.listdir(folder)):
    if file.split('.')[-1] == 'txt':
        files.append(os.path.join(folder, file))
#files = '/Volumes/Storage/Downloads/灰与幻想的格林姆迦尔level.12 某岛屿与龙的传说伊始.txt'
et = Epub_Txt(files, chapter_check=True)
et.make_epub()

# Make All
urls = [
    'https://tieba.baidu.com/p/5945463835?see_lz=1',
    'https://tieba.baidu.com/p/5973701607?see_lz=1',
    'https://tieba.baidu.com/p/5511651138',
]
mk_all(urls)

# Get List
url = ''
getList(url)

# Translate
path = ''
tf = Translate(path)
tf.translate_all()

# Rename
path = '/Volumes/Storage/Mine/Novels/素晴'
folder = RenameFiles(path)
folder.rename('为美好的世界献上祝福！', '素晴')


