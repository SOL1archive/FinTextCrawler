import datetime
import re
from pprint import pprint

import requests
from selenium import webdriver

from bs4 import BeautifulSoup
from w3lib.html import remove_tags, replace_entities, remove_comments

from Scrapers.BasicScraper import BasicScraper

from items import Article
from utils import *

class ArticleScraper(BasicScraper):
    def __init__(self, name='ArticleScraper', spider_designation_path='./spider-designation.yaml'):
        super().__init__(name, spider_designation_path)
        
        self.custom_settings['DEFAULT_QUERY_STRINGS']['display'] = self.spider_config['display']
        self.url_list = []
        # get list of links by searching
        for keyword in self.search_keywords:
            response = requests.get(
                url=self.start_urls[0],
                params=append_dict(
                    self.custom_settings['DEFAULT_QUERY_STRINGS'], 
                    {
                        'query': keyword,
                    }
                ),
                headers=append_dict(
                    self.custom_settings['DEFAULT_REQUEST_HEADERS'],
                    {
                        'X-Naver-Client-Id': self.spider_config['Naver_Client_Id'],
                        'X-Naver-Client-Secret': self.spider_config['Naver_Client_Secret'],
                    }
                )
            )

            if(response.status_code != 200):
                print("Error Code:" + response.status_code)
                raise RuntimeError

            # **매 쿼리마다 중복이 있는지 확인**
            query_items = response.json()['items']
            
            for item in query_items:
                date_str = item['pubDate']
                date_str = date_str[date_str.find(',') + 2:-6]
                pub_date = datetime.datetime.strptime(date_str, '%d %b %Y %H:%M:%S')
                if self.is_valid_date(pub_date) and (re.match(r'.*?//n.news.naver.com/mnews/article/.*', item['link']) != None):
                    self.url_list.append(item['link'].replace('\\', ''))

    def start_requests(self):
        result = []
        
        for url in self.url_list:
            if self.use_webdriver:
                driver = webdriver.ChromiumEdge(executable_path=self.webdriver_path)
                response = driver.get(url)
            else:
                response = requests.get(
                    url=url,
                    headers=self.custom_settings['DEFAULT_REQUEST_HEADERS']
                )

            article = self.parse_html(response)
            if article != None:
                result.append(article)
            
            delay(self.delay)
        
        return result
    
    def parse_html(self, response):
        article = dict()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        response_url = response.url
        print(response_url)
        if re.match(r'.*?naver[.]com.*?/article/[0-9]{3}/[0-9]{10}.*', response_url) == None:
            return None
        
        article['article_id'] = re.search(r'[0-9]{10}', response_url).group()
        article['press_id'] = re.search(r'/[0-9]{3}/', response_url).group()[1:-1]
        
        article['title'] = soup.find('h2', class_='media_end_head_headline').text
        try:
            article['author'] = soup.find('em', class_='media_end_head_journalist_name').text[:-3]
        except AttributeError:
            article['author'] = None
        datetime_str = soup.find('span', class_='media_end_head_info_datestamp_time _ARTICLE_DATE_TIME')['data-date-time']
        article['published_datetime'] = datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
        
        # article body parsing
        # 필요에 따라 세밀하게 조정될 필요가 있음
        article_body = str(soup.find('div', id='dic_area', class_='go_trans _article_content').extract())
        article_body = re.sub(r'<div class="go_trans _article_content".*?>', '', article_body)
        article_body = re.sub(r'</div>$', '', article_body)
        article_body = re.sub(r'<em class="img_desc">.*?</em>', '', article_body)
        article_body = re.sub(r'<strong.*?>.*?</strong>', '', article_body)
        article_body = re.sub(r'<br/><br/>', '\n', article_body)
        article_body = re.sub(r'\t', '', article_body)
        article_body = remove_comments(article_body)
        article_body = replace_entities(article_body)
        article_body = remove_tags(article_body)
        article_body = re.sub('\n{2,}', '', article_body)
        article_body = article_body.replace('△', '').replace(u'\xa0', u' ')
        article['article'] = article_body

        article['useful'] = int(soup.find('li', class_='u_likeit_list useful').find('span', class_='u_likeit_list_count _count').text)
        article['wow'] = int(soup.find('li', class_='u_likeit_list wow').find('span', class_='u_likeit_list_count _count').text)
        article['touched'] = int(soup.find('li', class_='u_likeit_list touched').find('span', class_='u_likeit_list_count _count').text)
        article['analytical'] = int(soup.find('li', class_='u_likeit_list analytical').find('span', class_='u_likeit_list_count _count').text)
        article['recommend'] = int(soup.find('li', class_='u_likeit_list recommend').find('span', class_='u_likeit_list_count _count').text)

        return Article(**article)
