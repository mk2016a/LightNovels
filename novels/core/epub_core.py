# The core of this


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

# Ocr Length
ocr_length = 200  # get rid of picture with few words being recognized

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
    ('([^<>]+?[^\.。\?？！“\”\"：』，——~――、\)）〕」】 》\]…-])\n(?![“《『\"\[])', '\g<1>') * 5,
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

# Files and Folder
download_dir = '/Volumes/Storage/Downloads/'

def get_file_path(folder, keyword='web'):
    file_date_list = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if re.search(keyword, file, flags=re.IGNORECASE):
                path = os.path.join(root, file)
                date = os.path.getctime(path)
                file_date_list.append((path, date))
    file = sorted(file_date_list, key=lambda line: line[-1], reverse=True)[0][0]
    # file = file_date_list.sort(key=lambda line: line[1], reverse=True)[0]
    # TypeError: 'NoneType' object is not subscriptable ....... not work in 3.6, but work in 3.7 above
    return file


# ---------------------- Beautiful Soup -----------------------

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


# ---------------------- Download Images -----------------------

# Read Image
def read_image(q, image_name, image_url, out_time=60, try_max=10):
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
            # image = '403'

    if try_times == try_max + 2:
        print('Error picture:', image_name, image_url)

    q.put((image_name, image))


# Name Number
def number_name(n, length=4):
    name = (length - len(str(n))) * '0' + str(n)
    return name


# Replace Img with src
def replace_img(src, replacement, content):
    print(src, replacement, sep='\n')
    return re.sub(re.compile('<img[^<]*?{}[^>]*?>'.format(src)), replacement, content)


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
                content = re.sub(re.escape(src), '\g<0>\n' + ocr_content, content)
                print('ocr: {}'.format(src))
        # name
        img_number = image_count + n + 1
        if src.split('.')[-1] == 'gif':
            image_name = number_name(img_number) + '.gif'
        elif src.split('.')[-1] == 'png':
            image_name = number_name(img_number) + '.png'
        else:
            image_name = number_name(img_number) + '.jpg'
        # tag
        src = re.sub('\&', '&amp;', src.split('/')[-1])
        content = re.sub('<img[^<]*?{}[^>]*?>'.format(re.escape(src)),
                         '<div><img src="../Images/{0}"/></div>\n'.format(image_name),
                         content)

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

    return content, image_count


# Set Cover
def set_cover_src(book, image_url, out_time=60, try_max=3):
    try_times = 1
    while try_times <= try_max and image_url != '':
        try:
            image = urlopen(image_url, timeout=out_time).read()
            book.set_cover(image)
            print('Cover Setted.')
            try_times = try_max + 1
        except Exception as e:
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
                    ocr_content = re.sub(re.compile(ocr_repair[0], flags=re.M), ocr_repair[1], ocr_content)
            else:
                ocr_content = False
        else:
            ocr_content = False
    except Exception as e:
        print('OCR Error')
        ocr_content = False
    return ocr_content


# ---------------------- Modify Title and Content -----------------------

# Modify title
def modify_title(title, modify_p=title_patterns):
    for (old, new) in modify_p:
        title = re.sub(re.compile(old, flags=re.M), new, title)
    return title


# Modify Content
def modify_content(content, modify_p=modify_patterns):
    for (old, new) in modify_p:
        content = re.sub(re.compile(old, flags=re.M), new, content)
    return content


# ---------------------- Split Chapters -----------------------

# Split Chapters
def split_chapters(title, content, chapter_pattern=chapter_pattern, chapter_length=chapter_length,
                   second_pattern=second_pattern, second_length=0, second_check=False):
    if not second_check:
        chapters = single_split(title, content, chapter_pattern=chapter_pattern, chapter_length=chapter_length)
    else:
        chapters = double_split(title, content, first_p=chapter_pattern, second_p=second_pattern, first_l=chapter_length,
                               second_l=second_length)

    return chapters

## single split chapter
def single_split(title, content, chapter_pattern=chapter_pattern, chapter_length=chapter_length):

    compiled_pattern = re.compile(chapter_pattern, flags=re.M)
    if re.search(compiled_pattern, content):

        finditer_result = re.finditer(compiled_pattern, content)
        # print(finditer_result)       <callable_iterator object at 0x10c6373c8>

        chapters = []
        chapter_title = last_title = title
        chapter_begining = last_begining = 0

        for n, match_result in enumerate(finditer_result):
            print(match_result)

            chapter_end = match_result.start()
            # every time the end of chapter will follow changing to maintain all content
            # the begining remain the same only changes when chapters's last item changes


            if chapter_end - chapter_begining >= chapter_length:

                chapters.append((chapter_title, content[chapter_begining: chapter_end]))

                # After Append
                ## next title, begining
                chapter_title = match_result.group().strip(' \n\r\t')
                chapter_begining = chapter_end

        chapter_content = content[chapter_begining:]
        chapters.append((chapter_title, chapter_content))

    else:
        # if can not being splited
        chapters = [(title, content)]

    return chapters

