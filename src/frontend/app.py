from operator import ifloordiv

import requests
import streamlit as st
from fastapi.openapi.utils import status_code_ranges
from streamlit.elements.widgets.selectbox import SelectboxSerde

from components.auth_component import render_login_page
from components.dashboard_component import render_dashboard_page
from components.sidebar_component import render_sidebar

from services.api_client import (
    login,
    get_all_config,
    get_config_by_ip,
    get_config_by_network_element
)

from utils.session import (
    init_session_state,
    is_authenticated,
    save_auth_data,
    clear_auth_data
)


URL = "http://localhost:3333"


st.set_page_config(page_title="Get Config", layout="wide")

init_session_state()

def _filtering(token, sidebar_components, all_config):
    if sidebar_components["selected_filter"] == "By OM IP" and sidebar_components["ip_value"]:
        return get_config_by_ip(token, ip=sidebar_components["ip_value"])

    if sidebar_components["selected_filter"] == "By NE" and sidebar_components["ne_values"]:
        return get_config_by_network_element(token, sidebar_components["ne_values"])

    return all_config


def _render_login_screen():
    username, password, submitted = render_login_page()

    if not submitted:
        return

    if not username and password:
        st.error("Username and password are required")
        return

    try:
        # login -> POST /auth/token
        token = login(username, password)
        access_token = token["access_token"]

        if not access_token:
            st.error("Token is missing")
            return

        # save info to session state
        save_auth_data(username, access_token)
        st.success(f"Logged in as {username}")
        st.rerun()

    except requests.HTTPError as err:
        status_code = err.response.status_code if err.response else "N/A"
        st.error(f"Login failed due to {status_code}")
    except Exception as err:
        st.error(err)



def _render_dashboard_screen():
    token = st.session_state["access_token"]
    username = st.session_state["auth_user"]

    try:
        all_config = get_all_config(token)
    except requests.HTTPError as err:
        status_code = err.response.status_code
        if status_code in [401, 403]:

            st.error("Session expired")
            clear_auth_data()
            st.rerun()
        st.error(err)
        return
    except Exception as err:
        st.error(err)
        return

    sidebar_components = render_sidebar(username, all_config)
    try:
        filtered_data = _filtering(token, sidebar_components, all_config)
        render_dashboard_page(filtered_data)
    except requests.HTTPError as err:
        status_code = err.response.status_code if err.response else "N/A"
        st.error(f"No results: {status_code}")



    if sidebar_components["logout"]:
        clear_auth_data()
        st.rerun()



def main_endpoint():
    """Main page"""

    if is_authenticated():
        _render_dashboard_screen()
    else:
        _render_login_screen()


if __name__ == "__main__":
    main_endpoint()