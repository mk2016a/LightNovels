import os
import re
import time
from zipfile import ZIP_DEFLATED
from zipfile import ZipFile
from shutil import make_archive
from shutil import rmtree
from opencc import OpenCC
import threading


modify_patterns = [
    ('<p>\s*?(<img.+?>)[^<>]\s*?</p>', '<div>\g<1></div>'),
]

# Unzip EPUB
def get_file_paths(root_path, file_types):
    file_paths = []
    for root, dirs, files in os.walk(root_path):
        for file in files:
            try:
                if file.split('.')[-1] in file_types:
                    file_paths.append(os.path.join(root, file))
            except IndexError:
                pass
    return file_paths


def convert_chinese(content):
    content = OpenCC('t2s').convert(content)
    return content


def unzipfile(zip_path, dst_path):
    zf = ZipFile(zip_path, 'r')
    zf.extractall(dst_path)
    zf.close()


def modify_html(html_path):
    with open(html_path, 'r') as f:
        content = convert_chinese(f.read())
        for m_pattern in modify_patterns:
            content = re.sub(m_pattern[0], m_pattern[1], content)
    with open(html_path, 'w+') as f:
        f.write(content)


def zip_folder(src, dst=None):
    if not dst:
        dst = src + '.zip'
    try:
        os.makedirs(os.path.dirname(dst))
    except:
        pass
    zf = ZipFile(dst, 'w', ZIP_DEFLATED)
    for root, dirs, files in os.walk(src):
        for file in files:
            file_path = os.path.join(root, file)
            arc_path = convert_chinese(
                os.path.relpath(file_path, src))  # use relpath to create file's relative path of root
            zf.write(file_path, arc_path)
    zf.close()


class Modify():

    def __init__(self, path):
        self.path = path
        self.dst_path = convert_chinese(path.split('.')[0])
        # instead of using rstrip('.epub') because 'eb' will be stripped as well
        self.unzipEpub()
        self.modifyEpub()
        self.zipEpub()

    def unzipEpub(self):
        # unzip epub files
        #   rename epub to zip
        path = self.path
        dst_path = self.dst_path
        zip_path = dst_path + '.zip'
        os.rename(path, zip_path)
        #   extract zip
        unzipfile(zip_path, dst_path)
        os.remove(zip_path)

    def modifyEpub(self):
        dst_path = self.dst_path
        html_paths = get_file_paths(dst_path, ['html', 'xhtml'])
        for html_path in html_paths:
            print(html_path)
            modify_html(html_path)

    def zipEpub(self):
        # zip folder into epub
        dst_path = self.dst_path
        make_archive(dst_path, 'zip', dst_path)
        os.rename(dst_path + '.zip', dst_path + '.epub')
        rmtree(dst_path)
        print(dst_path + '.epub')


folder = '/Volumes/Storage/Mine/Novels'
#folder = '/Volumes/Storage/Downloads'



for root, dirs, files in sorted(os.walk(folder)):
    for file in files:
        if file.split('.')[-1] in ['epub']:
            try:
                path = os.path.join(root, file)
                Modify(path)
            except Exception as e:
                print('Error', path)



