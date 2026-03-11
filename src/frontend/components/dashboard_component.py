"""Display the dashboard page"""
from email.utils import collapse_rfc2231_value
from selectors import SelectSelector

import streamlit as st
from numpy import ufunc


def render_dashboard_page(data: list[dict]):
    """Render the dashboard page"""

    st.title("Dashboard Config")
    st.caption("Use these filters to get your config data")

    total_network_elements = len(data)
    unique_network_elements = len({ne.get("ne_name") if isinstance(ne, dict) and ne.get("ne_name") else ne for ne in data})
    unique_ips = len({ne.get("om_ip") if isinstance(ne, dict) and ne.get("om_ip") else ne for ne in data})

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Network Elements", total_network_elements)
    col2.metric("Unique Network Elements", unique_network_elements)
    col3.metric("Unique IPs", unique_ips)

    if not data:
        st.warning("There is no data")
        return

    st.dataframe(data, hide_index=True)