"""Session state initialization"""

import streamlit as st
from numpy import ufunc

TOKEN_KEY = "access_token"
USER_KEY = "auth_user"


def init_session_state() -> None:
    """Initialize session state"""
    if TOKEN_KEY not in st.session_state:
        st.session_state[TOKEN_KEY] = None
    if USER_KEY not in st.session_state:
        st.session_state[USER_KEY] = None


def is_authenticated() -> bool:
    """Check if user is authenticated"""
    return st.session_state[TOKEN_KEY] is not None


def save_auth_data(username: str, token: str) -> None:
    """Persist user and token in session state"""

    st.session_state[USER_KEY] = username
    st.session_state[TOKEN_KEY] = token


def clear_auth_data() -> None:
    """Removes user and token from session state"""

    st.session_state[TOKEN_KEY] = None
    st.session_state[USER_KEY] = None