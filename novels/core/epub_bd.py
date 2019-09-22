from novels.core.epub_core import *

# Bdtb

class Tieba():

    def __init__(self, url):

        self.url = bd_see_lz(url)
        self.page_book_check()
        self.soup = bsoup(self.url)

    def page_book_check(self):
        if re.search(re.escape('tieba.baidu.com/f'), self.url):
            self.book_check = True
        else:
            self.book_check = False

# Book

    def get_book_info(self):
        self.book_title = ''
        self.cover_src = ''

    def get_page_urls(self, ul_class='l_posts_num'):
        soup = self.soup
        list = [self.url]
        try:
            for a in soup.find(class_=ul_class).find_all('a'):
                url = urllib.parse.urljoin(self.url, a.get('href'))
                if self.url in url \
                        and url != self.url \
                        and url not in [item[0] for item in list]:
                    list.append((url, '', ''))
        except Exception as e:
            print(e)
        self.url_list = list
        return self.url_list

# Page

    def get_page_content(self, content_class="d_post_content j_d_post_content ", next_page_check = True):
        # Define Variables
        title = self.get_page_title()
        image_srcs = []
        contents = ''

        # Next Page
        for url in self.url_list:

            # Get Content and Images' src
            soup = bsoup(url)
            soup_contents = soup.find_all("div", class_=content_class)
            for soup_content in soup_contents:

                # Content
                contents += str(soup_content) + '<br/>\n'

                # Images
                soup_imgs = soup_content.find_all('img')
                if soup_imgs != []:
                    for soup_img in soup_imgs:
                        src = soup_img['src']
                        if 'face' not in src.split('/'):
                            p = 'https?://imgsa\.baidu\.com/forum/'
                            if re.match(p, src):
                                l = src.split('/')
                                l[4] = 'pic'
                                l[5] = 'item'
                                src = '/'.join(l)
                            image_srcs.append(src)

        self.content = contents
        self.image_srcs = image_srcs
        return title, contents, image_srcs

    def get_page_title(self, title_tag="h3"):
        soup = self.soup
        try:
            title = soup.find_all(title_tag)[0].text
            openCC = OpenCC('t2s')
            title = openCC.convert(title)
        except (TypeError, IndexError):
            title = "Unknown"
        self.page_title = title
        print(title)
        return title

    def checkUpdate(self, date_class='tail-info'):
        # url modify date
        url = self.url_list[-1]
        soup = bsoup(url)
        date_string = soup.find_all(class_=date_class)[-1].text
        date = datetime.strptime(date_string, '%Y-%m-%d %H:%M')
        print(date)
        # local modify date
        folder = self.folder
        title = self.title
        local_date = get_local_date(title, folder)
        # compare
        if date > local_date:
            return True
        else:
            return False

    def quit(self):
        ''

def bd_see_lz(url):
    if not re.match('https?\://', url):
        url = 'http://'+url
    if not re.search('see_lz=1', url):
        url = urllib.parse.urljoin(url, "?see_lz=1")
    return url
