from novels.core.epub_core import *

css_data = '''h1,h2{text-align: center}
p{text-indent: 2em}'''

def qbsoup(url):
    resources = requests.get(url).content.decode()
    soup = BeautifulSoup(resources, "html.parser")
    return soup

def getContent(q,number,url):
    while True:
        try:
            print(url)
            soup = qbsoup(url)
            result = soup.find(id='content')
            title = soup.find('h1').text
            content = str(result)
            images = result.find_all('img')
            image_srcs = []
            for image in images:
                image_src = image.get('src')
                if image_src not in image_srcs:
                    image_srcs.append(image_src)
            break
        except Exception as e:
            print(e)
            time.sleep(1)
    q.put((number, title, content, image_srcs, url))

def page_check(url):
    if url.split('.')[-1] in ['html', 'htm', 'xhtml']:
        return True
    else:
        return(False)


class Ep1k():

    def __init__(self, url, folder=download_dir):
        if not folder[-1]==['/']:
            folder = folder+'/'

        self.url = url
        self.soup = qbsoup(url)
        self.getTitleIndex()
        self.file = folder + self.title + ' 1k ' + time.strftime('%m%d%H%M') + '.epub'

    def getTitleIndex(self):
        soup = self.soup
        url = self.url
        index = []
        if page_check(url):
            index=[url]
            title = soup.find('h1').text
            cover = ''
        else:
            a_list = soup.find_all(class_='mulu')[1].find_all('a')
            for a in a_list:
                link = urljoin(self.url, a.get('href'))
                if page_check(link):
                    index.append(link)
            title = soup.find('h1').text
            cover = urljoin(url, soup.find(class_='jieshao').find('img').get('src'))
        print(title)
        self.title = title
        self.index = index
        self.cover = cover

    def check_update(self):
        return True

    def makeEpub(self, m=5):
        # Variable change
        urls = self.index
        file = self.file
        title = self.title
        cover = self.cover
        image_number = 0

        # Prepare epub
        print('Making Epub...')
        check_delete_file(file)
        book = mkepub.Book(title=title)
        q = queue.PriorityQueue()
        threads = []

        # Add Chapters
        for n,url in enumerate(urls):
            t = threading.Thread(target=getContent, args=(q,n,url))
            threads.append(t)
            while threading.active_count() >= m:
                time.sleep(0.1)
            t.start()

        for t in threads:
            t.join()

        while not q.empty():
            n, title, content, image_srcs, url = q.get()
            content, image_number = download_replace(url, image_srcs, content, book, image_count=image_number)
            content = modify_content(content)  # modify content before add pages to keep most information for former actions
            content = convert_chinese(content)
            book.add_page(title=title, content='<h1>{}</h1>\n'.format(title) + content)

        # Set Cover
        if cover != '':
            set_cover_src(book, cover)
        # Add CSS
        book.set_stylesheet(css_data)
        # Save File
        book.save(file)
        print(file)