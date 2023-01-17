import datetime
from pprint import pprint

import yaml

import requests

from utils import *

class BasicScraper:
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'Accept-Language': 'ko-KR'
        },
    }

    def __init__(self, name='BasicScraper', spider_designation_path='./spider-designation.yaml'):
        self.name = name
        if self.name == 'BasicScraper':
            raise NotImplementedError
        
        with open(spider_designation_path, 'r') as f:
            self.spider_config = yaml.load(f, Loader=yaml.FullLoader)[self.name]

        self.use_webdriver = self.spider_config['use_webdriver']
        if self.use_webdriver:
            self.webdriver_path = self.spider_config['webdriver_path']
        self.start_urls = get_listed(self.spider_config['start_url'])
        self.target_keywords = self.spider_config['target_keywords']
        self.allowed_domains = self.spider_config['allowed_domains']
        self.delay = self.spider_config['delay']

        self.custom_settings['DEFAULT_QUERY_STRINGS'] = dict()

        self.start_date = datetime.datetime.strptime(
            self.spider_config['start_date'], 
            '%Y-%m-%d %H:%M:%S'
            )
        self.end_date = datetime.datetime.strptime(
            self.spider_config['end_date'],
            '%Y-%m-%d %H:%M:%S'
            )
        
        self.search_keywords = get_listed(self.spider_config['search_keywords'])
        
    def is_valid_date(self, date):
        return self.start_date <= date <= self.end_date
