from novels.core.epub_bd import *
from novels.core.epub_ln import *
#from novels.bin.epub_qb import *
#from novels.bin.epub_txt import *
from novels.tools.rename import *
from novels.tools.translate import *

re_number = '[1234567890０１２３４５６７８９一二三四五六七八九十百]{1,5}?'
# chapter title split pattern core
chapter_pattern_core = ('(序\s{0,5}?[章幕言])|'
         '([间终]\s{0,5}?章)|'
         '(第?\s{0,3}?'+re_number+'\s{0,3}?[章话节])|'
         '('+re_number+'[\.\s])|'
         '(web.{0,5}?'+re_number+')|'
         '((Chapter)|(CH).{0,5}?'+re_number+')|'
         '(尾声)|(后记)|(目录)|(Epilogue)|(CONTENTS)|(角色介绍)|(幕间)')
# chapter title split pattern
chapter_pattern = '(?im)[^<>]{0,10}?('+chapter_pattern_core+')[^<>]{0,30}?(?=<)'
# second chapter title split pattern
second_pattern = '(?<=>)\s*?(\d{1,2}?)\s*?(?=<)'

download_path = '/Volumes/Storage/Downloads/'

# Epub Append
def epub_append(urls='', file='', book_title='', folder='', chapter_check=False):
    # Prepare New Book
    print('Making Epub...')
    if folder == '':
        if file != '':
            folder = os.path.dirname(file)
        else:
            folder = download_path
    if book_title == '':
        if file != '':
            book_title = file.split('/')[-1].split('.')[0]
        else:
            book_title = input('Please enter book title:')
            book_title = book_title.replace('/', ' ')
            book_title = book_title.replace('.', ' ')
    new_file = folder + '/' + book_title + ' ' + time.strftime('%m%d%H%M') + '.epub'
    book = mkepub.Book(title=book_title)

    # Check Original Epub File
    if file != '':
        path = file.split('.')[0]
        title_content_list, image_list = read_epub(path)
        for title, content in title_content_list:
            title = convert_chinese(title)
            content = convert_chinese(content)
            book.add_page(title=title, content=content)
        if image_list != {}:
            try:
                book.set_cover(image_list['0001.jpg'])
            except Exception as e:
                print(e)
            for name, image in image_list.items():
                book.add_image(name, image)
        image_count = len(image_list)
        rmtree(path)
    else:
        image_count = 0

    # Append or Make Epub from urls
    if urls != '':
        if isinstance(urls, str):
            urls = [urls]
        for url in urls:
            try:
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
                    chapters = double_split(title, content, first_p=chapter_pattern, second_p=second_pattern)
                    print(chapters)
                    addChapter(book, title, chapters)
                else:
                # One Chapter
                    # modify content before add pages to keep most information for former actions
                    content = modify_content(content)
                    print(content)
                    book.add_page(title=title, content='<h1>{}</h1>\n'.format(title) + content)
            except Exception as e:
                print(e)
                print(url)
                break

    book.set_stylesheet(css_data)
    check_delete_file(new_file)
    book.save(new_file)
    print(book_title + ' complete.')

