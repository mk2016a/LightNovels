# Common
import os
import re
import time
from datetime import datetime

# Urllib
import ssl
import urllib
from urllib.parse import urljoin
from urllib.request import urlopen
import urllib.error
import socket

# Beautiful Soup
import requests
from bs4 import BeautifulSoup

# Json
import json

# Threads
import threading
import queue

# Zip Folder
import zipfile
from shutil import rmtree

# Open Chinese Convert
from opencc import OpenCC

# Make Epub
import mkepub

# ---------------------- Beautiful Soup -----------------------

# Chapter Pattern
## Numbers
re_number = '[1234567890０１２３４５６７８９0零一二三四五六七八九十百①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳]'
## chapter title split pattern core
chapter_pattern_core = ('((?<=\W)序[幕章言])|((?<=\W)幕间)|((?<=\W)[间终]章)|((?<=\W)最终章)|'
                        '((?<=\W)尾声)|((?<=\W)后记)|((?<=\W)目录)|'
                        '((?<=\W)Epilogue)|((?<=\W)CONTENTS)|((?<=\W)角色介绍)|'
                        '(第\s{0,3}?'+re_number+'{1,5}?\s{0,3}?[章话节])')
## chapter title split pattern
chapter_pattern = '(?im)[^<>]{0,10}?('+chapter_pattern_core+')[^<>]{0,20}?(?=<)'

## second chapter title split pattern
second_pattern = '(?<=>)\s*?第?('+re_number+'{1,2})[节\.]?.*?(?=<)'

# Chapter Length
chapter_length = 500    # get rid of index list in front of a book

# Ocr Length
ocr_length = 200        #  get rid of picture with few words being recognized

# Modify Patterns
modify_patterns = [
    # empty replace
    ('<img(?! src="\.\./Images/\d{4}\.(jpg)|(gif)|(png)").*?>', ''),
    ('(&nbsp;)|(\s{2,})|(&#160;)', ''),
    ('(<dt.*?/dt>)|(\[/?img\])',''),
    ('(一楼给?度娘)|( *惯例占坑。)|( *本话完)|(【草翻】)|(【翻】)|(【翻译】)|(本章未完)|(本章已完)', ''),
    ('<.*?((本帖最后由)|(下载次数)|(下载附件)|(上传)).*?>',''),
    ('(以下内容由.*?提供)|(={2,}?)|(【下次.+?】)',''),
    ('<p>=</p>',''),
    ('(--&gt;\"&gt;)|(\"&gt;)',''),
    (r'&gt;&gt;&gt;最全日本轻小说网QinXiaoShuo.com【亲小说】&lt;&lt;&lt;', ''),
    (r'最新最全的日本动漫轻小说 轻小说文库(http://www.wenku8.com) 为你一网打尽！', ''),
    (r'本文来自 轻小说文库(http://www.wenku8.com)', ''),
    # \n replace
    ('<div.*?>', ''),
    ('</div>','\n'),
    ('(<br.*?/?>)', '\n'),
    ('\n{2,}', '\n'),
    # remove useless tag
    ('<(?!/?(img)|(p)).*?>', ''),
    # add <p> tag
    ('^(?!<p>)', '<p>'),
    ('(?<!</p>)$', '</p>'),
    # replace <p> tag
    ('<p>.*?(<img.+?>.*?)</p>', '<div>\g<1></div>'),
]# only work with bdtb or lightnovels

# Ocr Repairs
ocr_repair = [
    # add <p> tag
    ('^[fr」T\[]', '「'),
    ('[JT1「\]]$', '」'),
    ('(\.\.\.…\.)|(\.……)|(\.\.…\.)|(\.\.\.\.)|(……\.)', '……'),
    ('(—一)|(一-)|(一—)|(一一)', '——'),
    ('^([^「].+?」)', '「\g<1>'),
    ('(「.+?[^」])$', '\g<1>」'),
    (r'<', '&#60;'),
    (r'>', '&#62;'),
    ('(^」)|', ''),
    ('([^<>]+?[^\.。\?？！“\”\"：』，——~――、\)）〕」】 》\]…-])\n(?![“《『\"\[])', '\g<1>')*5,
]

