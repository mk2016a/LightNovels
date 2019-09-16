from novels.core.epub_core import *
from novels.core.epub_bd import *
from novels.core.epub_ln import *
from novels.core.epub_qb import *
from novels.core.epub_1k import *
from novels.core.epub_qin import *
from novels.core.epub_wk import *
from novels.tools.rename import *
from novels.tools.translate import *

download_path = '/Volumes/Storage/Downloads/'

# Tieba

def get_tieba(url):
    ## Get Content
    _ = BDTB(url)
    book_check = False
    url_list = [url]

        return _,  book_check, url_list, cover_src


def get_light(url):
    _ = LightNovel(url)
    
    ## This is a Page.
    if re.search(re.compile('mod=viewthread'), url):
        book_check = False
        url_list = [url]
        if n == 0:
            ### get title
            title, content, srcs = _.get_page_content(url)
            ### set title
            if book_check == '':
                book_check = title
                
    ## This is a Book.
    elif re.search(re.compile('mod=forumdisplay'), url):
        book_check = True
        title, url_list = _.get_title_index()

    cover_src = ''
    return _,  book_check, url_list, cover_src

def get_qb(url):
    ## Make the new class variable.
    _ = QB23(url)

    ## This is a Page.
    if re.search(re.compile('\.html'), url):
        book_check = False
        url_list = [url]
        if n == 0:
            ### get title
            title, content, srcs = _.get_page_content(url)
            ### set title
            if book_check == '':
                book_check = title
            cover_src = ''

    ## This is a Book.
    else:
        book_check = True
        ### get index
        _.getTitleIndex()
        url_list = _.index
        ### set title
        if n == 0 and book_check == '':
            book_check = _.title
            cover_src = _.cover_src
            
    return _,  book_check, url_list, cover_src

def get_wenku8(url):
    ## Make the new class variable.
    _ = WK8(url)

    ## This is a Page.
    if re.search(re.compile('/novel/'), url):
        book_check = False
        url_list = [url]
        if n == 0:
            ### get title
            title, content, srcs = _.get_page_content(url)
            ### set title
            if book_check == '':
                book_check = title
            cover_src = ''

    ## This is a Book.
    elif re.search(re.compile('/book/'), url):
        book_check = True
        ### get index
        _.getTitleIndex()
        url_list = _.index
        ### set title
        if n == 0 and book_check == '':
            book_check = _.title
            cover_src = _.cover_src
            
    return _,  book_check, url_list, cover_src

def get_qin(url):
    ## Make the new class variable.
    _ = Qin(url)

    ## This is a Page.
    if re.search(re.compile('/read/'), url):
        book_check = False
        url_list = [url]
        if n == 0:
            ### get title
            title, content, srcs = _.get_page_content(url)
            ### set title
            if book_check == '':
                book_check = title
            cover_src = ''

    ## This is a Book.
    elif re.search(re.compile('/book/'), url):
        book_check = True
        ### get index
        _.getTitleIndex()
        url_list = _.index
        ### set title
        if n == 0 and book_check == '':
            book_check = _.title
            cover_src = _.cover_src
    return _,  book_check, url_list, cover_src


def get_pages(_, book, image_count=0, chapter_check=False, second_check=False, chapter_pattern=chapter_pattern, second_pattern=second_pattern, chapter_length=chapter_length, modify_patterns=modify_patterns):

    url_list = _.url_list

    ## Get Pages
    content_check = ''
    for url in url_list:
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


        book.add_page(title=title, content='<h1>{}</h1>\n'.format(title) + content)

    return book

## make book with book_title, download content and images from url_list into the book

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


download_folder = '/Volumes/Storage/Downloads/'


def epub_make(uris='', book_title='', folder=download_folder, chapter_check=False, second_check=False,
              modify_check=False, chapter_pattern=chapter_pattern, second_pattern=second_pattern,
              modify_p=modify_patterns, chapter_length=chapter_length, time_stamp=True):
    # Prepare New Book
    if isinstance(uris, str):  # Turn string into list of uris
        uris = [uris]

    image_count = 0
    max_retries = 1
    book = ''

    # Work on list of uris
    for n, uri in enumerate(uris):

        for retries in range(max_retries):
            t0 = datetime.now()

            # try:
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

                    print(book_title)