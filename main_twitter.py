from pprint import pprint

from SQL_DB import Table
from Scrapers.TwitterScraper import TwitterScraper

scraper = TwitterScraper()
tweets = scraper.start_requests()

tweet_table = Table(db_name="crawl_spc", table_name='twitter', data_list=tweets)
tweet_table.connect()
tweet_table.insert()
tweet_table.commit_close()
