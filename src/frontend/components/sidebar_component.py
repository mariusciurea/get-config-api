"""Sidebar component"""

import streamlit as st
from git.config import needs_values


def render_sidebar(username: str | None, all_config: list[dict]):
    """Render the sidebar component"""

    with st.sidebar:
        st.header("Data Filtering")
        st.write(f"User: {username or "unknown"}")

        selected_filter = st.radio(
            "Data filter",
            options=["All NEs", "By NE", "By OM IP"],
            index=0,
        )

        ip_value = st.text_input("IP", placeholder="Enter IP") if selected_filter == "By OM IP" else ""

        ne_options = sorted({ne.get("ne_name") for ne in all_config if ne.get("ne_name")})
        ne_values = (
            st.selectbox("Network Element", options=[""] + ne_options) if selected_filter == "By NE" else ""
        )


        logout_button = st.button("Logout", type="primary")

        return {
            "selected_filter": selected_filter,
            "ip_value": ip_value,
            "ne_values": ne_values,
            "logout": logout_button,
        }