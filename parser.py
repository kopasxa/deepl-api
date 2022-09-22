#from db import database
import imp
from lib2to3.pgen2 import driver
import os
import re
from this import d
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup as bs
from datetime import datetime
from db import database
from time import sleep
class Parser:
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome()
        self.driver.get(self.url)
        self.driver.implicitly_wait(10)
        self.driver.set_window_size(1440,1480)
        self.db = database()

    def get_all_articles(self, country):
        if country == "United Kingdom":
            return self.get_uk_articles()
        elif country == "United States":
            return self.get_us_articles()
        elif country == "Canada":
            return self.get_cn_articles()
        elif country == "France":
            return self.get_fr_articles()

        return self.driver

    def get_uk_articles(self):
        source = self.db.get_id_of_source("United Kingdom")
        articles = []
        article_items = self.driver.find_elements_by_xpath('//*[@id="lx-stream"]/div[1]/ol/li')

        for article in article_items:
            html_of_article = str(article.get_attribute("innerHTML"))
            try:
                soup = bs(html_of_article, 'html.parser')
                title = soup.find('header').text

                if not self.db.get_all_articles(title, source[0]) is None:
                    continue

                body = soup.find('div', {'class': 'qa-post-body'})
                url = "https://bbc.com" + body.select_one('a.qa-story-cta-link')['href']
                desc = body.find('p', {'class': 'qa-story-summary'}).text
                date = soup.find('span', {'class', 'qa-post-auto-meta'}).text
                text_articles = ""

                try:
                    try:
                        date = datetime.strptime(date, '%H:%M')
                        date = date.replace(year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
                        date = date.strftime('%Y-%m-%d %H:%M')
                    except:
                        date = datetime.strptime(date, '%H:%M %d %b')
                        date = date.replace(year=datetime.now().year)
                        date = date.strftime('%Y-%m-%d %H:%M')
                except:
                    date = datetime.now()
                    date = date.strftime('%Y-%m-%d %H:%M')

                self.driver.execute_script(f"window.open('{url}');")

                window_name = self.driver.window_handles
                self.driver.switch_to.window(window_name=window_name[-1])

                sleep(2)

                content = bs(self.driver.page_source, 'html.parser')
                pre_images = content.select('.ssrcss-pv1rh6-ArticleWrapper div[data-component=image-block] img')
                images = []
                for image in pre_images:
                    if float(image['height']) > 150:
                        images.append(image['src'])
                
                article_content = self.driver.find_element(By.CSS_SELECTOR, 'main div.ssrcss-1ocoo3l-Wrap')
                
                try:
                    element = self.driver.find_element(By.CSS_SELECTOR, '#sticky-mpu')
                    self.driver.execute_script("""
                    var element = arguments[0];
                    element.parentNode.removeChild(element);
                    """, element)

                    element = self.driver.find_element(By.CSS_SELECTOR, '#sticky-leaderboard')
                    self.driver.execute_script("""
                    var element = arguments[0];
                    element.parentNode.removeChild(element);
                    """, element)
                except:
                    pass

                reg = re.compile('[^0-9\s^a-zA-Z]')
                title = reg.sub('', title)

                parent_path = f"{source[1]}/{datetime.now().year}/{datetime.now().month}"

                if not os.path.exists(parent_path):
                    os.makedirs(parent_path)

                path_thumb = f'{parent_path}/{"_".join(title.split(" "))}.png'
                article_content.screenshot(path_thumb)

                for item in bs(self.driver.page_source, 'html.parser').select('div[data-component=text-block] p'):
                    text_articles += item.text + "\n"

                self.driver.switch_to.window(window_name=window_name[0])

                article_id = self.db.article_push_to_db({'id_source': source[0], 'title': title, 'url': url, 'desc': desc, 'date': date, 'text': text_articles, 'thumb': path_thumb})
                self.db.set_images_by_article(article_id, images)
            
                self.driver.execute_script("window.close();")
                self.driver.switch_to.window(window_name=window_name[0])   
            except Exception as r:
                print(r)
                self.driver.execute_script("window.close();")
                self.driver.switch_to.window(window_name=window_name[0])
                continue
        return articles

    def get_us_articles(self):
        source = self.db.get_id_of_source("United States")
        articles = []
        article_items = self.driver.find_elements_by_xpath('//*[@id="search"]/div[2]/div/div[2]/div')

        for article in article_items:
            html_of_article = str(article.get_attribute("innerHTML"))
            try:
                soup = bs(html_of_article, 'html.parser')
                title = soup.find('div', {'class', '__headline'}).text.strip()

                if not self.db.get_all_articles(title, source[0]) is None:
                    continue

                url = soup.select_one('a.__link')['href']
                desc = soup.find('div', {'class': '__description'}).text.strip()
                date = soup.find('div', {'class', '__date'}).text.strip()
                text_articles = ""

                try:
                    date = datetime.strptime(date, '%b %d, %Y')
                    date = date.replace(hour=datetime.now().hour, minute=datetime.now().minute)
                    date = date.strftime('%Y-%m-%d %H:%M')
                except:
                    date = datetime.now()
                    date = date.strftime('%Y-%m-%d %H:%M')

                self.driver.execute_script(f"window.open('');")

                window_name = self.driver.window_handles
                self.driver.switch_to.window(window_name=window_name[-1])

                self.driver.get(url)
                sleep(2)

                content = bs(self.driver.page_source, 'html.parser')

                new_date = content.select_one('div.timestamp').get_text().replace("Published", "").replace("Updated", "").replace(".", "").replace("ET", "").replace("EDT", "").strip()
                date = datetime.strptime(new_date, '%H:%M %p , %a %B %d, %Y')
                date = date.strftime('%Y-%m-%d %H:%M')

                try:
                    images = []
                    pre_images = content.select('.article__main .image__picture img[src]')
                    for item in pre_images:
                        images.append(item['src'])
                except:
                    images = []

                for item in content.select('.article__main p, .article__main h2'):
                    text_articles += item.text.strip() + "\n"

                if len(text_articles) < 50:
                    raise Exception("Text is too short")

                wait2 = WebDriverWait(self.driver, 10)
                try:
                    wait2.until(lambda x: x.find_element(By.CSS_SELECTOR, "video.top-player-video-element"))
                except:
                    pass
            
                try:
                    element = self.driver.find_element(By.CSS_SELECTOR, '.header__wrapper-outer')
                    self.driver.execute_script("""
                    var element = arguments[0];
                    element.parentNode.removeChild(element);
                    """, element)
                except Exception as r:
                    pass

                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, 'div.ad-slot-rail')
                    
                    for element in elements:
                        self.driver.execute_script("""
                        var element = arguments[0];
                        element.parentNode.removeChild(element);
                        """, element)
                except:
                    pass

                sleep(2)

                reg = re.compile('[^0-9\s^a-zA-Z]')
                title = reg.sub('', title)

                parent_path = f"{source[1]}/{datetime.strptime(date, '%Y-%m-%d %H:%M').year}/{datetime.strptime(date, '%Y-%m-%d %H:%M').month}"

                if not os.path.exists(parent_path):
                    os.makedirs(parent_path)

                path_thumb = f'{parent_path}/{"_".join(title.split(" "))}.png'
                article_content = self.driver.find_element(By.CSS_SELECTOR, 'body')
                article_content.screenshot(path_thumb)
                
                article_id = self.db.article_push_to_db({'id_source': source[0], 'title': title, 'url': url, 'desc': desc, 'date': date, 'text': text_articles, 'thumb': path_thumb})
                try:
                    self.db.set_images_by_article(article_id, images)
                except:
                    pass

                self.driver.execute_script("window.close();")
                self.driver.switch_to.window(window_name=window_name[0])
            except Exception as r:
                print(r)
                self.driver.execute_script("window.close();")
                self.driver.switch_to.window(window_name=window_name[0])
                continue
        return articles
    
    def get_cn_articles(self):
        source = self.db.get_id_of_source("Canada")
        articles = []
        article_items = self.driver.find_elements(By.CSS_SELECTOR, 'div.contentListCards .card')

        for article in article_items:
            html_of_article = str(article.get_attribute("outerHTML"))

            try:
                soup = bs(html_of_article, 'html.parser')
                title = soup.find('h3', {'class', 'headline'}).text.strip()

                if not self.db.get_all_articles(title, source[0]) is None:
                    continue

                if soup.select_one('a.card')['href'].startswith("//"):
                    url = "https:" + soup.select_one('a.card')['href']
                else:
                    url = "https://cbc.ca" + soup.select_one('a.card')['href']

                desc = soup.find('div', {'class': 'description'}).text.strip()
                #date = soup.find('div', {'class', '__date'}).text.strip()
                text_articles = ""

                self.driver.execute_script(f"window.open('');")

                window_name = self.driver.window_handles
                self.driver.switch_to.window(window_name=window_name[-1])

                self.driver.get(url)
                sleep(2)

                content = bs(self.driver.page_source, 'html.parser')

                new_date = content.select_one('time.timeStamp').get('datetime')
                date = datetime.strptime(new_date.replace("Z", "").replace("T", " "), '%Y-%m-%d %H:%M:%S.%f')
                date = date.strftime('%Y-%m-%d %H:%M')

                try:
                    element = self.driver.find_element(By.CSS_SELECTOR, '.ad-bigbox-fixed')
                    self.driver.execute_script("""
                    var element = arguments[0];
                    element.parentNode.removeChild(element);
                    """, element)
                except Exception as r:
                    pass

                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, '.ad-risingstar-container')
                    
                    for element in elements:
                        self.driver.execute_script("""
                        var element = arguments[0];
                        element.parentNode.removeChild(element);
                        """, element)
                except:
                    pass

                try:
                    images = []
                    pre_images = content.select('.story .imageMedia img[src]')
                    for item in pre_images:
                        images.append(item['src'])
                except:
                    images = []

                for item in content.select('.storyWrapper .story p, .storyWrapper .story h2'):
                    text_articles += item.text.strip() + "\n"

                if len(text_articles) < 50:
                    raise Exception("Text is too short")

                reg = re.compile('[^0-9\s^a-zA-Z]')
                title = reg.sub('', title)

                parent_path = f"{source[1]}/{datetime.strptime(date, '%Y-%m-%d %H:%M').year}/{datetime.strptime(date, '%Y-%m-%d %H:%M').month}"

                if not os.path.exists(parent_path):
                    os.makedirs(parent_path)

                path_thumb = f'{parent_path}/{"_".join(title.split(" "))}.png'
                article_content = self.driver.find_element(By.CSS_SELECTOR, 'body')
                article_content.screenshot(path_thumb)
                
                article_id = self.db.article_push_to_db({'id_source': source[0], 'title': title, 'url': url, 'desc': desc, 'date': date, 'text': text_articles, 'thumb': path_thumb})
                try:
                    self.db.set_images_by_article(article_id, images)
                except:
                    pass

                self.driver.execute_script("window.close();")
                self.driver.switch_to.window(window_name=window_name[0])
            except Exception as r:
                print(r)
                self.driver.execute_script("window.close();")
                self.driver.switch_to.window(window_name=window_name[0])
                continue
        return articles

    def get_fr_articles(self):
        source = self.db.get_id_of_source("France")
        articles = []
        self.driver.find_element(By.CSS_SELECTOR, 'button#didomi-notice-agree-button').click()
        sleep(1)
        article_items = self.driver.find_elements(By.CSS_SELECTOR, '.o-layout-list .o-layout-list__item')

        for article in article_items:
            html_of_article = str(article.get_attribute("outerHTML"))

            try:
                soup = bs(html_of_article, 'html.parser')
                title = soup.find('p', {'class', 'article__title'}).text.strip()

                if not self.db.get_all_articles(title, source[0]) is None:
                    break
                
                url = "https://france24.com" + soup.select_one('a[data-article-item-link]')['href']
                
                #desc = soup.find('div', {'class': 'description'}).text.strip()
                #date = soup.find('div', {'class', '__date'}).text.strip()
                text_articles = ""

                self.driver.execute_script(f"window.open('');")

                window_name = self.driver.window_handles
                self.driver.switch_to.window(window_name=window_name[-1])

                self.driver.get(url)
                sleep(2)

                content = bs(self.driver.page_source, 'html.parser')

                new_date = content.select_one('time[datetime]').text
                date = datetime.strptime(new_date, '%d/%m/%Y - %H:%M')
                date = date.strftime('%Y-%m-%d %H:%M')

                try:
                    element = self.driver.find_element(By.CSS_SELECTOR, 'div[data-tms-ad-container]')
                    self.driver.execute_script("""
                    var element = arguments[0];
                    element.parentNode.removeChild(element);
                    """, element)
                except Exception as r:
                    pass

                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, '.m-block-ad ')
                    
                    for element in elements:
                        self.driver.execute_script("""
                        var element = arguments[0];
                        element.parentNode.removeChild(element);
                        """, element)
                except:
                    pass

                try:
                    images = []
                    pre_images = content.select('article img[srcset]')
                    for item in pre_images:
                        images.append(item['srcset'].split(' ')[0])
                except:
                    images = []

                arrs = content.select('.t-content__chapo, .t-content__body p:not(div.o-self-promo p), .t-content__body h2')
                for item in arrs:
                    if arrs[-1] != item:
                        text_articles += item.text.strip() + "\n"

                if len(text_articles) < 50:
                    raise Exception("Text is too short")

                reg = re.compile('[^0-9\s^a-zA-Z]')
                title = reg.sub('', title)

                parent_path = f"{source[1]}/{datetime.strptime(date, '%Y-%m-%d %H:%M').year}/{datetime.strptime(date, '%Y-%m-%d %H:%M').month}"

                if not os.path.exists(parent_path):
                    os.makedirs(parent_path)

                path_thumb = f'{parent_path}/{"_".join(title.split(" "))}.png'
                article_content = self.driver.find_element(By.CSS_SELECTOR, 'body')
                article_content.screenshot(path_thumb)
                
                article_id = self.db.article_push_to_db({'id_source': source[0], 'title': title, 'url': url, 'date': date, 'text': text_articles, 'thumb': path_thumb})
                try:
                    self.db.set_images_by_article(article_id, images)
                except:
                    pass

                self.driver.execute_script("window.close();")
                self.driver.switch_to.window(window_name=window_name[0])
            except Exception as r:
                print(r)
                self.driver.execute_script("window.close();")
                self.driver.switch_to.window(window_name=window_name[0])
                continue
        return articles

    def close(self):
        self.driver.close()