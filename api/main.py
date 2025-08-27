from fastapi import FastAPI
from starlette.responses import HTMLResponse

from src.auth.router import user_auth_router
from src.db.pool_dependency import ConnectionPoolDepends

app = FastAPI()

app.include_router(user_auth_router)


@app.get("/")
def read_root():
    return HTMLResponse(content="<h1>Hello Docker Booking Project</h1>", status_code=200)


@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id > 0:
        return {"item_id": item_id}
    raise ValueError('Item id must be greater than 0')


@app.get("/postgres")
def read_postgres(conn_pool: ConnectionPoolDepends):
    with conn_pool.getconn() as conn:
        return conn.execute("SELECT * from users_info").fetchone()
