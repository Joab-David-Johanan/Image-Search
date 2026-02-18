import streamlit as st
from visionlab.frontend.session import init_session_state
from visionlab.frontend.styles import load_css
from visionlab.frontend.inference_ui import render_inference_section
from visionlab.frontend.search_ui import render_search_section
from visionlab.frontend.display_ui import render_results

# set page config and page title
st.set_page_config(page_title="VisionLab App", layout="wide")
st.title("Computer Vision Search")

# load CSS
load_css()

# init session
init_session_state()

# render UI sections
render_inference_section()
render_search_section()
render_results()
