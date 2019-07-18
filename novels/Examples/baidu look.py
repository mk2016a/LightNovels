import sys
sys.path.append('.')

from novels.core.epub_core import *

# Look
def print_list(q, url):
    soup = bsoup(url)
    title = soup.find('a', class_=' card_title_fname').text
    q.put(title)
    lists = soup.find_all('a', class_='j_th_tit ')
    for line in lists:
        link = urljoin(url, line.get('href'))+'?see_lz=1'
        title = line.text
        if re.search('(' + re_number + ')|(特典)|(Web)', title):
            q.put(link+'\t'+title)
        #print(str(line))

def bd_look(urls):
    m = 8
    threads = []
    queues = []
    for url in urls:
        q = queue.PriorityQueue()
        t = threading.Thread(target=print_list, args=(q, url), daemon=True)
        threads.append(t)
        t.start()
        queues.append(q)

    for t in threads:
        t.join()

    for q in queues:
        print(q.get())
        t_list = []
        while not q.empty():
            print(q.get())

    print('\n'+'-'*99+'\n')


look_urls=[
    'https://tieba.baidu.com/f?kw=一击男',
    # 'https://tieba.baidu.com/f?kw=天启的异世界转生谭',
    'https://tieba.baidu.com/f?kw=无职转生',
    'https://tieba.baidu.com/f?kw=关于我转生成为史莱姆的那件事',
    'https://tieba.baidu.com/f?kw=骑士魔法',
    'https://tieba.baidu.com/f?kw=灰与幻想的格林姆迦尔',
    'https://tieba.baidu.com/f?kw=哥布林杀手',
    'https://tieba.baidu.com/f?kw=为美好的世界献上祝福',
    'https://tieba.baidu.com/f?kw=期待在地下城邂逅有错吗',
    'https://tieba.baidu.com/f?kw=re从零开始异世界生活',
    'https://tieba.baidu.com/f?kw=盾之勇者成名录',
    'https://tieba.baidu.com/f?kw=异世界狂想曲',

]
bd_look(look_urls)

