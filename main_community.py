from pprint import pprint

from SQL_DB import Table
from Scrapers.CommunityScraper import CommunityScraper

scraper = CommunityScraper()
articles = scraper.start_requests()

article_table = Table(db_name="crawl_kakao", table_name='community', data_list=articles)
article_table.connect()
article_table.insert()
article_table.commit_close()
