from novels.core.epub_bd import *
from novels.core.epub_ln import *
from novels.core.epub_qb import *
from novels.tools.get_list import *
from novels.tools.rename import *


# Make
def check_replace(path, title,  keyword, replacement):
    if re.search(keyword, title):
        file = RenameFiles(path)
        file.rename(keyword, replacement)

def mk_bd(url, folder = download_dir):
    bdtb = BDTB(url, folder)
    if bdtb.checkUpdate():
        bdtb.makeEpub()

def mk_ln(url, folder = download_dir):
    novel = LightNovel(url, folder)
    if novel.checkUpdate():
        novel.makeEpub()

def mk_qb(url, folder = download_dir):
    qb = QB23(url, folder)
    qb.makeEpub()

def mk_all(urls, folder = download_dir):
    threads = []
    m = 8
    for url in urls:
        print(url)
        if re.search('tieba.baidu.com', url):
            while threading.active_count() > m:
                time.sleep(0.1)
            t = threading.Thread(target=mk_bd, args=(url,folder), daemon=True)
            threads.append(t)
            t.start()
            for t in threads:
                t.join()
        elif re.search('qb23.com', url):
            while threading.active_count() > m:
                time.sleep(0.1)
            t = threading.Thread(target=mk_qb, args=(url,folder), daemon=True)
            threads.append(t)
            t.start()
            for t in threads:
                t.join()

        elif re.search('www.lightnovel.cn', url):
            mk_ln(url, folder)

    print('All Done.')

urls = [
    'https://tieba.baidu.com/p/5945463835?see_lz=1',
    'https://tieba.baidu.com/p/5912376064?see_lz=1',
]
mk_all(urls)

#url = 'https://tieba.baidu.com/p/5967082655?see_lz=1 '
#mk_bd(url)
#mk_ln(url)

