from novels.core.epub_core import *

# Bdtb

def master_only(url):
    if not re.search('see_lz=1', url):
        url = urllib.parse.urljoin(url, "?see_lz=1")
    return url


class BDTB():

    def __init__(self, url, folder=download_dir):
        #self.url = master_only(url)
        self.url = url
        self.soup = bsoup(self.url)
        self.getTitle()
        self.get_page_urls()
        self.folder = folder
        self.file_name = self.title + ' ' + time.strftime('%m%d%H%M') + '.epub'
        self.file = os.path.join(folder, self.file_name)
        self.getContent()

    def getTitle(self, title_tag="h3"):
        soup = self.soup
        try:
            title = soup.find_all(title_tag)[0].text
            openCC = OpenCC('t2s')
            title = openCC.convert(title)
        except (TypeError, IndexError):
            title = "unknow title"
        self.title = title
        print(title)

    def get_page_urls(self, ul_class='l_posts_num'):
        soup = self.soup
        url = self.url
        new_url_list = [self.url]
        try:
            for a in soup.find(class_=ul_class).find_all('a'):
                new_url = urllib.parse.urljoin(url, a.get('href'))
                if url in new_url and url != new_url and new_url not in new_url_list:
                    new_url_list.append(new_url)
        except Exception as e:
            print(e)
        self.new_url_list = new_url_list

    def checkUpdate(self, date_class='tail-info'):
        # url modify date
        url = self.new_url_list[-1]
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

    def getContent(self, content_class="d_post_content j_d_post_content "):
        # Define Variables
        url = self.url
        title = self.title
        image_srcs = []
        contents = ''

        # Next Page
        for url in self.new_url_list:

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
        return url, image_srcs, title, contents

    def makeEpub(self):

        # Variable change
        url = self.url
        title = self.title
        image_srcs = self.image_srcs
        contents = self.content
        file = self.file
        print(contents)

        # Prepare
        print('Making Epub...')
        check_delete_file(file)
        book = mkepub.Book(title=title)

        if image_srcs != []:
        # Set Cover
            set_cover_src(book, image_srcs[0])
        # Add Images
            contents, n = download_replace(url, image_srcs, contents, book, ocr_check=True)
        # Contents
        contents = convert_chinese(contents)
        # Split Chapters
        chapters = double_split(title, contents, chapter_pattern, second_pattern, chapter_length)
        # Add Chapters
        addChapter(book, title, chapters)
        # Add CSS
        book.set_stylesheet(css_data)
        # Save Book
        book.save(file)
        print(file)