# Regular Expression String to Pattern Replacements
reg_replace = [
    ('.', '\.'),
    ('?', '\?'),
    ('(', '\('),
    (')', '\)'),
    ('[', '\['),
    (']', '\]'),
    ('"', '\"'),
    ("'", '\''),
    ('\\', '\\\\'),
]

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

download_dir = '/Volumes/Storage/Downloads/'

#               Common Tools

# Beautiful Soup
def bsoup(url, code='utf-8'):
    resources = requests.get(url).content.decode(code)
    soup = BeautifulSoup(resources, "html.parser")
    return soup

# Convert Traditional Chinese to Simplified
def convert_chinese(content):
    content = OpenCC('t2s').convert(content)
    return content

def translate_html(html_path):
    with open(html_path, 'r') as f:
        f_content = convert_chinese(f.read())
        f.close()
    with open(html_path, 'w+') as f:
        f.write(f_content)
        f.close()

# Check and Make directory
def check_make_dir(dir):
    if not os.path.isdir(dir):
        os.makedirs(dir)

# Check and Delete file
def check_delete_file(file):
    if os.path.isfile(file):
        os.remove(file)

# Check Update
def get_local_date(title, folder):
    local_date = datetime.fromtimestamp(0)
    for root, dirs, files in os.walk(folder):
        for file in files:
            if re.match(re.escape(title), file):
                path = root + '/' + file
                date = datetime.fromtimestamp(os.path.getmtime(path))
                if date > local_date:
                    local_date = date
    return local_date

# Replace <img>
def replace_url(url, replacement, content):
    url = re.escape(url)
    return re.sub(url, replacement, content)

def replace_img(src, replacement, content):
    return re.sub('<img[^<]*?{}[^>]*?>'.format(src), replacement, content)
#replace_img = lambda src, replacement, content: re.sub('<img[^<]*?{}[^>]*?>'.format(src), replacement, content)

# Read Image
def read_image(q, image_name, image_url, out_time = 60, try_max = 10):
    image = ''
    try_times = 1
    while try_times <= try_max:
        try:
            context = ssl._create_unverified_context()
            image = urlopen(image_url, context=context, timeout=out_time).read()
            try_times = try_max + 1

        except socket.timeout as e:
            print('Try again.')
            time.sleep(2)
            try_times += 1

        except urllib.error.HTTPError as e:
            print(e)
            # if e.code == 403
            print(image_url)
            try_times = try_max + 2
            #image = '403'

    if try_times == try_max + 2:
        print('Error picture:',image_name, image_url)

    q.put((image_name, image))

# Name Number
def number_name(n, length=4):
    name = (length-len(str(n)))*'0' + str(n)
    return name

# Get All Images with OCR
def download_replace(url, image_srcs, content, book, image_count=0, ocr_check=False, max_threads=4):
    imgs = []  # list of ReadImage
    m = max_threads  # Limit of threads' number
    q = queue.PriorityQueue()
    threads = []

    for n, src in enumerate(image_srcs):
        # url
        image_url = urllib.parse.urljoin(url, src)
        # ocr
        if ocr_check:
            ocr_content = content_ocr(image_url)
            if ocr_content:
                content = replace_img(re.escape(src), '\g<0>\n'+ocr_content, content)
                print('ocr: {}'.format(src))
        # name
        img_number = image_count + n + 1
        print(img_number)
        if src.split('.')[-1] == 'gif':
            image_name = number_name(img_number) + '.gif'
        elif src.split('.')[-1] == 'png':
            image_name = number_name(img_number) + '.png'
        else:
            image_name = number_name(img_number) +'.jpg'
        # tag
        content = replace_img(re.escape(src), '<div><img src="../Images/{0}"/></div>\n'.format(image_name), content)

        # limit thread number
        while threading.active_count() > m:
            time.sleep(0.1)
        # add read thread
        print(image_name + ': ' + image_url)
        t = threading.Thread(target=read_image, args=(q, image_name, image_url),
                             daemon=True)  # args=(q,) always end with a commar for args
        threads.append(t)
        t.start()

    # wait for threads finished
    for t in threads:
        t.join()

    while not q.empty():
        _ = q.get()
        imgs.append(_)

    # Add and Retrieve Image
    for (image_name, image) in imgs:
        if image != '':
            book.add_image(image_name, image)

    image_count = img_number
    print(image_count)

    return content, image_count