## single split chapter
def single_split2(title, content, chapter_pattern=chapter_pattern, chapter_length=chapter_length):

    compiled_pattern = re.compile(chapter_pattern, flags=re.M)
    if re.search(compiled_pattern, content):

        finditer_result = re.finditer(compiled_pattern, content)
        # print(finditer_result)       <callable_iterator object at 0x10c6373c8>

        chapters = []
        chapter_title = last_title = title
        chapter_begining = last_begining = 0

        for n, match_result in enumerate(finditer_result):
            print(match_result)

            chapter_end = match_result.start()
            # every time the end of chapter will follow changing to maintain all content
            # the begining remain the same only changes when chapters's last item changes


            if chapter_end - chapter_begining >= chapter_length:

                chapters.append((chapter_title, content[chapter_begining: chapter_end]))

                # After Append

                ## last title, begining
                last_title = chapter_title
                last_begining = chapter_begining        # keep the value of last begining is the key issue.

                ## next title, begining
                chapter_title = match_result.group().strip(' \n\r\t')
                chapter_begining = chapter_end


            else: #chapter_end - chapter_begining < chapter_length:

                if chapter_end - last_begining >= chapter_length:

                    chapters.pop(-1)
                    chapters.append((last_title, content[last_begining: chapter_end]))

                    # After Append

                    # last title, begining
                    # last_title = last_title
                    # last_begining = last_begining
                    # because this time appended last title and last begining content.
                    # last is still the last

                    ## next title, begining
                    chapter_title = match_result.group().strip(' \n\r\t')
                    chapter_begining = chapter_end

                # else:
                # remain the same value for the next result
                # nothing in chapters changed yet
                # last title still the last title, last begining still the last begining
                # because the old title and begining are not used
                # even the next chapter's title and begining will not change to the new one

                # the chapter title will stay the same
                # there will be no chapter content until next loop
                # the beginning will stay the same
                # the end will be new end in next loop
                # the short result will be added in front


        # the first match result's start is 0

        # after all loops ended, begining is last match'es end


        if len(content) - chapter_begining >= chapter_length:
            # when chapter is long enough, no need to change last item
            chapters.append((chapter_title, content[chapter_begining:]))

        else:
            # when chapter is not long enough, pop the last one,
            # and add content from the last begining to the end with last title
            chapters.pop(-1)
            chapters.append((last_title, content[last_begining:]))

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
            second_chapters = single_split(first_title, first_content, chapter_pattern=second_p,
                                           chapter_length=second_l)
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
            second_content = modify_content(content[0][1], modify_patterns)
            first = book.add_page(title=title, content='<h1>{}</h1>\n'.format(title) + second_content)
            for title2, second_content in content[1:]:
                title2 = modify_content(title2, modify_patterns)
                second_content = modify_content(second_content, modify_patterns)
                book.add_page(title=title2, content='<h2>{}</h2>\n'.format(title2) + second_content, parent=first)


# Read Txt

def modify_txt(content, replacements=txt_replacements):
    for (old, new) in replacements:
        content = re.sub(re.compile(old, flags=re.M), new, content)
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
    opf = open(opf_file, encoding='utf-8').read()
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
        if not re.search(re.compile('(cover\.xhtml)|(toc\.xhtml)|(nav\.xhtml)', flags=re.IGNORECASE), value):
            print(value)
            itemref_list.append(os.path.join(dir, value))
    # print(itemref_list)
    return itemref_list


def read_epub(file):  # read xhtml files and get content
    # Get Titles and Contents
    path = file.split('.')[0]
    title_content_list = []
    itemref_list = read_opf(path)
    for itemref in itemref_list:
        xhtml = itemref
        with open(xhtml, encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            title = soup.find('title').text
            if len(title) < 3:
                if soup.find('h1'):
                    title = soup.find('h1').text
                elif soup.find('h2'):
                    title = soup.find('h2').text
            print(title)
            content = str(soup.find('body'))[6:-7]
            title_content_list.append((title, content))
    # Get Images
    images = {}
    for root, folders, files in os.walk(path):
        for file in files:
            if file.split('.')[-1] in ['gif', 'jpg', 'png', 'jpeg']:
                with open(root + '/' + file, 'rb') as f:
                    image = f.read()
                images[file] = image

    return title_content_list, images


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
    # opts.headless = True
    ##  open firefox
    driver = webdriver.Firefox(firefox_profile=fp, capabilities=caps, options=opts)
    return driver


# Wait for Loading
def wait_loading(driver, sleep_seconds=60, timeout=60, before_loading=True):
    t1 = time.time()
    ## wait before loading
    if before_loading:
        while driver.execute_script('return document.readyState;') == 'complete' and time.time() - t1 < sleep_seconds:
            time.sleep(0.1)
    #time.sleep(1)
    ## wait for loading
    while driver.execute_script('return document.readyState;') != 'complete' and time.time() - t1 < timeout:
        scroll_down(driver)
        time.sleep(0.1)
    scroll_down(driver)
    ## calculate waiting time
    print('Loading time: ', time.time() - t1)


# Wait for presense of xpath
def waitXpath(driver, xpath, timeout=5):
    t1 = time.time()
    while time.time() - t1 < timeout:
        try:
            time.sleep(1)
            wait = WebDriverWait(driver, timeout=timeout)
            wait.until(expected_conditions.presence_of_element_located((By.XPATH, xpath)))
            break
        except:
            pass
    print(xpath, time.time() - t1)


# Scroll Down to Bottom
def scroll_down(driver):
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    except:
        pass


# Check next page by xpath
def next_page(driver, xpath):
    try:
        next_page = driver.find_element_by_xpath(xpath)
        next_page.click()
        wait_loading(driver, sleep_seconds=30)
        return True
    except:
        return False
