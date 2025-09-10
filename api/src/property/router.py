from fastapi import APIRouter

property_router = APIRouter(prefix="/property", tags=["property"])


@property_router.get("/test")
def test():
    return "test property"
