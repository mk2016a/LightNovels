from novels.core.epub_bd import *
from novels.core.epub_ln import *
#from novels.bin.epub_qb import *
#from novels.bin.epub_txt import *
from novels.tools.rename import *
from novels.tools.translate import *


# Make All Contents in One Epub
def make_list_epub(urls, book_title, folder = download_dir, chapter_check = False):
    # Prepare
    print('Making Epub...')
    file = folder + book_title + ' ' + time.strftime('%m%d%H%M') + '.epub'
    check_delete_file(file)
    book = mkepub.Book(title=book_title)
    image_count = 0

    for url in urls:
        print(url)
        if re.search('tieba.baidu.com', url):
            bdtb = BDTB(url)
            url, srcs, title, content = bdtb.getContent()
            if srcs != []:
                content, image_count = download_replace(url, srcs, content, book, image_count, ocr_check=True)
        elif re.search('www.lightnovel.cn', url):
            light = LightNovel(url)
            url, srcs, title, content = light.getContent()
            if srcs != []:
                content, image_count = download_replace(url, srcs, content, book, image_count)
        # Convert Simplify Chinese
        content = convert_chinese(content)
        if chapter_check:
        # Split Chapters
            chapters = double_split(title, content)
            addChapter(book, title, chapters)
        else:
        # One Chapter
            content = modify_content(content)               # modify content before add pages to keep most information for former actions\
            book.add_page(title=title, content='<h1>{}</h1>\n'.format(title) + content)

    print(image_count)
    book.set_stylesheet(css_data)
    book.save(file)
    print(title + ' complete.')

'''
urls = [
"http://tieba.baidu.com/p/4318280188",
" http://tieba.baidu.com/p/4365398636",
"http://tieba.baidu.com/p/4390935610",
" http://tieba.baidu.com/p/4452854601",
" http://tieba.baidu.com/p/4523031537",
" http://tieba.baidu.com/p/4538434944",
" http://tieba.baidu.com/p/4552980011",
" http://tieba.baidu.com/p/4672595977",
" http://tieba.baidu.com/p/4698459333",
"http://tieba.baidu.com/p/4866503219",
"http://tieba.baidu.com/p/4913548471",
"http://tieba.baidu.com/p/4920822071",
"http://tieba.baidu.com/p/4922876554",
"http://tieba.baidu.com/p/4926415372",
"http://tieba.baidu.com/p/4928980714",
"http://tieba.baidu.com/p/4950247297",
"http://tieba.baidu.com/p/4957186149",
"http://tieba.baidu.com/p/4964406234",
]
make_epub(urls, 'WEB 第二卷')

urls = [
'http://tieba.baidu.com/p/3894400000',
'https://tieba.baidu.com/p/5061644660',
'https://tieba.baidu.com/p/5835898581?see_lz=1',
'https://tieba.baidu.com/p/5842465384?see_lz=1'
]
make_epub(urls, 'WEB 第三卷')

urls = [
    'https://www.lightnovel.cn/forum.php?mod=viewthread&tid=918462&page=1&authorid=594376',
    'https://tieba.baidu.com/p/5888969323?see_lz=1',
    'https://tieba.baidu.com/p/5564892211?see_lz=1',
    'https://tieba.baidu.com/p/5601036795?see_lz=1',
]
make_epub(urls, '在地下城寻求邂逅是否搞错了什么 13', chapter_check=True)

urls = [
    'https://tieba.baidu.com/p/5784933310?see_lz=1',
    'https://tieba.baidu.com/p/5808242525?see_lz=1',
    'https://tieba.baidu.com/p/5711375072?see_lz=1',
    'https://tieba.baidu.com/p/5725942156?see_lz=1',
]
make_epub(urls, '在地下城寻求邂逅是否搞错了什么 外传 剑姬神圣谭 10')

file = '/Volumes/Storage/Mine/Novels/Re：从零开始的异世界生活/Web/web第六章.csv'
with open(file, 'r') as csv_file:
    csv_read = csv.DictReader(csv_file)
    list = [(row['title'], row['url']) for row in csv_read]
    urls = [item[1] for item in list]
make_epub(urls, ' Re从零开始异世界生活 Web 第六章')

file = '/Volumes/Storage/Mine/Novels/骑士&魔法/web url list.csv'
with open(file, 'r') as csv_file:
    csv_read = csv.DictReader(csv_file)
    list = [(row['title'], row['url']) for row in csv_read]
    urls = [list[-4][1]]
make_epub(urls, '骑士&魔法 147')
'''

