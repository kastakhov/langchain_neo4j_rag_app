import streamlit as st
import json

from streamlit_ace import st_ace

from Chatbot import CHATBOT_URL

from utils.configuration import (
    get_current_configuration,
    update_configuration
)

st.title("App Settings")

with st.sidebar:
    st.header("About")
    st.markdown(
        """
        This page allows you to update the configuration of the chatbot.
        """
    )
current_config = get_current_configuration(CHATBOT_URL)

def editable_json_tree(json_obj):
    st.subheader("Edit Current Configuration")

    estimated_height = len(json.dumps(json_obj, indent=4).splitlines()) * 18
    edited_json = st_ace(
        value=json.dumps(json_obj, indent=4),
        language="json",
        theme="github",
        height=estimated_height,
        key="json_editor"
    )

    if edited_json:
        try:
            return json.loads(edited_json)
        except json.JSONDecodeError:
            st.error("Invalid JSON format. Please correct the errors.")
            return None

    return json_obj

updated_config = editable_json_tree(current_config)

if st.button("Update Configuration"):
    if updated_config:
        update_configuration(CHATBOT_URL, updated_config)
        st.rerun()
    else:
        st.error("Cannot update configuration due to invalid JSON.")
