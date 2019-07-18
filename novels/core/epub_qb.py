from novels.core.epub_core import *

def get_page_content(q,number,url):
    while True:
        try:
            print(url)
            soup = bsoup(url, 'gbk')
            result = soup.find(id='TextContent')
            title = result.find('h1').text
            content = str(result)
            break
        except Exception as e:
            print(e)
            time.sleep(1)
    q.put((number, title, content))

class QB23():

    def __init__(self, url, folder=download_dir):
        self.url = url
        self.soup = bsoup(url, 'gbk')
        self.getTitleIndex()
        self.file = folder + self.title + ' qb ' + time.strftime('%m%d%H%M') + '.epub'

    def getTitleIndex(self):
        soup = self.soup
        url = self.url
        if soup.find(id='chapterList'):
            a_list = soup.find(id='chapterList').find_all('a')
            index = [urljoin(self.url, a.get('href')) for a in a_list]
            title = soup.find(id='bookinfo').find('h1').text
            image = urljoin(url, soup.find(id='bookimg').find('img').get('src'))
        else:
            index=[url]
            title = soup.find(id='TextContent').find('h1').text
            image = None
        self.title = title
        self.index = index
        self.image = image

    def check_update(self):
        return True

    def makeEpub(self, m=3):
        # Variable change
        urls = self.index
        file = self.file
        title = self.title
        image = self.image

        # Prepare epub
        print('Making Epub...')
        check_delete_file(file)
        book = mkepub.Book(title=title)
        q = queue.PriorityQueue()
        threads = []

        # Add Chapters
        for n,url in enumerate(urls):
            t = threading.Thread(target=get_page_content, args=(q,n,url))
            threads.append(t)
            while threading.active_count() > m:
                time.sleep(0.1)
            t.start()

        for t in threads:
            t.join()

        while not q.empty():
            n, title, content = q.get()
            #content = modify_content(content)  # modify content before add pages to keep most information for former actions
            book.add_page(title=title, content='<h1>{}</h1>\n'.format(title) + content)

        if image != '':
        # Set Cover
            set_cover_src(book, image)
        # Add CSS
        book.set_stylesheet(css_data)
        # Save File
        book.save(file)
        print(file)






