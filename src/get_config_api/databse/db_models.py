from sqlalchemy import Column, Integer, String
from src.get_config_api.databse.db import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(100))


class NetworkElementConfig(Base):
    __tablename__ = "network_elements"
    id = Column(Integer, primary_key=True, index=True)
    ne_name = Column(String(100), unique=True, index=True)
    om_ip = Column(String(20))
    lte_ip = Column(String(20))
    enodeb_id = Column(Integer)