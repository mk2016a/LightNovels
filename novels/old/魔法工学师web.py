import sys
import os
sys.path.append('.')

from novels.core.epub_make import *

epub_path = '/Volumes/Storage/Mine/Novels/魔法工学师/Web.epub'
root_path = '/Volumes/Storage/Downloads/42'

book = mkepub.Book(title='Web')


title_content_list, image_list = read_epub(epub_path)

# Read Epub
## Add Chapter
for title, content in title_content_list:
    title = convert_chinese(title)
    content = convert_chinese(content)
    book.add_page(title=title, content=content)
## Add Image
if image_list != {}:
    for name, image in image_list.items():
        book.add_image(name, image)
rmtree(epub_path.split('.')[0])

# Get Files
file_paths = []
for root, folders, files in os.walk(root_path):
    for file in files:
        if file.split('.')[-1] == 'txt':
            file_paths.append(os.path.join(root, file))

# Read Files
title_content_list = []
for file in file_paths:

    title = ''
    content = ''

    with open(file, 'r', encoding='gbk') as f:
        lines = f.readlines()
        title = lines[0]

        i = 0 # print on condition 1

        for eachline in lines:

            if i == 1:
                content += eachline
                i = 0

            if eachline == '\n':
                i = 1
                next

    content = '<h3>'+title.strip()+'</h3>\n'+modify_txt(content)
    title_content_list.append((title, content))
    print(content)
    print('-'*90)

for title, content in title_content_list:
    title = convert_chinese(title)
    content = convert_chinese(content)
    book.add_page(title=title, content=content)

book.set_stylesheet(css_data)
check_delete_file(epub_path)
book.save(epub_path)