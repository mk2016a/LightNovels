import os
from opencc import OpenCC
import threading
import queue


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

def get_folder_paths(root_path):
    folder_paths = []
    for root, dirs, files in os.walk(root_path):
        for dir in dirs:
            forler_path = os.path.join(root, dir)
            folder_paths.append(forler_path)
    return folder_paths


def convert_chinese(content):
    content = OpenCC('t2s').convert(content)
    return content


def translate_file(file_path):
    codes = ['utf-8', 'gbk']
    for code in codes:
        try:
            with open(file_path, 'r', encoding=code) as f:
                content = f.read()
                content = convert_chinese(content)
                with open(file_path, 'w+', encoding='utf-8') as f:
                    f.write(content)
                    f.close()
                break
        except Exception as e:
            print(code, e)
            pass
    print(file_path)


def translate_dirs(top):
    for root, dirs, files in os.walk(top, topdown=False):
        for dir in dirs:
            new_dir = convert_chinese(dir)
            if new_dir != dir:
                dir_path = os.path.join(root, dir)
                new_dir_path = os.path.join(root, new_dir)
                os.rename(dir_path, new_dir_path)
                print(new_dir_path)
    
def translate_files(top):
    for root, dirs, files in os.walk(top):
        for file in files:
            if file.split('.')[-1] in ['txt', 'md']:
                new_file = convert_chinese(file)
                new_file_path = os.path.join(root, new_file)
                if new_file != file:
                    file_path = os.path.join(root, file)
                    os.rename(file_path, new_file_path)
                t = threading.Thread(target=translate_file, args=(new_file_path,))
                t.start()

path = '/Volumes/Storage/Mine/Novels/TXT'
#translate_dirs(path)
translate_files(path)
