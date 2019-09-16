from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time
from datetime import datetime

from novels.core.epub_core import  *

# max thread number
max_thread_number = 4


class Light:

    def __init__(self, url):

        self.url = url
        self.page_book_check()
        # Get Driver
        self.driver = set_driver()
        if self.book_check:
            self.get_book_driver()
        else:
            self.get_page_driver()

    def page_book_check(self):
        if re.search(re.compile('mod=forumdisplay'), self.url):
            self.book_check = True
        else:
            self.book_check = False

    def get_book_driver(self):
        self.driver.get(self.url)

        # not work in small program only work in one line
        try:
            # Wait for click
            waitXpath(self.driver, '//div[@id="threadlist"]', 100)
        except Exception as e:
            print(e)
            self.log_in()
            # Wait for click
            waitXpath(self.driver, '//div[@id="threadlist"]', 600)
            pass

        # before get any information, it must be wait for loading all content
        wait_loading(self.driver)


    def get_page_driver(self, username='', password=''):

        self.driver.get(self.url)

        # not work in small program only work in one line
        try:
            # Wait for click only master link
            self.only_master()
        except Exception as e:
            print(e)
            self.log_in()
            # Wait for click
            self.only_master(60)
            pass
        # before get any information, it must be wait for loading all content
        wait_loading(self.driver, sleep_seconds=300)

    # Only Master
    def only_master(self, timeout=60):
        # Wait for click
        waitXpath(self.driver, '//div[@id="postlist"]', timeout)
        try:
            self.driver.find_element_by_link_text('显示全部楼层')
        except:
            self.driver.find_element_by_link_text('只看该作者').click()
            waitXpath(self.driver, '//a[text()="显示全部楼层"]')
            pass

    def log_in(self):
        waitXpath(self.driver, '//div[@id="main_message"]//table', 200)

        self.driver.find_element_by_xpath('//div[@id="main_message"]//input[@name="username"]').send_keys(
            self.username)
        self.driver.find_element_by_xpath('//div[@id="main_message"]//input[@name="password"]').send_keys(
            self.password)

        waitXpath(self.driver, '//input[@id="seccodeverify_cSA"]')
        self.driver.find_element_by_xpath('//input[@id="seccodeverify_cSA"]').click()

        # Wait for Verification
        waitXpath(self.driver, '//img[@src="static/image/common/check_right.gif"]', timeout=600)
        try:
            self.driver.find_element_by_xpath('//button[@name="loginsubmit"]').click()
        except:
            pass

    # Book

    def get_book_info(self):
        self.book_title = ''
        self.cover_src = ''

    def get_url_list(self):
        # Click Next Page and Get List
        list = []
        next_page_check = True
        while next_page_check:
            list = list + self.get_urls()
            next_page_check = next_page(self.driver, '//a[text()="下一页"]')

        list = reversed(list)
        self.url_list = list
        return self.url_list

    def get_urls(self):

        list = []
        source = self.driver.find_element_by_xpath('//table[@id="threadlisttableid"]').get_attribute('innerHTML')

        # Beautifulsoup parser innerHTML and find_all results
        soup = BeautifulSoup(source, 'html.parser')
        results = soup.find_all('tbody', id=re.compile('normalthread_\d+'))

        for result in results:
            a = result.find('a', class_="s xst")
            span = result.find('td', class_='by').em.span
            if span.span:
                date = datetime.strptime(span.span.get('title'), '%Y-%m-%d').date()
            else:
                date = datetime.strptime(span.text, '%Y-%m-%d').date()

            link = urljoin(self.url, a.get('href'))
            list.append((link, a.text, date))

        return list

# Page

    # Get Contents
    def get_page_content(self, url='', content_xpath='//td[@class="t_f"]|//div[@class="pattl"]'):
        # Define Variables
        title = self.get_page_title()
        if url == '':
            url = self.url
        image_srcs = []
        contents = ''

        # Next Page
        #while True:
        # Get Content and Images' src
        # Check Next
        next_page_check = True
        while next_page_check:
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
                    print('Error27: ', e)
                    pass
            next_page_check = next_page(self.driver, '//a[text()="下一页"]')

        self.image_srcs = image_srcs
        self.content = contents
        #self.driver.quit()
        return title, contents, image_srcs

    # Get Title
    def get_page_title(self, title_xpath='//span[@id="thread_subject"]'):
        try:
            title = self.driver.find_element_by_xpath(title_xpath).text
            title = convert_chinese(title)
            title = title.replace('/', '\\')
        except Exception as e:
            print('Error25')
            print(e)
            title = 'Unknown'
        self.page_title = title
        print(title)
        return title

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

    def quit(self):
        self.driver.quit()



