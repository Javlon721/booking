from fastapi import FastAPI
from starlette.responses import HTMLResponse

from src.auth.dependencies import AuthorizeUserDepends
from src.auth.router import auth_router
from src.db.pool_dependency import ConnectionPoolDepends
from src.property.router import property_router
from src.user.router import user_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(property_router)


@app.get("/")
def read_root():
    return HTMLResponse(content="<h1>Hello Docker Booking Project</h1>", status_code=200)


@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id > 0:
        return {"item_id": item_id}
    raise ValueError('Item id must be greater than 0')


@app.get("/postgres", dependencies=[AuthorizeUserDepends])
def read_postgres(conn_pool: ConnectionPoolDepends):
    with conn_pool.connection() as conn:
        return conn.execute("SELECT * from users_info").fetchall()
