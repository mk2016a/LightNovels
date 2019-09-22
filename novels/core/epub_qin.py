from novels.core.epub_core import *

css_data = '''h1,h2{text-align: center}
p{text-indent: 2em}'''

class Qin():

    def __init__(self, url, max_retries=3):

        # self.variables
        self.url = url
        self.book_page_check()
        self.driver = set_driver()
        for retries in range(max_retries):
            self.driver.get(url)
            wait_loading(self.driver)
            self.soup = BeautifulSoup(self.driver.page_source, "html.parser")
            break

    def book_page_check(self):
        if re.search('/book/', self.url):
            self.book_check = True
        else:
            self.book_check = False

# Book

    def get_book_info(self):
        self.book_title = self.soup.find(class_='book_name flex_shrink').text
        try:
            self.cover_src = urljoin(self.url, self.soup.find(class_='book_info').find('img').get('src'))
        except:
            self.cover_src = ''

    def get_url_list(self):
        list = []
        a_list = self.soup.find_all(class_='site_box')[1].find_all('a')
        for a in a_list:
            link = urljoin(self.url, a.get('href'))
            if re.search('/read/', link) and link not in [item[0] for item in list]:
                list.append(link)
        self.url_list = [(link, '', '') for link in list]
        return self.url_list

# Page

    # Get Page Content
    def get_page_content(self, url, wrong_max=50, next_page_check = True):
        print(url)
        wrong_times = 0
        while True:
            try:
                self.driver.get(url)
                wait_loading(self.driver)
                resources = self.driver.page_source
                soup = BeautifulSoup(resources, "html.parser")
                result = soup.find(id='chapter_content')
                title = soup.find(class_='title').find('h3').text
                print(title)
                content = str(result)
                print(content[0:300])
                images = result.find_all('img')
                image_srcs = []
                for image in images:
                    image_src = image.get('src')
                    if image_src not in image_srcs:
                        image_srcs.append(image_src)

                # Try next page
                while next_page_check:
                    print('Next Page.')
                    resources = self.driver.page_source
                    soup = BeautifulSoup(resources, "html.parser")
                    result = soup.find(id='chapter_content')
                    print(str(result)[:300])
                    content = content +'\n'+ str(result)
                    images = result.find_all('img')
                    for image in images:
                        image_src = image.get('src')
                        if image_src not in image_srcs:
                            image_srcs.append(image_src)
                    next_page_check = next_page(self.driver, '//a[text()="下一页"]')
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


    def get_page_title(self):
        self.page_title = self.soup.find('h1').text

    # Quit Driver
    def quit(self):
        self.driver.quit()

    # Check next page
    def nextPage(self, link_text):
        try:
            next_page = self.driver.find_element_by_link_text(link_text)
            next_page.click()
            wait_loading(self.driver)
            return True
        except:
            return False
