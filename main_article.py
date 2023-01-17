from pprint import pprint

from SQL_DB import Table
from Scrapers.ArticleScraper import ArticleScraper

scraper = ArticleScraper()
articles = scraper.start_requests()

article_table = Table(db_name="crawl_spc", table_name='article', data_list=articles)
article_table.connect()
article_table.insert()
article_table.commit_close()
