from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import datetime

from novels.core.epub_core import  *


# max thread number
max_thread_number = 4


class Zhenbai:

    def __init__(self, url, folder = download_dir, username='', password=''):

        caps = DesiredCapabilities().FIREFOX
        caps["pageLoadStrategy"] = "none"  # none, eager, normal
        fp = webdriver.FirefoxProfile()
        fp = webdriver.FirefoxProfile('/Users/mk/Library/Application Support/Firefox/Profiles/wn1jjo27.default')
        fp.set_preference('network.proxy.type', 0)  # direct, none proxy

        self.url = url
        self.driver = webdriver.Firefox(firefox_profile=fp, capabilities=caps)

        self.driver.set_window_position(-1920, 0)
        self.driver.set_window_size(1920, 1057)
        self.driver.get(url)

        # not work in small program only work in one line
        try:
            # Wait for click
            self.waitXpath('//div[@id="postlist"]', 100)
            try:
                self.driver.find_element_by_link_text('显示全部楼层')
            except:
                self.driver.find_element_by_link_text('只看该作者').click()
                self.waitXpath('//a[text()="显示全部楼层"]')
                print('只看该作者')
                pass

        except:

            self.waitXpath('//div[@id="main_message"]//table', 200)

            self.driver.find_element_by_xpath('//div[@id="main_message"]//input[@name="username"]').send_keys(
                username)
            self.driver.find_element_by_xpath('//div[@id="main_message"]//input[@name="password"]').send_keys(
                password)

            self.waitXpath('//input[@id="seccodeverify_cSA"]')
            self.driver.find_element_by_xpath('//input[@id="seccodeverify_cSA"]').click()

            # Wait for Verification
            self.waitXpath('//img[@src="static/image/common/check_right.gif"]', time=600)
            try:
                self.driver.find_element_by_xpath('//button[@name="loginsubmit"]').click()
            except:
                pass

            # Wait for click
            self.waitXpath('//div[@id="postlist"]', 600)

            try:
                self.driver.find_element_by_link_text('显示全部楼层')
            except:
                self.driver.find_element_by_link_text('只看该作者').click()
                self.waitXpath('//a[text()="显示全部楼层"]')
                print('只看该作者')
                pass

            pass
        # before get any information, it must be wait for loading all content
        self.waitLoading(timeout=20)
        #self.scroll_down()

        self.getTitle()
        self.folder = folder
        self.file_name = self.title + ' ' + time.strftime('%m%d%H%M') + '.epub'
        self.file = os.path.join(folder, self.file_name)


    # Wait for presense of xpath
    def waitXpath(self, xpath, time=5):
        t1 = time.time()
        wait = WebDriverWait(self.driver, time)
        wait.until(expected_conditions.presence_of_element_located((By.XPATH, xpath)))
        t2 = time.time()
        print(t2-t1)

    # Wait for Loading
    def waitLoading(self, timeout=30):
        t1 = time.time()
        wait_time = 0
        while self.driver.execute_script('return document.readyState;') != 'complete' and wait_time < timeout:
            self.scroll_down()
            wait_time += 1
            time.sleep(1)
        t2 = time.time()
        print(t2-t1)
        print('Load Complete.')

    # Scroll Down to Bottom
    def scroll_down(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Check next page
    def nextPage(self, link_text):
        try:
            next_page = self.driver.find_element_by_link_text(link_text)
            next_page.click()
            time.sleep(30)
            self.waitLoading()
            return True
        except:
            print('All Done.')
            return False


    # Get Title
    def getTitle(self, title_xpath='//span[@id="thread_subject"]'):
        try:
            title = self.driver.find_element_by_xpath(title_xpath).text
            title = convert_chinese(title)
            title = title.replace('/', '\\')
        except Exception as e:
            print('Error25')
            print(e)
            title = 'Unknown'
        self.title = title
        print(title)

    # Get Date
    def getDate(self, date_xpath):
        date = datetime.fromtimestamp(0)
        date_elms = self.driver.find_elements_by_xpath(date_xpath)
        for date_elm in date_elms:
            date_text = re.search('(?<=\D)\d{4}-\d{1,2}-\d{1,2} \d\d:\d\d', date_elm.text)[0]
            date_tmp = datetime.strptime(date_text, '%Y-%m-%d %H:%M')
            if date_tmp > date:
                date = date_tmp
        return date

    # Check Update
    def checkUpdate(self, mdate_xpath='//td[@class="t_f"]/i[@class="pstatus"]', cdate_xpath='//div[@class="authi"]/em'):
        # url modify date
        try:
            mdate = self.getDate(mdate_xpath)
        except:
            print('Error26')
            pass
        cdate = self.getDate(cdate_xpath)
        if mdate > cdate:
            date = mdate
        else:
            date = cdate
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

    # Get Contents
    def getContent(self, content_xpath='//td[@class="t_f"]|//div[@class="pattl"]'):
        # Define Variables
        title = self.title
        url = self.url
        image_srcs = []
        contents = ''

        # Next Page
        #while True:
        # Get Content and Images' src
        results = self.driver.find_elements_by_xpath(content_xpath)
        for result in results:
            try:
                #print(result.text)
                # Add Content
                contents += result.get_attribute('innerHTML')
                # Add Image srcs
                imgs = result.find_elements_by_tag_name('img')
                if imgs != []:
                    for img in imgs:
                        src = img.get_attribute('src')
                        if src not in image_srcs and src != None and not re.search('(google)|(none\.gif)', src) :
                            image_srcs.append(src)
            except Exception as e:
                print('Error27')
                print(e)
                pass

        # Check Next
        next_page = self.nextPage('下一页')
        while next_page:
            print('Next Page')
            results = self.driver.find_elements_by_xpath(content_xpath)
            for result in results:
                try:
                    # print(result.text)
                    # Add Content
                    contents += result.get_attribute('innerHTML')
                    # Add Image srcs
                    imgs = result.find_elements_by_tag_name('img')
                    if imgs != []:
                        for img in imgs:
                            src = img.get_attribute('src')
                            if src not in image_srcs and src != None and not re.search('(google)|(none\.gif)', src):
                                image_srcs.append(src)
                except Exception as e:
                    print('Error27')
                    print(e)
                    pass

            next_page = self.nextPage('下一页')

        self.image_srcs = image_srcs
        self.content = contents
        self.driver.quit()
        return url, image_srcs, title, contents

    # Make Epub
    def makeEpub(self):

        self.getContent()

        title = self.title
        url = self.url
        image_srcs = self.image_srcs
        contents = self.content

        # Prepare
        print('Making Epub...')
        file = self.file
        check_delete_file(file)
        book = mkepub.Book(title=title)

        if image_srcs != []:
        # Set Cover:
            set_cover_src(book, image_srcs[0])
        # Add Images
            contents, n = download_replace(url, image_srcs, contents, book, max_threads=max_thread_number)
        # Contents
        contents = convert_chinese(contents)
        # Split Chapters
        print(contents)
        chapters = double_split(title, contents, chapter_pattern, second_pattern, first_l=chapter_length)
        # Add Chapters
        addChapter(book, title, chapters)   # modified in addChapter to keep most information for former actions
        # Add CSS
        book.set_stylesheet(css_data)
        # Save Book
        book.save(file)
        print(file)




