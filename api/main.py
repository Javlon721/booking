import json

import psycopg
from fastapi import FastAPI
from starlette.responses import HTMLResponse

from src.config import settings

app = FastAPI()


@app.get("/")
def read_root():
    return HTMLResponse(content="<h1>Hello Docker Booking Project</h1>", status_code=200)


@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id > 0:
        return {"item_id": item_id}
    raise ValueError('Item id must be greater than 0')


@app.get("/postgres")
def read_postgres():
    with psycopg.connect(host='db', dbname='booking', user='postgres', password='secret') as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT now()')
            now = cur.fetchone()
            return {"now": now}