# Set Cover
def set_cover_src(book, image_url, out_time=60, try_max = 4):
    try_times = 1
    while try_times <= try_max and image_url != '':
        try:
            image = urlopen(image_url, timeout=out_time).read()
            book.set_cover(image)
            print('Cover Setted.')
            try_times = try_max + 1
        except Exception as e:
            print('Error02')
            print('Cover unsetted. Try again. ')
            try_times += 1


# Optical Character Recognition
def ocr(src):
    ocr_url = 'http://pic.sogou.com/pic/ocr/ocrOnline.jsp?query=' + src
    ocr_resources = requests.get(ocr_url).content
    ocr_json = json.loads(ocr_resources)
    return ocr_json

def content_ocr(src_url, ocr_repairs=ocr_repair, ocr_l=ocr_length):
    try:
        ocr_json = ocr(src_url)
        if ocr_json["success"] == 1:
            ocr_content = ''
            for ocr_content_json in ocr_json["result"]:
                ocr_content += ocr_content_json["content"]
            if len(ocr_content) > ocr_l:
                for ocr_repair in ocr_repairs:
                    ocr_content = re.sub(ocr_repair[0], ocr_repair[1], ocr_content, flags=re.M)
            else:
                ocr_content = False
        else:
            ocr_content = False
    except Exception as e:
        print('OCR Error')
        ocr_content = False
    return ocr_content

# Modify Content
def modify_content(content, modify_p=modify_patterns):
    for (old, new) in modify_p:
        content = re.sub(old, new, content, flags=re.M)
    return content

# Splite Chapters
def split_chapters(title, content, chapter_pattern=chapter_pattern, chapter_length=chapter_length, second_pattern=second_pattern, second_length=0, second_check=False):

    if not second_check:
        chapter = single_split(title, content, chapter_pattern=chapter_pattern, chapter_length=chapter_length)
    else:
        chapter = double_split(title, content, first_p=chapter_pattern, second_p=second_pattern, first_l=chapter_length, second_l=second_length)
    print(chapter)
    return chapter

