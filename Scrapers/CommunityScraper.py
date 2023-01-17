import datetime
from pprint import pprint
import re

import requests
from bs4 import BeautifulSoup
from w3lib.html import remove_tags, replace_entities, remove_comments

from utils import *
from Scrapers.BasicScraper import BasicScraper
from items import Community

class CommunityScraper(BasicScraper):
    def __init__(self, name = 'CommunityScraper', spider_designation_path='./spider-designation.yaml'):
        super().__init__(name, spider_designation_path)
        self.result = []
        self.count = self.spider_config['count']
        self.ticker = self.spider_config['ticker']

    def start_requests(self):
        for page in range(301, 302):
            response = requests.get(
                self.start_urls[0], 
                headers=self.custom_settings['DEFAULT_REQUEST_HEADERS'],
                params=
                {
                    'code': str(self.ticker),
                    'page': str(page)
                }
            )
            self.parse_index_page(response)
            delay(self.delay)

        return self.result

    def parse_index_page(self, response):
        soup = BeautifulSoup(response.text, 'html.parser', from_encoding='euc-kr')
        table = soup.find('table', {'class': 'type2'})
        tb = table.select('tbody > tr')
        
        for i in range(2, len(tb)):
            if len(tb[i].select('td > span')) > 0:
                #print('in if')
                article = dict()
                article['title'] = tb[i].select('td.title > a')[0]['title']
                article['created_at'] = datetime.datetime.strptime(
                    tb[i].select('td > span')[0].text, 
                    '%Y.%m.%d %H:%M'
                    )
                url = self.allowed_domains[0] + tb[i].select('td.title > a')[0]['href']
                article_response = requests.get(
                    url,
                    headers=self.custom_settings['DEFAULT_REQUEST_HEADERS']
                )
                article['body'] = self.parse_article_page(article_response)
                article['views'] = tb[i].select('td > span')[1].text
                article['good'] = tb[i].select('td > strong')[0].text
                article['bad'] = tb[i].select('td > strong')[1].text
                
                self.result.append(Community(**article))
                dump_json(article, 'comu.json')
                print('done')
                delay(self.delay)

    def parse_article_page(self, response):
        soup = BeautifulSoup(response.text, 'html.parser', from_encoding='euc-kr')

        article_body = soup.find('div', id='body', class_='view_se')
        article_body = str(article_body)
        article_body = re.sub(r'<div .*?>', '', article_body)
        article_body = re.sub(r'</div>$', '', article_body)
        article_body = re.sub(r'<br/><br/>', '\n', article_body)
        article_body = re.sub(r'<br/>', '\n', article_body)
        article_body = re.sub('\r\n \n', '\n\n', article_body)
        article_body = re.sub('\r', '', article_body)
        article_body = remove_comments(article_body)
        article_body = replace_entities(article_body)
        article_body = remove_tags(article_body)
        
        return article_body
