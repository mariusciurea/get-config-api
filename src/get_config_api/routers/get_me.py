from fastapi import APIRouter


get_me_router = APIRouter()

@get_me_router.get("/me", tags=["me"])
def get_me():
    return {
        "user": "admin"
    }