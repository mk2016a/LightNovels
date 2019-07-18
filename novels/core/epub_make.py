from novels.core.epub_core import *
from novels.core.epub_bd import *
from novels.core.epub_ln import *
from novels.core.epub_qin import *
from novels.core.epub_1k import *
from novels.core.epub_qb import *
from novels.core.epub_wk import *
#from novels.core.epub_zb import *
#from novels.bin.epub_qb import *
#from novels.bin.epub_txt import *
from novels.tools.rename import *
from novels.tools.translate import *

download_path = '/Volumes/Storage/Downloads/'


# Epub Append
def epub_make(uris='', book_title='', folder='', chapter_check=False, second_check=False, modify_check=False, chapter_pattern=chapter_pattern, second_pattern=second_pattern, modify_p=modify_patterns, chapter_length= chapter_length, txt_codes=['utf-8', 'gbk', 'utf-16'], time_stamp=True):
    # Prepare New Book
    print('Making Epub...')
    book = mkepub.Book(title=book_title)
    image_count = 0
    # Turn string into list of uris
    if isinstance(uris, str):
        uris = [uris]

    # Work on list of uris
    for n, uri in enumerate(uris):

        # Url
        if re.match('http', uri):
            url = uri
            print(url)
            if re.search('(masiro)|(lightnovel)|(tieba)', url):

                # Content(simplify Chinese)
                if re.search('tieba', url):

                    ## Get Content
                    bdtb = BDTB(url)
                    url, srcs, title, content = bdtb.getContent()

                    ## Make Book
                    if n == 0:
                        if book_title=='':
                            book_title = title
                        book = mkepub.Book(title=book_title)
                        file_name = book_title + 'tb'
                        print(book_title)

                    ## Download Images
                    if srcs != []:
                        content, image_count = download_replace(url, srcs, content, book, image_count, ocr_check=True)
                elif re.search('(masiro)|(lightnovel)', url):

                    ## Get Content
                    light = LightNovel(url)
                    url, srcs, title, content = light.getContent()

                    ## Make Book
                    if n == 0:
                        if title != '' and book_title=='':
                            book_title = title
                        book = mkepub.Book(title=book_title)
                        file_name = book_title + ' ln'
                        print(book_title)

                    ## Download Images
                    if srcs != []:
                        content, image_count = download_replace(url, srcs, content, book, image_count)

                # Convert Simplify Chinese
                content = convert_chinese(content)

                # Modify Content before Split Chapters
                if modify_check:
                    content = modify_content(content)

                # Split Chapters
                if chapter_check:
                    chapters = split_chapters(title, content, chapter_pattern=chapter_pattern, second_pattern=second_pattern, chapter_length=chapter_length, second_check=second_check)
                    addChapter(book, chapters)

                # One Chapter
                else:
                    # modify content before add pages to keep most information for former actions
                    content = modify_content(content)
                    book.add_page(title=title, content='<h1>{}</h1>\n'.format(title) + content)

                # add cover
                if n == 0 and srcs != []:
                    set_cover_src(book, srcs[0])

            elif re.search('(qinxiaoshuo)|(wenku8)', url):

                if re.search('wenku8', url):

                    ## Make the new class variable.
                    _ = WK8(url)

                    ## url is a page
                    if re.search('/novel/',url):
                        url_list = [url]
                        if n == 0:
                            ### get title
                            title, content, srcs = _.get_page_content(url)
                            ### set title
                            if book_title == '':
                                book_title = _.title
                            cover_src = ''

                    ## url is a book
                    elif re.search('/book/', url):

                        ### get index
                        _.getTitleIndex()
                        url_list = _.index

                        ### set title
                        if n == 0 and book_title=='':
                            book_title = _.title
                            cover_src = _.cover_src

                    ## Make Book
                    if n == 0:
                        book = mkepub.Book(title=book_title)
                        file_name = book_title + ' wk'
                        print(book_title)

                    ## get pages
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
                        book.add_page(title=title, content='<h1>{}</h1>\n'.format(title) + content)

                ## Open Driver
                elif re.search('qinxiaoshuo', url):

                    ## Make the new class variable.
                    _ = Qin(url)

                    ## url is a page
                    if re.search('/read/', url):
                        url_list = [url]
                        if n == 0:
                            ### get title
                            title, content, srcs = _.get_page_content(url)
                            ### set title
                            if book_title == '':
                                book_title = _.title
                            cover_src = ''

                    ## url is a book
                    elif re.search('/book/', url):

                        ### get index
                        _.getTitleIndex()
                        url_list = _.index

                        ### set title
                        if n == 0 and book_title=='':
                            book_title = _.title
                            cover_src = _.cover_src

                    ## Make Book
                    if n == 0:
                        book = mkepub.Book(title=book_title)
                        file_name = book_title + ' qin'
                        print(book_title)


                    ## get pages
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
                        book.add_page(title=title, content='<h1>{}</h1>\n'.format(title) + content)


                ## Quit Driver
                _.quit()

                ## Set Cover
                set_cover_src(book, cover_src)

        # Files
        elif re.match('/.+/.+', uri):

            ## Variables
            file = uri
            folder = '/'.join(file.split('/')[:-1])
            path, type = file.split('.')
            txt_list = []

            ## Make Book
            if n == 0:
                if book_title == '':
                    book_title = path.split('/')[-1]
                book = epub_make(book_title=book_title)

            ## Name File
            file_name = book_title

            ## Txt, Zip file
            if type in ['zip', 'txt']:

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
                    print(content)

                    ### add pages
                    if chapter_check:
                        chapters = split_chapters(title, content, chapter_pattern=chapter_pattern,second_pattern=second_pattern, chapter_length=chapter_length,second_check=second_check)
                        addChapter(book, chapters)

                    else:
                        # One Chapter
                        # modify content before add pages to keep most information for former actions
                        content = modify_content(content, modify_patterns)
                        book.add_page(title=title, content='<h1>{}</h1>\n'.format(title) + content)

            ## Epub file
            elif type == 'epub':

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
                        if name.split('.')[0] == 'cover' and n == 0:
                            book.set_cover(image)
                        # add images
                        else:
                            book.add_image(name, image)
                image_count += len(image_list)

                ### remove unzip folder
                rmtree(path)

    # Save Epub
    if folder == '':
        folder = '/Volumes/Storage/Downloads/'

    if time_stamp:
        epub_name = file_name + ' ' + time.strftime('%m%d%H%M') + '.epub'

    epub_file = os.path.join(folder, epub_name)
    book.set_stylesheet(css_data)
    check_delete_file(epub_file)
    book.save(epub_file)

    # Output Result
    print(book_title + ' complete.')
    print(epub_file)

