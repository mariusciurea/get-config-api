from contextlib import asynccontextmanager

from src.get_config_api.settings import get_settings, get_db_settings, ph

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from src.get_config_api.databse.db import get_db

from src.get_config_api.routers.config import config_router
from src.get_config_api.routers.auth import auth_router
from src.get_config_api.routers.get_me import get_me_router
from src.get_config_api.databse.db import Base, engine

from src.get_config_api.databse.db_models import User, NetworkElementConfig

from src.get_config_api.get_data_from_file.file_handlers import JSONFileHandler

settings = get_settings()
db_settings = get_db_settings()


def create_admin_user():
    """Create admin user if not exists"""


    db = next(get_db())

    admin_user = db.query(User).filter(User.username == "admin").first()

    if not admin_user:
        new_admin = User(username="admin", hashed_password=ph.hash("Passwd123"))
        db.add(new_admin)
        db.commit()
        print("Admin user created")
    else:
        print("Admin user already exists")
    db.close()


def load_json_config(db: Session):
    """Load config from json file"""

    config_data = JSONFileHandler().read_file(settings.DATA_DIR / "network_elements_data.json")
    for ne in config_data:
        exists = db.query(NetworkElementConfig).filter_by(ne_name=ne["ne_name"]).first()
        if not exists:
            new_config = NetworkElementConfig(**ne)
            db.add(new_config)
    db.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan event handler"""

    Base.metadata.create_all(bind=engine)
    create_admin_user()

    db = next(get_db())
    load_json_config(db)

    yield


app = FastAPI(lifespan=lifespan)


app.include_router(auth_router)
app.include_router(config_router)
app.include_router(get_me_router)


# http -> get
# http -> post
# http -> put
# http -> delete
# http -> patch

# URL = Uniform Resource Locator
# scheme://host:port/path?query#fragment
# https://api.test.com:443/config?ip=10.111.122.168
