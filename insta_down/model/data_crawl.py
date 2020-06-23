from datetime import datetime
from typing import List

from dataclasses import dataclass


@dataclass
class ItemCrawl:
    id: str
    # url of pic
    url: str
    height: int
    width: int
    # thumbnail of pic (if list choose size minimum)
    thumbnail: str
    # count comment of pic
    countComment: int
    # count like of pic
    countLike: int
    # short-code of pic
    shortcode: str


@dataclass
class Owner:
    # id user
    id: str
    # avatar user
    avatar: str
    # username user
    name: str


@dataclass
class DataCrawl:
    id: str
    count: int
    owner: dict
    data: List[dict]
    _expire_at: datetime

@dataclass
class User:
    username: str
    password: str