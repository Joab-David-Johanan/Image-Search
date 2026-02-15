import streamlit as st
import sys
from pathlib import Path

# streamlit run app.py --> runs by default on port 8501
# streamlit run app.py --server.port 8080 --> runs by the custom specified port 8080


# add project root to system path
sys.path.append(str(Path(__file__).parent))


# Initialize the session state
def init_session_state():
    session_defaults = {"image_dir": "path"}

    for key, value in session_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_session_state()

# set page config
st.set_page_config(page_title="Computer Vision application", layout="wide")
st.title("Computer Vision Powered Search Application")

# main options that decides app flow
st.radio(
    "Choose an option: ",
    ("Process new images", "Load existing metadata"),
    horizontal=True,
)
