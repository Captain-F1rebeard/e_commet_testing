from datetime import date
from typing import List

from fastapi import Query, HTTPException, APIRouter

from github_top_100.models import Repository, Activity
from .database import get_database_connection


router = APIRouter()

@router.get("/api/repos/top100", response_model=List[Repository])
async def get_top_100_repos(
        sort_by: str = Query(None,
                             regex="^(stars|watchers|forks|open_issues)$")
):
    """
    Отображение топ 100 публичных репозиториев.
    Топ составляется по количеству звезд (stars).
    Также имеется возможность сортировки по другим параметрам.
    """
    try:
        async with get_database_connection() as conn:
            if sort_by in ["stars", "watchers", "forks", "open_issues"]:
                query = (f"SELECT repo, owner, position_cur, position_prev,"
                         f" stars, watchers, forks, open_issues, language"
                         f" FROM repos ORDER BY {sort_by} DESC LIMIT 100")
            else:
                query = ("SELECT repo, owner, position_cur, position_prev,"
                         " stars, watchers, forks, open_issues, language"
                         " FROM repos ORDER BY stars DESC LIMIT 100")
            rows = await conn.fetch(query)
        return [Repository(repo=row['repo'],
                            owner=row['owner'],
                            position_cur=row['position_cur'],
                            position_prev=row['position_prev'],
                            stars=row['stars'],
                            watchers=row['watchers'],
                            forks=row['forks'],
                            open_issues=row['open_issues'],
                            language=row['language']
                            ) for row in rows
                ]
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f"Database connection error: {e}")

@router.get("/api/repos/{owner}/{repo}/activity",
         response_model=List[Activity])
async def get_repo_activity(owner: str, repo: str, since: date, until: date):
    """
    Отображение активности репозитория за указанный период (since, until).
    """
    try:
        async with get_database_connection() as conn:
            query = ("SELECT date, commits, authors"
                     "FROM activity"
                     "WHERE owner = $1 AND repo = $2 AND "
                     "date BETWEEN $3 AND $4")
            rows = await conn.fetch(query, owner, repo, since, until)
        return [Activity(date=row['date'],
                         commits=row['commits'],
                         authors=row['authors']
                         ) for row in rows
                ]
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f"Database connection error: {e}")
