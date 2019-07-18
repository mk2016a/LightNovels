from novels.core.epub_core import *

css_data = '''h1,h2{text-align: center}
p{text-indent: 2em}'''


class WK8():

    def __init__(self, url, folder=download_dir):

        ## self.varibles
        self.url = url
        self.folder = folder
        if not folder[-1]==['/']:
            self.folder = folder+'/'
        self.driver = set_driver()

    def getTitleIndex(self, wrong_max=5):
        wrong_times = 0
        while True:
            try:
                ## open url
                url = self.url
                self.driver.get(url)
                wait_loading(self.driver)

                ## get page source
                resources = self.driver.page_source
                soup = BeautifulSoup(resources, "html.parser")
                index = []

                ## check whether page
                if re.search('wenku8\.net/novel/[/\d]+\.htm$', url):
                    title = soup.find('h1').text
                    cover_src = ''
                    index=[url]

                ## get index urls
                elif re.search('wenku8\.net/book/', url):
                    title = soup.find('span').text
                    cover_src = urljoin(url, soup.find_all('img')[1].get('src'))
                    self.driver.find_element_by_link_text('小说目录').click()
                    wait_loading(self.driver)
                    resources = self.driver.page_source
                    index_soup = BeautifulSoup(resources, "html.parser")
                    a_list = index_soup.find('table', class_='css').find_all('a')
                    for a in a_list:
                        link = urljoin(self.driver.current_url, a.get('href'))
                        print(link)
                        if link not in index:
                            index.append(link)

                self.title = title
                self.index = index
                self.cover_src = cover_src
                break

            except Exception as e:
                print(e)
                wrong_times += 1
                time.sleep(1)
                if wrong_times >= wrong_max:
                    break
                else:
                    print('Try again.')
                pass


    def check_update(self):
        return True

    # Check next page
    def nextPage(self, link_text):
        try:
            next_page = self.driver.find_element_by_link_text(link_text)
            next_page.click()
            wait_loading(self.driver)
            return True
        except:
            return False

    # Get Page Content
    def get_page_content(self, url, wrong_max = 50):
        wrong_times = 0
        while True:
            try:
                print(url)
                self.driver.get(url)
                wait_loading(self.driver)
                resources = self.driver.page_source
                soup = BeautifulSoup(resources, "html.parser")
                result = soup.find(id='content')
                title = soup.find(id='title').text
                print(title)
                content = str(result)
                print(content[:300])
                images = result.find_all('img')
                image_srcs = []
                for image in images:
                    image_src = image.get('src')
                    if image_src not in image_srcs:
                        image_srcs.append(image_src)
                return (title, content, image_srcs)

            except Exception as e:
                print(e)
                wrong_times += 1
                time.sleep(1)
                if wrong_times >= wrong_max:
                    break
                else:
                    print('Try again.')
                pass

    # Process all
    def makeEpub(self):

        ## Get Title and Index
        self.getTitleIndex()

        ## Make Epub File
        self.file = self.folder + self.title + ' wk ' + time.strftime('%m%d%H%M') + '.epub'

        # Variable change
        index = self.index
        file = self.file
        title = self.title
        cover_src = self.cover_src
        image_number = 0

        # Prepare epub
        print('Making Epub...')
        check_delete_file(file)
        book = mkepub.Book(title=title)

        # Add Chapters
        content_check = ''
        for n,url in enumerate(index):
            title, content, image_srcs = self.get_page_content(url)
            while content == content_check:
                print('Same Page.')
                title, content, image_srcs = self.get_page_content(url)
            content_check = content
            content, image_count = download_replace(url, image_srcs, content, book, image_count)
            content = convert_chinese(content)
            content = modify_content(content)  # modify content before add pages to keep most information for former actions
            book.add_page(title=title, content='<h1>{}</h1>\n'.format(title) + content)

        # Set Cover
        set_cover_src(book, cover_src)

        # Add CSS
        book.set_stylesheet(css_data)

        # Save File
        book.save(file)
        print(file)
        self.driver.quit()

    # Quit Driver
    def quit(self):
        self.driver.quit()