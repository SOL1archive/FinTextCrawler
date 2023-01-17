import datetime
import re
from pprint import pprint
from collections import deque
import json

import requests

from Scrapers.BasicScraper import BasicScraper
from utils import *

from items import Tweet

class TwitterScraper(BasicScraper):
    def __init__(self, name='TwitterScraper', spider_designation_path='./spider-designation.yaml'):
        super().__init__(name, spider_designation_path)
        self.consumer_key = self.spider_config['consumer_key']
        self.consumer_secret = self.spider_config['consumer_secret']
        self.access_token = self.spider_config['access_token']
        self.access_token_secret = self.spider_config['access_token_secret']
        self.bear_token = self.spider_config['bearer_token']
        self.max_results = self.spider_config['count']

        self.start_date = self.start_date.astimezone()
        self.end_date = self.end_date.astimezone()
        
        self.query_fields = self.spider_config['query_fields']
        
        self.token_queue = deque()
        self.result = []

    def start_requests(self):
        for search_keyword in self.search_keywords:
            self.keyword_request(search_keyword)        
        for target_keyword in self.target_keywords:
            self.keyword_request('#' + target_keyword)

        # Next Page에 대한 BFS
        while self.token_queue:
            keyword, next_token = self.token_queue.popleft()
            self.keyword_request(target_keyword, next_token)

        return self.result

    def bearer_oauth(self, r):
        """
        Method required by bearer token authentication.
        """

        r.headers["Authorization"] = f"Bearer {self.bear_token}"
        r.headers["User-Agent"] = self.name
        return r

    def keyword_request(self, keyword, next_token=None):
        param_dict = {
                'query': keyword,
                'max_results': self.max_results,
                'start_time': self.start_date.isoformat('T'),
                'end_time': self.end_date.isoformat('T'),
                'tweet.fields': self.query_fields
            }

        if next_token != None:
            param_dict['next_token'] = next_token

        response = requests.get(
            self.start_urls[0],
            params=param_dict,
            auth=self.bearer_oauth
            )

        check_status_code(response)
        
        next_token_queue(self.token_queue, response, keyword)
        self.result.append(self.parse_tweet(response))
        delay(self.delay)

    def parse_tweet(self, response):
        total_tweet = json.loads(response.text)['data']
        for tweet_response in total_tweet:
            tweet = dict()
            tweet['id'] = tweet_response['id']
            tweet['text'] = tweet_response['text']
            tweet['created_at'] = datetime.datetime.strptime(
                tweet_response['created_at'], 
                '%Y-%m-%dT%H:%M:%S.000Z'
                )

        return Tweet(**tweet)
    