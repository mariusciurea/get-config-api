
from fastapi import FastAPI, HTTPException

from src.get_config_api.routers.config import config_router


app = FastAPI()
app.include_router(config_router)



# http -> get
# http -> post
# http -> put
# http -> delete
# http -> patch

# URL = Uniform Resource Locator
# scheme://host:port/path?query#fragment
# https://api.test.com:443/config?ip=10.111.122.168
