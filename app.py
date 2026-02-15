import sys
import time
import streamlit as st
from pathlib import Path

from src.inference import YOLO_V11_Inference
from src.utils import save_metadata, load_metadata, get_unique_class_counts

# streamlit run app.py --> runs by default on port 8501
# streamlit run app.py --server.port 8080 --> runs by the custom specified port 8080

# add project root to system path
sys.path.append(str(Path(__file__).parent))


# Initialize the session state
def init_session_state():
    session_defaults = {"metadata": None}

    for key, value in session_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_session_state()

# set page config
st.set_page_config(page_title="Computer Vision application", layout="wide")
st.title("Computer Vision Powered Search Application")

# main options that decides app flow
user_option = st.radio(
    "Choose an option: ",
    ("Process new images", "Load existing metadata"),
    horizontal=True,
)

if user_option == "Process new images":
    with st.expander("Process new images", expanded=True):

        # creating the two columns with text inputs
        col1, col2 = st.columns(2)
        with col1:
            image_dir = st.text_input(
                "Image directory path: ", placeholder=r"path\to\images"
            )
        with col2:
            model_weights = st.text_input("Model weights path: ", "yolo11m.pt")

        # button for processing
        if st.button("Start Inference"):
            if image_dir:
                try:
                    with st.spinner("Running object detection..."):

                        # create an instance of Yolo_v11_inference
                        inferencer = YOLO_V11_Inference(model_name=model_weights)
                        # run inference on the image directory and get metadata
                        metadata = inferencer.process_directory(image_dir)
                        # save metadata to the processed directory
                        metadata_path = save_metadata(metadata, image_dir)
                        # display success message with the number of processed images and metadata path
                        st.success(
                            f"Processed {len(metadata)} images. Metadata saved to:"
                        )
                        st.code(str(metadata_path))

                        # save the metadata in session state
                        st.session_state.metadata = metadata

                except Exception as e:
                    st.error(f"Error during inference: str({e})")
            else:
                st.warning("Please enter an image directory path")

else:
    with st.expander("Load existing metadata", expanded=True):
        metadata_file_path = st.text_input(
            "Metadata file path: ", placeholder=r"path\to\metadata.json"
        )

        # button for processing
        if st.button("Load Metadata"):
            if metadata_file_path:
                try:
                    with st.spinner("Loading model metadata..."):
                        time.sleep(3)
                        st.success("Loaded metadata.")
                except Exception as e:
                    st.error(f"Error during metadata loading: str({e})")
            else:
                st.warning("Please enter metadata path")
