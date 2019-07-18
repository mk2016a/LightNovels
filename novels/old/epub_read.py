import os
import zipfile
from zipfile import ZIP_DEFLATED
from zipfile import ZipFile
from shutil import make_archive
from shutil import rmtree
from opencc import OpenCC
from bs4 import BeautifulSoup


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
    zf = zipfile.ZipFile(zip_path, 'r')
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


class EpubPlus():

    def __init__(self, file):
        self.file = file
        self.path = file.split('.')[0]

    def unzipEpub(self):
        # unzip epub files
        #   rename epub to zip
        file = self.file
        path = self.path
        zip_path = path + '.zip'
        os.rename(file, zip_path)
        #   extract zip
        unzipfile(zip_path, path)
        os.rename(zip_path, file)

    def removeFolder(self):
        # remote unzip directory
        path = self.path
        rmtree(path)

    def readopf(self):      # to correct order of files
        
        self.unzipEpub()
        # Read XML
        folder = self.path
        for root, folders, files in os.walk(folder):
            for file in files:
                file_type = file.split('.')[-1]
                if file_type == 'opf':
                    opf_file = root+'/'+file
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
            itemref_list.append(manifest_list[itemref['idref']])
        #print(itemref_list)
        return itemref_list





paths = [
    '/Volumes/Storage/Downloads/【渣排】素晴15.epub',
    '/Volumes/Storage/Downloads/在地下城期待邂逅是否搞错了什么 14 12160949.epub',
]
for path in paths:
    m = EpubPlus(path)
    m.unzipEpub()
    m.readopf()