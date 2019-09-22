from novels.core.epub_core import *
from novels.core.epub_bd import *
from novels.core.epub_ln import *
from novels.core.epub_qb import *
from novels.core.epub_1k import *
from novels.core.epub_qin import *
from novels.core.epub_wk import *
from novels.tools.rename import *
from novels.tools.translate import *

# ---------------------- Variables -----------------------

# Chapter Pattern
## Numbers
re_number = '[1234567890０１２３４５６７８９0零一二三四五六七八九十百①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳]'
## chapter title split pattern core
chapter_pattern_core = ('((?<=\W)序[幕章言])|((?<=\W)幕间)|((?<=\W)[间终]章)|((?<=\W)最终章)|'
                        '((?<=\W)尾声)|((?<=\W)后记)|((?<=\W)目录)|'
                        '((?<=\W)Epilogue)|((?<=\W)CONTENTS)|((?<=\W)角色介绍)|'
                        '(第\s{0,3}?' + re_number + '{1,5}?\s{0,3}?[章话节])')
## chapter title split pattern
chapter_pattern = '(?im)[^<>]{0,10}?(' + chapter_pattern_core + ')[^<>]{0,20}?(?=<)'

## second chapter title split pattern
second_pattern = '(?<=>)\s*?第?(' + re_number + '{1,2})[节\.]?.*?(?=<)'

# Chapter Length
chapter_length = 200  # get rid of index list in front of a book

# Title Patterns
title_patterns = [('<', '&lt;'), ('>', '&gt;'), ]

# Modify Patterns
modify_patterns = [
    # empty replace
    ('<img(?! src=\"\.\./Images/).*?>', ''),
    ('(&nbsp;)|(\s{2,})|(&#160;)', ''),
    ('(<dt.*?/dt>)|(\[/?img\])', ''),
    ('(一楼给?度娘)|( *惯例占坑。)|( *本话完)|(【草翻】)|(【翻】)|(【翻译】)|(本章未完)|(本章已完)|(本帖最后由)|(下载次数)|(下载附件)|(以下内容由.*?提供)|(【下次.+?】)|(<p.*?>.+?上传</p>)|(<p>.+?(\d+ KB, : \d)</p>)', ''),
    ('(--&gt;\"&gt;)|(\"&gt;)|(<p>=</p>)', ''),
    (r'&gt;&gt;&gt;最全日本轻小说网QinXiaoShuo.com【亲小说】&lt;&lt;&lt;', ''),
    (r'最新最全的日本动漫轻小说 轻小说文库(http://www.wenku8.com) 为你一网打尽！', ''),
    (r'本文来自 轻小说文库(http://www.wenku8.com)', ''),
    # \n replace
    ('<div.*?>', ''),
    ('</div>', '\n'),
    ('(<br.*?>)', '\n'),
    # remove useless tag
    ('<(?!/?(img)|(p)).*?>', ''),
    # remove blank lines
    ('(={2,}?)', ''),
    ('^。\n', ''),
    ('\n{2,}', '\n'),
    # add <p> tag
    ('^(?!<p>)', '<p>'),
    ('(?<!</p>)$', '</p>'),
    # replace <p> tag
    ('<p>.*?(<img.+?>.*?)</p>', '<div>\g<1></div>'),
]  # only work with bdtb or lightnovels

# Txt Replacements
txt_replacements = [
    ('\r', '\n'),
    (r'&#160;', ''),
    (r'&nbsp;', ''),
    ('<', '&gt;'),
    ('>', '&lt;'),
    ('^(?!<p>)', '<p>'),
    ('(?<!</p>)$', '</p>'),
    ('<p></p>\n', ''),
]

css_data = '''h1,h2,div{text-align: center}
p{text-indent: 2em}'''

# Files and Folder
download_folder = '/Volumes/Storage/Downloads/'

def epub_make(uris='', book_title='', folder=download_folder, chapter_check=False, second_check=False, chapter_pattern=chapter_pattern, second_pattern=second_pattern, modify_patterns=modify_patterns, chapter_length= chapter_length, time_stamp=True):

    # Prepare New Book
    if isinstance(uris, str):   # Turn string into list of uris
        uris = [uris]

    image_count = 0
    max_retries = 1
    book = ''

    # Work on list of uris
    for n, uri in enumerate(uris):

        for retries in range(max_retries):
            t0 = datetime.now()

            try:
                # Url
                if re.match(re.compile('http'), uri):
                    url = uri
                    print(url)

                    # First: dealing with the first url
                    ## Baidu Tieba
                    if re.search(re.compile('tieba'), url):
                        _ = Tieba(url)

                    ## Light Masiro
                    elif re.search(re.compile('(lightnovel)|(masiro)'), url):
                        _ = Light(url)

                    ## QianBi
                    elif re.search(re.compile('23qb'), url):
                        _ = QB23(url)

                    ## Wenku8
                    elif re.search(re.compile('wenku8'), url):
                        _ = WK8(url)

                    ## QinXiaoShuo
                    elif re.search(re.compile('qinxiaoshuo'), url):
                        _ = Qin(url)

                    else:
                        print('Url Error')
                        quit()

                    # Second: make the book and get pages from url list
                    ## Make Book
                    if n == 0:
                        ### the url is a book url
                        if _.book_check:
                            _.get_book_info()
                            if book_title == '':
                                book_title = _.book_title
                            book = mkepub.Book(title=book_title)
                            if _.cover_src != '':
                                set_cover_src(book, _.cover_src)

                        ### the url is a page url
                        else:
                            title, content, srcs = _.get_page_content(url)
                            if book_title == '':
                                book_title = title
                            book = mkepub.Book(title=book_title)
                            if srcs != []:
                                set_cover_src(book, srcs[0])

                        _.driver

                        print(book_title)

                    ## Get Pages
                    book = get_pages(_, book, image_count, chapter_check, second_check, chapter_pattern, second_pattern, chapter_length, modify_patterns)

                    _.quit()

                # Files
                if re.match(re.compile('/.+?/.+'), uri):

                    ## Variables
                    file = uri
                    folder = '/'.join(file.split('/')[:-1])
                    path, type = file.split('.')

                    ## Make Book
                    if n == 0:
                        if book_title == '':
                            book_title = (file.split('/')[-1]).split('.')[0]
                        if re.search('\s\d{8}$', book_title):
                            book_title = book_title[:-9]
                        book = mkepub.Book(title=book_title)
                        print(book_title)

                    ## Txt, Zip file
                    if type in ['zip', 'txt']:
                        book = get_txt(book, file, chapter_check, second_check, chapter_pattern, second_pattern, chapter_length)

                    ## Epub file
                    elif type == 'epub':
                        book = get_epub(book, n, file, image_count)

                print('Using time: ', datetime.now()-t0)
                break

            except Exception as e:
                print(e)
                book, retries = get_errors(book, n, uri, retries)

    complete_book(book, book_title, folder, time_stamp)