## single split chapter
def single_split(title, content, chapter_pattern=chapter_pattern, chapter_length=chapter_length):

    if re.search(chapter_pattern, content, flags=re.M):

        finditer_result = re.finditer(chapter_pattern, content, flags=re.M)
        # print(finditer_result)       <callable_iterator object at 0x10c6373c8>

        chapters = []
        chapter_title = title
        infront_img = ''
        begining = 0
        before_check = True

        for n, match_result in enumerate(finditer_result):
            print(match_result)

            # get the split content end position from this match's begining
            this_end = match_result.start()      # end for this chapter
            next_title = match_result.group().strip(' \n\r\t')       # title for next chapter
            # the end of this chapter is the begining of new chapter title's start
            # when this chapter is long enough
            if this_end - begining >= chapter_length and before_check:
                # get chapter image infront
                ## this image from last chapter
                if infront_img != '':
                    chapter_content = content[infront_img.start():this_end]
                else:
                    chapter_content = content[begining:this_end]
                ## next chapter's infront image
                if infront_img != '':
                    chapter_content = infront_img + chapter_content
                    infront_img = ''
                search_results = re.search(re.compile('<img.+?>.{0, 100}$'), chapter_content)
                if search_results != None:
                    infront_img = search_results[-1]
                else:
                    infront_img = ''

                # append chapter to chapters
                chapters.append((chapter_title, chapter_content))

                # after append, next chapter's new beginning and title
                begining = match_result.end()
                chapter_title = next_title

            elif this_end - begining >= chapter_length and before_check == False:
                # last chapter
                last_content = content[begining : last_end]
                chapters.append((chapter_title, last_content))
                # this chapter
                chapter_content = content[last_end : this_end]
                chapters.append((this_title, chapter_content))
                # after twice append
                before_check = True
                begining = match_result.end()
                chapter_title = next_title
            else:
                before_check = False
                # for the next result, keep last ending and this title
                last_end = this_end
                this_title = next_title


                # the chapter title will stay the same
                # there will be no chapter content until next loop
                # the beginning will stay the same
                # the end will be new end in next loop
                # the short result will be added in front

           # the first match result's start is 0

        # after all loops ended, begining is last match'es end
        #chapter_content = modify_content(content[begining:])
        chapter_content = content[begining:]
        # chapters will append the last match's title and content
        chapters.append((chapter_title, chapter_content))

    else:
    # if can not being splited
        chapters = [(title, content)]

    return chapters


## Double Split Chapters
def double_split(title, content, first_p=chapter_pattern, second_p=second_pattern, first_l=chapter_length, second_l=0):
    chapters = []
    first_chapters = single_split(title, content, first_p, chapter_length=first_l)
    if first_chapters != []:
        for first_title, first_content in first_chapters:
            second_chapters = single_split(first_title, first_content, chapter_pattern=second_p, chapter_length=second_l)
            if second_chapters:
                chapters.append((first_title, second_chapters))
            else:
                chapters.append((first_title, first_content))
    else:
        chapters.append((title, content))
    return chapters


# Add Chapters
def addChapter(book, chapters, modify_patterns=modify_patterns):

    for title, content in chapters:
        title = modify_content(title, modify_patterns)
        # content is a string
        if isinstance(content, str):
            content = modify_content(content, modify_patterns)
            book.add_page(title=title, content='<h1>{}</h1>\n'.format(title) + content)
        # content is a list of titles and contents
        if isinstance(content, list):
            content1 = modify_content(content[0][1], modify_patterns)
            first = book.add_page(title=title, content='<h1>{}</h1>\n'.format(title) + content1)
            for title2, content2 in content[1:]:
                title2 = modify_content(title2, modify_patterns)
                content2 = modify_content(content2, modify_patterns)
                book.add_page(title=title2, content='<h2>{}</h2>\n'.format(title2) + content2, parent=first)


# Read Txt

def modify_txt(content, replacements=txt_replacements):
    for (old, new) in replacements:
        content = re.sub(old, new, content, flags=re.M)
    return content

def read_txt(file, codes=['utf-8', 'gbk', 'utf-16']):
    if isinstance(codes, str):
        codes = [codes]
    for code in codes:
        try:
            with open(file, 'r', encoding=code) as f:
                content = f.read()
                content = modify_txt(content)
                content = convert_chinese(content)
                break
        except Exception as e:
            pass
    return content


# Read Epub
def unzipfile(zip_path, dst_path):
    zf = zipfile.ZipFile(zip_path, 'r')
    zf.extractall(dst_path)
    zf.close()

def unzip_epub(path):
    # unzip epub files
    #   rename epub to zip
    file = path + '.epub'
    zip_path = path + '.zip'
    os.rename(file, zip_path)
    #   extract zip
    unzipfile(zip_path, path)
    os.rename(zip_path, file)

def get_file_paths(root_path, file_types):
    file_paths = []
    for root, dirs, files in os.walk(root_path):
        for file in files:
            try:
                if file.split('.')[-1] in file_types:
                    file_paths.append(os.path.join(root, file))
            except IndexError:
                print('Error03')
                pass
    return file_paths

