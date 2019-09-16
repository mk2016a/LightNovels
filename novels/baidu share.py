import sys
sys.path.append('.')

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException
import time
from datetime import datetime

class BaiduShare:

    def __init__(self, url='https://pan.baidu.com/mbox/homepage#share/type=friend'):

        caps = DesiredCapabilities().FIREFOX
        caps["pageLoadStrategy"] = "eager"  # none, eager, normal
        opts = webdriver.FirefoxOptions()
        #opts.headless = True
        fp = webdriver.FirefoxProfile('/Users/mk/Library/Application Support/Firefox/Profiles/wn1jjo27.default')
        fp.set_preference('network.proxy.type', 0)  # direct, none proxy

        self.url = url
        self.driver = webdriver.Firefox(firefox_profile=fp, capabilities=caps, options=opts)
        #self.driver.set_window_size(1920, 1200)
        #self.driver.set_window_position(-1920, 0)
        self.getDriver(url)

        # Refresh when can not loaded
        self.driver.refresh()

        # Find Share
        x22 = '//a[@data-sharetype="friend"]'
        x23 = '//a[@class="avatar service-icon-newfriend"]'
        x24 = '//a[@class="shareFile"]'
        x25 = '//div[@class="select-file"]'
        x26 = '//iframe[@id="yunfujianPanel"]'
        x261 = '//span[@node-type="chk"]/following::div[@title="Novels"]'
        x262 = '//a[@class="sbtn sure"]'
        x27 = '//div[@title="Novels"]'
        shared_count = 0
        time.sleep(10)

        # Sharing Everyone
        for i in range(100):
            '''
            if shared_count>=15:
                print('All shared.')
                break
            '''
            print(i+1)

            # Go to the New Friends List
            for x in [x22, x23]:
                print(x)
                time.sleep(2)
                self.waitXpath(x, 5)
                self.driver.find_element_by_xpath(x).click()

            # Find Share Buttons and Click the Right One
            #time.sleep(2)
            self.waitXpath(x24)
            shares = self.driver.find_elements_by_xpath(x24)
            share = shares[i]
            share.click()

            # Break if already shared
            try:
                time.sleep(2)
                self.driver.find_element_by_xpath(x27)
                print('Already shared!')
                shared_count += 1
                continue
            except NoSuchElementException as e:
                pass
            self.driver.find_element_by_xpath(x25).click()

            # Switch to iFrame to Share Folder
            #time.sleep(2)
            self.waitXpath(x26)
            iframe_switch = self.driver.find_element_by_xpath(x26)
            self.driver.switch_to.frame(iframe_switch)
            print('Switch to iframe')
            self.waitXpath(x261)
            self.driver.find_element_by_xpath(x261).click()
            self.waitXpath(x262)
            self.driver.find_element_by_xpath(x262).click()
            time.sleep(1)

            # Switch Back to the Main Content
            self.driver.switch_to.default_content()
            print('Switch back')
            time.sleep(1)


        self.driver.quit()
        print('Done.')

    # Try to get url 3 times
    def getDriver(self, url):
        try_times = 0
        while try_times < 3:
            try:
                self.driver.get(url)
                self.waitLoading()
                break

            except:
                try_times += 1
                pass

    # Wait for presense of xpath
    def waitXpath(self, xpath, timeout=5):
        t1 = time.time()
        while time.time() - t1 < timeout:
            try:
                time.sleep(1)
                wait = WebDriverWait(driver=self.driver, timeout=timeout)
                wait.until(expected_conditions.presence_of_element_located((By.XPATH, xpath)))
                break
            except:
                pass
        print(xpath, time.time()-t1)

    # Wait for Loading
    def waitLoading(self, timeout=30):
        t1 = time.time()
        while self.driver.execute_script('return document.readyState;') != 'complete' and time.time()-t1 < timeout:
            self.scroll_down()
            time.sleep(0.1)
        print('Loading time', time.time()-t1)

    # Scroll Down to Bottom
    def scroll_down(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Safari Click
    def jclick(self, xpath):
        element = self.driver.find_element_by_xpath(xpath)
        return self.driver.execute_script("arguments[0].click();", element)

    # Quit Driver
    def driver_quit(self):
        self.driver.quit()
        print('Driver quit.')

try:
    baidushare = BaiduShare()
except Exception as e:
    pass
exit()


''''
for i in range(100):
    try:
        print('#'*90)
        baidushare = BaiduShare()
        #time.sleep(60)
        exit()
    except Exception as e:
        print(e)
'''
