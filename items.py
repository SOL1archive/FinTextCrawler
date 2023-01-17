# MySQL 인터페이스용 클래스

from dataclasses import dataclass, asdict
import datetime
import re

from utils import *

class Row:
    def __str__(self) -> str:
        return str({k: str(v) for k, v in asdict(self).items()})

    def total_row(self):
        res_str = ''
        row = asdict(self)
        for key in row.keys():
            item = re.sub('\"', r'\"', str(row[key]))
            res_str += ',"' + item + r'"'

        return res_str[1:]

@dataclass
class Article(Row):
    article_id: int
    press_id: int
    title: str
    author: str
    published_datetime: datetime.datetime
    article: str
    useful: int
    wow: int
    touched: int
    analytical: int
    recommend: int

@dataclass
class Tweet(Row):
    id: int
    text: str
    created_at: datetime.datetime

@dataclass
class Community(Row):
    title: str
    created_at: datetime.datetime
    body: str
    views: int
    good: int
    bad: int