def get_pages(_, book, image_count=0, chapter_check=False, second_check=False, chapter_pattern=chapter_pattern, second_pattern=second_pattern, chapter_length=chapter_length, modify_patterns=modify_patterns):

    ## Get Url List
    if _.book_check:
        url_list = _.get_url_list()
        print('This is a book.')
    else:
        url_list = [(_.url, '', '')]
        print('This is a page.')

    ## Get Pages
    content_check = ''
    for url, name, date in url_list:
        title, content, srcs = _.get_page_content(url)
        while content == content_check:
            print('Same Page.')
            title, content, srcs = _.get_page_content(url)
        content_check = content

        if srcs != []:
            content, image_count = download_replace(url, srcs, content, book, image_count)
        content = convert_chinese(content)
        content = modify_content(content)

        # Split Chapters
        if chapter_check:
            chapters = split_chapters(title, content, chapter_pattern=chapter_pattern, second_pattern=second_pattern, chapter_length=chapter_length, second_check=second_check)
            addChapter(book, chapters)

        # One Chapter
        else:
            # modify content before add pages to keep most information for former actions
            content = modify_content(content, modify_patterns)
            book.add_page(title=title, content='<h1>{}</h1>\n'.format(title) + content)

    return book


def get_txt(book, file, chapter_check, second_check, chapter_pattern, second_pattern, chapter_length):
    path, type = file.split('.')
    txt_codes = ['utf-8', 'gbk', 'utf-16']
    txt_list = []

    ## Read TXT
    ### get txt file list
    if type == 'zip':
        unzipfile(file, path)
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.split('.')[-1] == 'txt':
                    txt_list.append(os.path.join(root, file))

    elif type == 'txt':
        txt_list.append(file)
    print(txt_list)

    ### read txt files
    for txt_file in txt_list:
        title = convert_chinese(txt_file.split('/')[-1].split('.')[0])
        content = read_txt(txt_file, codes=txt_codes)
        print(title)

        ### add pages
        if chapter_check:
            chapters = split_chapters(title, content, chapter_pattern=chapter_pattern, second_pattern=second_pattern,
                                      chapter_length=chapter_length, second_check=second_check)
            addChapter(book, chapters)

        else:
            # One Chapter
            # modify content before add pages to keep most information for former actions
            content = modify_content(content, modify_patterns)
            book.add_page(title=title, content='<h1>{}</h1>\n'.format(title) + content)

    return book


def get_epub(book, n, file, image_count=0):
    path, type = file.split('.')

    ### read epub file
    title_content_list, image_list = read_epub(file)

    ### add chapters
    for title, content in title_content_list:
        title = convert_chinese(title)
        content = convert_chinese(content)
        book.add_page(title=title, content=content)

    ### add images
    if image_list != {}:
        for name, image in image_list.items():

            # add cover
            if n == 0 and name.split('.')[0] == 'cover':
                book.set_cover(image)

            # add images
            else:
                book.add_image(name, image)

    image_count += len(image_list)

    ### remove unzip folder
    rmtree(path)

    return book


def get_errors(book, n, uri, retries):
    if retries == 3:
        ## Make Book
        if n == 0:
            book_title = 'Unknown {}'.format(str(n))
            book = mkepub.Book(title=book_title)
            print(book_title)
        book.add_page(title='Error {0}'.format(str(n)),
                      content='<h1>Error {0}</h1><a href="{1}">{1}</a>\n'.format(str(n), uri))
        return book, retries
    else:
        print('Try again: {}'.format(str(retries + 1)))
        return book, retries
        pass


def complete_book(book, book_title, folder, time_stamp=True):
    # CSS
    book.set_stylesheet(css_data)

    if time_stamp:
        epub_name = book_title + ' ' + time.strftime('%m%d%H%M') + '.epub'
    else:
        epub_name = book_title + '.epub'

    epub_file = os.path.join(folder, epub_name)

    check_delete_file(epub_file)

    book.save(epub_file)

    # Output Result
    print(book_title + ' complete.')
    print(epub_file)