def read_opf(path):  # to correct order of files
    # Read XML
    unzip_epub(path)
    for root, folders, files in os.walk(path):
        for file in files:
            file_type = file.split('.')[-1]
            if file_type == 'opf':
                dir = root
                opf_file = root + '/' + file
                break
    opf = open(opf_file).read()
    soup = BeautifulSoup(opf, 'xml')

    manifest_list = {}
    manifest = soup.find('manifest')
    items = manifest('item')
    for item in items:
        manifest_list[item['id']] = item['href']

    itemref_list = []
    spine = soup.find('spine')
    itemrefs = spine('itemref')
    for itemref in itemrefs:
        value = manifest_list[itemref['idref']]
        if not re.search('(cover\.xhtml)|(toc\.xhtml)|(nav\.xhtml)', value, flags=re.IGNORECASE):
            print(value)
            itemref_list.append(os.path.join(dir, value))
    # print(itemref_list)
    return itemref_list

def read_epub(file):    # read xhtml files and get content
    # Get Titles and Contents
    path = file.split('.')[0]
    title_content_list = []
    itemref_list = read_opf(path)
    for itemref in itemref_list:
        xhtml = itemref
        with open(xhtml) as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            title = soup.find('title').text
            if len(title)<3:
                if soup.find('h1'):
                    title = soup.find('h1').text
                elif soup.find('h2'):
                    title = soup.find('h2').text
            print(title)
            content = str(soup.find('body'))[6:-7]
            print(content)
            title_content_list.append((title, content))
    # Get Images
    images = {}
    for root, folders, files in os.walk(path):
        for file in files:
            if file.split('.')[-1] in ['gif', 'jpg', 'png', 'jpeg']:
                with open(root+'/'+file, 'rb') as f:
                    image = f.read()
                images[file]=image

    return title_content_list, images

# Modify chapter content
'''
                if infront_img != '':
                    chapter_content = infront_img + chapter_content
                    infront_img = ''
                search_results = re.search('<img.+?>.{0,20}$', chapter_content)
                if search_results != None:
                    infront_img = search_results[0]
                    chapter_content = chapter_content[:search_results.start()]
'''

# EPUB CSS
def addCSS(book, css=css_data):
    book.set_stylesheet(css)

# ---------------------- Selenium Driver ----------------------

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from datetime import datetime

def set_driver():
    # Prepare Firefox
    ## firefox profile
    caps = DesiredCapabilities().FIREFOX
    caps["pageLoadStrategy"] = "none"  # none, eager, normal
    fp = webdriver.FirefoxProfile('/Users/mk/Library/Application Support/Firefox/Profiles/wn1jjo27.default')
    fp.set_preference('network.proxy.type', 1)  # proxy
    fp.set_preference('network.proxy.http', '127.0.0.1')
    fp.set_preference('network.proxy.http_port', '8087')
    fp.set_preference('network.proxy.type', 0)  # direct
    opts = webdriver.FirefoxOptions()
    #opts.headless = True
    ##  open firefox
    driver = webdriver.Firefox(firefox_profile=fp, capabilities=caps, options=opts)
    return driver

# Wait for Loading
def wait_loading(driver, sleep_seconds=600, max_wait_time=900):
    wait_time = 0
    t1 = datetime.now()
    ## wait before loading
    while driver.execute_script('return document.readyState;') == 'complete' and wait_time < sleep_seconds:
        time.sleep(0.1)
        wait_time += 0.1
    ## wait for loading
    while driver.execute_script('return document.readyState;') != 'complete' and wait_time < max_wait_time:
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        except:
            pass
        time.sleep(0.1)
        wait_time += 0.1
    ## calculate waiting time
    t2 = datetime.now()
    print(t2 - t1)
    print('Load Complete.')

# Check next page
def next_page(driver, link_text):
    try:
        next_page = driver.find_element_by_link_text(link_text)
        next_page.click()
        wait_loading(driver)
        return True
    except:
        return False