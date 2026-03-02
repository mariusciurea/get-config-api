import json

from fastapi import FastAPI, HTTPException
from pydantic import ValidationError

from starlette import status

from src.get_config_api.settings import get_settings
from src.get_config_api.get_data_from_file.file_handlers import JSONFileHandler

from src.get_config_api.data_models.models import NEConfigOutput, NEConfigInput, NEID


settings = get_settings()
config_data = JSONFileHandler().read_file(settings.DATA_DIR / "network_elements_data.json")

app = FastAPI()


@app.get("/config")
def get_all_config():
    return [NEConfigOutput(**ne) for ne in config_data]


@app.get("/config/{ne_name}")
def get_ne_config(ne_name: str):
    try:
        for ne in config_data:
            if ne["ne_name"] == ne_name:
                return NEConfigOutput(**ne)
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ne not found due to {e}")

    return HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.get("/config-by-ip")
def get_ne_config_by_om_ip(ip: str):

    try:
        ne_data = [NEConfigOutput(**ne) for ne in config_data if ne["om_ip"] == ip]
        return ne_data
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.post("/config/{ne_name}")
def add_ne_config(network_element: NEConfigInput):
    ne_data = [ne for ne in config_data if ne["ne_name"] == network_element.ne_name]
    if ne_data:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Ne already exists")

    config_data.append(network_element.model_dump())

    try:
        with open(settings.DATA_DIR / "network_elements_data.json", "w") as f:
            json.dump(config_data, f, indent=4)
    except FileNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return {"message": "Ne added successfully", "data": config_data}


@app.delete("/config/{id}")
def delete_ne_config(network_element: NEID):
    ne_del = [ne for ne in config_data if ne["id"] == network_element.id]
    if not ne_del:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ne {network_element} does not exist")
    print(ne_del)
    with open(settings.DATA_DIR / "network_elements_data.json", "w") as f:
        data = [ne for ne in config_data if ne["id"] != network_element.id]
        json.dump(data, f, indent=4)
    return {"message": "Ne deleted successfully", "data": data}


# http -> get
# http -> post
# http -> put
# http -> delete
# http -> patch

# URL = Uniform Resource Locator
# scheme://host:port/path?query#fragment
# https://api.test.com:443/config?ip=10.111.122.168
