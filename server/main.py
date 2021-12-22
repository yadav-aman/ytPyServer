from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm.session import sessionmaker
import uvicorn
from fastapi_utils.session import FastAPISessionMaker
from fastapi_utils.tasks import repeat_every

from database.main import engine, Base, SQLALCHEMY_DB_URL
from routes import data
from jobs import fetch_yt

app = FastAPI(
    title="Backend Assignment"
)

Base.metadata.create_all(engine)
sessionmaker = FastAPISessionMaker(SQLALCHEMY_DB_URL)

app.include_router(data.router)

origins = ['http://localhost:3000', 'localhost:3000']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


@app.on_event("startup")
@repeat_every(seconds=60)
def ytJob():
    with sessionmaker.context_session() as db:
        fetch_yt.req_yt_api(db)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
