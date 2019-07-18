from novels.core.epub_core import *
from zipfile import ZIP_DEFLATED
from zipfile import ZipFile
from shutil import make_archive
from shutil import rmtree

def get_file_paths(root_path, file_types):
    file_paths = []
    for root, dirs, files in os.walk(root_path):
        for file in files:
            try:
                if file.split('.')[-1] in file_types:
                    file_paths.append(os.path.join(root, file))
            except IndexError:
                pass
    return  file_paths


def convert_chinese(content):
    content = OpenCC('t2s').convert(content)
    return content

def rename_epub_zip(path1, path2):
    try:
        os.rename(path1, path2)
    except:
        pass

def unzipfile(zip_path, unzip_path):
    try:
        zf = ZipFile(zip_path, 'r')
        zf.extractall(unzip_path)
        zf.close()
    except:
        pass

def translate_html(html_path):
    with open(html_path, 'r') as hf:
        hf_content = convert_chinese(hf.read())
        hf.close()
    with open(html_path, 'w+') as hf:
        hf.write(hf_content)
        hf.close()

def zip_folder(src, dst=None):
    if not dst:
        dst = src+'.zip'
    try:
        os.makedirs(os.path.dirname(dst))
    except:
        pass
    zf = ZipFile(dst, 'w', ZIP_DEFLATED)
    for root, dirs, files in os.walk(src):
        for file in files:
            file_path = os.path.join(root, file)
            arc_path = convert_chinese(os.path.relpath(file_path, src)) # use relpath to create file's relative path of root
            zf.write(file_path, arc_path)
    zf.close()


class Combine():

    def __init__(self, path):
        if os.path.isdir(path):
            self.file_paths = get_file_paths(path, ['epub', 'zip'])
        else:
            self.file_paths = [path]

    def read(self):
        for path in self.file_paths:
            # unzip epub files
            unzip_path = path.rstrip('.epub')
            zip_path = unzip_path + '.zip'
            os.rename(path, zip_path)
            unzipfile(zip_path, unzip_path)
            os.rename(zip_path, path)
            # translate html files
            html_paths = get_file_paths(unzip_path, ['html', 'xhtml', 'opf', 'ncx'])
            for html_path in html_paths:
                translate_html(html_path)
            # zip folder into epub
            dst_path = convert_chinese(unzip_path)
            make_archive(dst_path, 'zip', unzip_path)
            os.rename(dst_path+'.zip', dst_path+'.epub')
            rmtree(unzip_path)
            print(dst_path+'.epub')




