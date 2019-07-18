import os
from zipfile import ZIP_DEFLATED
from zipfile import ZipFile
from shutil import make_archive
from shutil import rmtree
from opencc import OpenCC
import threading
import sys
sys.setrecursionlimit(10000000)

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


def translate_html(html_path):
    with open(html_path, 'r') as f:
        f_content = convert_chinese(f.read())
        f.close()
    with open(html_path, 'w+') as f:
        f.write(f_content)
        f.close()


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

def unzipEpub(src_path, dst_path):
    # unzip epub files
    #   rename epub to zip
    zip_path = dst_path + '.zip'
    os.rename(src_path, zip_path)
    #   extract zip
    unzipfile(zip_path, dst_path)
    os.remove(zip_path)

def translateEpub(src_path):
    dst_path = convert_chinese(src_path.rstrip('.epub'))
    unzipEpub(src_path, dst_path)
    #   translate html files
    html_paths = get_file_paths(dst_path, ['html', 'xhtml', 'opf', 'ncx'])
    for html_path in html_paths:
        translate_html(html_path)
    zipEpub(dst_path)


def zipEpub(dst_path):
    # zip folder into epub
    make_archive(dst_path, 'zip', dst_path)
    os.rename(dst_path + '.zip', dst_path + '.epub')
    rmtree(dst_path)
    print(dst_path + '.epub')


def translate_epubs(top):
    epub_paths = get_file_paths(top, 'epub')
    for file in epub_paths:
        translateEpub(file)