# 在地下城期待邂逅是否搞错了什么 14
urls=[
    'https://tieba.baidu.com/p/5979568779?see_lz=1',    #七章 幕间
    'https://tieba.baidu.com/p/5980809799?see_lz=1',    #八章

    'https://tieba.baidu.com/p/5980809799?see_lz=1',    #第十二章
    'https://tieba.baidu.com/p/5983790298?see_lz=1',    #结尾琉部分
]
#make_list_epub(urls, '在地下城期待邂逅是否搞错了什么 14', chapter_check=True)

# 为美好的世界献上祝福 特典
urls=[
'https://tieba.baidu.com/p/5014584647',
'https://tieba.baidu.com/p/5071120628',
'https://tieba.baidu.com/p/5014584647',
'https://tieba.baidu.com/p/5071453162',
'https://tieba.baidu.com/p/5014584647',
'https://tieba.baidu.com/p/5071474881',
'https://tieba.baidu.com/p/4543348020',
'https://tieba.baidu.com/p/5014584647',
'https://www.lightnovel.cn/thread-771624-1-1.html',
'https://tieba.baidu.com/p/5014584647',
'https://tieba.baidu.com/p/5116610759',
'https://www.lightnovel.cn/thread-835364-1-1.html',
'https://tieba.baidu.com/p/5000848400',
'https://www.lightnovel.cn/thread-848663-1-1.html',
'https://tieba.baidu.com/p/5053788788',
'https://www.lightnovel.cn/thread-867919-1-1.html',
'https://www.lightnovel.cn/thread-867919-1-1.html',
'https://tieba.baidu.com/p/5076088220',
'https://tieba.baidu.com/p/5034263001',
'https://www.lightnovel.cn/thread-879172-1-1.html',
'https://tieba.baidu.com/p/5117978589',
'https://tieba.baidu.com/p/5055862485',
'https://www.lightnovel.cn/thread-749378-1-1.html',
'https://tieba.baidu.com/p/4642345211',
'https://tieba.baidu.com/p/4658281434',
'https://tieba.baidu.com/p/4900904305',
'https://tieba.baidu.com/p/4903639605',
'https://www.lightnovel.cn/thread-858436-1-1.html',
'https://tieba.baidu.com/p/5057644592',
'https://www.lightnovel.cn/thread-883480-1-1.html',
'https://tieba.baidu.com/p/5123061093',
'https://tieba.baidu.com/p/5123139809',
'https://tieba.baidu.com/p/5139076890',
'https://tieba.baidu.com/p/3802680609',
'https://tieba.baidu.com/p/5000840311',
'https://tieba.baidu.com/p/5001160991',
'https://tieba.baidu.com/p/5000769130',
'https://tieba.baidu.com/p/5022099636',
'https://tieba.baidu.com/p/5033152425',
'https://tieba.baidu.com/p/5051253411',
'https://tieba.baidu.com/p/5063073420',
'https://tieba.baidu.com/p/4999052535',
'https://tieba.baidu.com/p/4968370377',
'https://tieba.baidu.com/p/5116567943',
'https://tieba.baidu.com/p/5121764201',
'https://tieba.baidu.com/p/5125820114',
'https://tieba.baidu.com/p/5137518022',
'https://tieba.baidu.com/p/5147594755',
'https://tieba.baidu.com/p/5161165134',
'https://tieba.baidu.com/p/5255894810',
'https://www.lightnovel.cn/thread-899174-1-1.html',
'https://tieba.baidu.com/p/5263297745',
'https://tieba.baidu.com/p/5406134431',
'https://tieba.baidu.com/p/5294574731',
'https://tieba.baidu.com/p/5294580569',
'https://tieba.baidu.com/p/5406072326',
'https://tieba.baidu.com/p/5460784675',
'https://tieba.baidu.com/p/5496245346',
'https://tieba.baidu.com/p/5496981455',
'https://tieba.baidu.com/p/5473825573',
'https://tieba.baidu.com/p/5787694065',
'https://tieba.baidu.com/p/5808002783',
'https://tieba.baidu.com/p/5786096594',
'https://tieba.baidu.com/p/5500707003',
]
make_list_epub(urls, '为美好的世界献上祝福 特典')