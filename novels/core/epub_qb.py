from novels.core.epub_core import *

def get_page_content(q,number,url, max_retries=5):
    for retries in range(max_retries):
        try:
            print(url)
            soup = bsoup(url, 'gbk')
            result = soup.find(id='mlfy_main_text')
            title = result.find('h1').text
            content = str(result.find(id='TextContent'))
            break
        except Exception as e:
            print(e)
            time.sleep(1)
    q.put((number, title, content))

class QB23():

    def __init__(self, url):
        self.url = url
        self.page_book_check()
        self.soup = bsoup(url, 'gbk')

    def page_book_check(self):
        if re.search(re.compile('\.html'), self.url):
            self.book_check = False
        else:
            self.book_check = True
# Book

    def get_book_info(self):
        self.book_title = self.soup.find(id='bookinfo').find('h1').text
        try:
            self.cover_src = urljoin(self.url, self.soup.find(id='bookimg').find('img').get('src'))
        except:
            self.cover_src = ''

    def get_url_list(self):
        a_list = self.soup.find(id='chapterList').find_all('a')
        list = [urljoin(self.url, a.get('href')) for a in a_list]
        self.url_list = [(url, '', '') for url in list]
        return self.url_list
# Page

    def get_page_content(self, url, max_retries = 5):
        srcs = []

        for retries in range(5):
            try:
                print(url)
                soup = bsoup(url, 'gbk')
                result = soup.find(id='mlfy_main_text')
                title = result.find('h1').text
                content = str(result.find(id='TextContent'))
                break
            except Exception as e:
                print(e)
                time.sleep(1)

        return (title, content, srcs)

    def get_page_title(self):
        self.page_title = self.soup.find(id='TextContent').find('h1').text

    def quit(self):
        ''






