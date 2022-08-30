from db import database
from selenium import webdriver

class Parser:
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome()
        self.driver.get(self.url)
        self.driver.implicitly_wait(10)

    def get_all_articles(self):
        return self.driver

    def get_title(self):
        return self.driver.find_element_by_xpath('//h1[@class="entry-title"]').text

    def get_content(self):
        return self.driver.find_element_by_xpath('//div[@class="entry-content"]').text

    def get_url(self):
        return self.url

    def get_date(self):
        return self.driver.find_element_by_xpath('//time[@class="entry-date published updated"]').text
    
    def close(self):
        self.driver.close()