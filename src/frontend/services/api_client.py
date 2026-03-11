"""Client layer for backend API calls"""

import requests

URL = "http://localhost:3333"


def _request(method: str, endpoint: str, **kwargs) -> requests.Response:
    """wrapper around requests.request"""

    url = f"{URL}{endpoint}"

    response = requests.request(method, url, **kwargs)
    response.raise_for_status()

    return response


def _auth_header(token: str) -> dict[str, str]:
    """Authorization header"""
    return {"Authorization": f"Bearer {token}"}


def login(username, password):
    """Login to API"""
    response = _request("POST", "/auth/token", data={"username": username, "password": password}).json()
    return response


def get_all_config(token: str):
    """Request to /config endpoint"""

    response = _request("GET", "/config", headers=_auth_header(token)).json()
    return response


def get_config_by_ip(token: str, ip: str):
    """Request to /config_by_ip endpoint"""

    response = _request("GET", "/config-by-ip", headers=_auth_header(token), params={"ip": ip}).json()
    return response


def get_config_by_network_element(token: str, ne_name: str):
    """Request to /config/{ne_name} endpoint"""

    response = _request("GET", f"/config/{ne_name}", headers=_auth_header(token)).json()
    return response