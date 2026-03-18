"""Login page"""

import streamlit as st


def render_login_page() -> tuple[str, str, bool]:
    """Renders the login page"""

    st.title("Get Config")
    st.caption("Please authenticate yourself to get access to the dashboard")

    with st.form("login form"):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", placeholder="Enter your password", type="password")
        submitted = st.form_submit_button("Login")

    return username.strip(), password, submitted