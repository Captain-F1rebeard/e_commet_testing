from datetime import date
from typing import List

from pydantic import BaseModel


class Repository(BaseModel):
    repo: str
    owner: str
    position_cur: int
    position_prev: int
    stars: int
    watchers: int
    forks: int
    open_issues: int
    language: str


class Activity(BaseModel):
    date: date
    commits: int
    authors: List[str]

