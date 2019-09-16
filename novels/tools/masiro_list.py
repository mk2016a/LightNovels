from novels.core.epub_core import  *


# max thread number
max_thread_number = 4

class MasiroList:

    def __init__(self, url, folder = download_dir, username='', password=''):

        self.url = url
        self.username = username
        self.password = password
        self.folder = folder

    # Get Index List
    def getList(self):

        caps = DesiredCapabilities().FIREFOX
        caps["pageLoadStrategy"] = "none"  # none, eager, normal
        fp = webdriver.FirefoxProfile('/Users/mk/Library/Application Support/Firefox/Profiles/wn1jjo27.default')
        fp.set_preference('network.proxy.type', 0)  # direct, none proxy
        opts = webdriver.FirefoxOptions()
        # opts.headless = True

        self.driver = webdriver.Firefox(firefox_profile=fp, capabilities=caps, options=opts)
        # self.driver.set_window_position(-1920, 0)
        # self.driver.set_window_size(1920, 1057)
        self.driver.get(self.url)

        # not work in small program only work in one line
        try:
            # Wait for click
            waitXpath(self.driver, '//div[@id="threadlist"]', 100)

        except:

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

            # Wait for click
            waitXpath(self.driver, '//div[@id="threadlist"]', 600)
            pass

        # before get any information, it must be wait for loading all content
        wait_loading(self.driver)

        # Get Book Title
        title = self.getTitle()

        # Click Next Page and Get List
        list = []
        next_page_check = True
        while next_page_check:
            list = list + self.getOneList()
            next_page_check = next_page(self.driver, '//a[text()="下一页"]')

        self.driver.quit()
        list = reversed(list)

        return title, list

    # Get Title
    def getTitle(self, title_xpath='//h1[@class="xs2"]/a'):
        try:
            title = self.driver.find_element_by_xpath(title_xpath).text
            title = convert_chinese(title)
            title = title.replace('/', '\\')
        except Exception as e:
            print('Error25')
            print(e)
            title = 'Unknown'
        return title

    def getOneList(self):

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
            list.append((a.get('href'), a.text, date))

        return list