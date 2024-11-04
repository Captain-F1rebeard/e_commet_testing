from fastapi import FastAPI

from github_top_100.endpoints import router

app = FastAPI(
    title='GitHub Top 100',
    description='Веб-сервис для просмотра топ 100 репозиториев на GitHub',
    version='0.1.0'
)

app.include_router(router)