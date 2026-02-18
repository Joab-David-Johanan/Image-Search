import io
import sys
import json
import base64
import streamlit as st
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


from visionlab.core.inference import YOLO_V11_Inference
from visionlab.core.utils import save_metadata, load_metadata, get_unique_class_counts

# streamlit run app.py --> runs by default on port 8501
# streamlit run app.py --server.port 8080 --> runs by the custom specified port 8080

# add project root to system path
sys.path.append(str(Path(__file__).parent))


# add image to HTML
def img_to_base64(image: Image.Image) -> str:
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()


# Initialize the session state
def init_session_state():
    session_defaults = {
        "metadata": None,
        "unique_class": [],
        "class_counts": {},
        "search_results": [],
        "search_params": {
            "search_mode": "Any of the selected classes (OR)",
            "selected_classes": [],
            "thresholds": {},
        },
        "show_boxes": True,
        "grid_columns": 3,
        "highlight_matches": True,
    }

    for key, value in session_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_session_state()

# set page config
st.set_page_config(page_title="Computer Vision application", layout="wide")
st.title("Computer Vision Powered Search Application")

# Custom CSS for perfect grid layout
st.markdown(
    f"""
<style>
/* Main container adjustments */
.st-emotion-cache-1v0mbdj {{
    width: 100% !important;
    height: 100% !important;
}}

/* Column container - critical for grid layout */
.st-emotion-cache-1wrcr25 {{
    max-width: none !important;
    padding: 0 1rem !important;
}}

/* Individual column styling */
.st-emotion-cache-1n76uvr {{
    padding: 0.5rem !important;
}}

/* Image cards */
.image-card {{
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    transition: all 0.3s ease;
    margin-bottom: 20px;
    background: #f8f9fa;
}}

.image-card:hover {{
    transform: translateY(-3px);
    box-shadow: 0 6px 16px rgba(0,0,0,0.15);
}}

.image-container {{
    position: relative;
    width: 100%;
    aspect-ratio: 4/3;
}}

.image-container img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
}}

.meta-overlay {{
    padding: 10px;
    background: rgba(0,0,0,0.85);
    color: white;
    font-size: 13px;
    line-height: 1.4;
}}
</style>
""",
    unsafe_allow_html=True,
)

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

                        # get unique class counts and save in session state for later use in visualization
                        st.session_state.unique_class, st.session_state.class_counts = (
                            get_unique_class_counts(metadata)
                        )

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
                        metadata = load_metadata(metadata_file_path)
                        st.session_state.metadata = metadata
                        st.session_state.unique_class, st.session_state.class_counts = (
                            get_unique_class_counts(metadata)
                        )
                        st.success(
                            f"Successfully loaded metadata for {len(metadata)} images"
                        )
                except Exception as e:
                    st.error(f"Error during metadata loading: str({e})")
            else:
                st.warning("Please enter metadata path")

# search functionality
if st.session_state.metadata:
    st.header("Search Engine")

    with st.container():
        st.session_state.search_params["search_mode"] = st.radio(
            "Search mode: ",
            ("Any of the selected class (OR)", "All selected classes (AND)"),
            horizontal=True,
        )

        # multi select box for selecting multiple classes
        st.session_state.search_params["selected_classes"] = st.multiselect(
            "Classes to search for: ", options=st.session_state.unique_class
        )

        if st.session_state.search_params["selected_classes"]:
            st.subheader("Count thresholds (optional)")
            cols = st.columns(len(st.session_state.search_params["selected_classes"]))
            for i, cls in enumerate(st.session_state.search_params["selected_classes"]):
                with cols[i]:
                    st.session_state.search_params["thresholds"][cls] = st.selectbox(
                        f"Max count for {cls}: ",
                        options=["None"] + st.session_state.class_counts[cls],
                    )

        if (
            st.button("Search Images", type="primary")
            and st.session_state.search_params["selected_classes"]
        ):
            results = []
            search_params = st.session_state.search_params

            for item in st.session_state.metadata:
                matches = False
                class_matches = {}

                for cls in search_params["selected_classes"]:
                    class_detections = [
                        d for d in item["detections"] if d["class"] == cls
                    ]
                    class_count = len(class_detections)
                    class_matches[cls] = False

                    # either show None or threshold number selected by user
                    threshold = search_params["thresholds"].get(cls, "None")
                    if threshold == "None":
                        class_matches[cls] = class_count >= 1
                    else:
                        class_matches[cls] = class_count >= 1 and class_count <= int(
                            threshold
                        )
                        # example 1:
                        # threshold = 4
                        # class_count = 8
                        # then : class_matches[cls] = False
                        # We dont want to show this image

                        # example 2:
                        # threshold = 4
                        # class_count = 2
                        # then : class_matches[cls] = True
                        # We want to show this image

                if search_params["search_mode"] == "Any of selected classes (OR)":
                    # not work only when both are not present or False
                    matches = any(class_matches.values())
                    # 1.jpg
                    # apple : False
                    # banana : True
                    # any(False, true) --> True
                else:  # AND mode
                    # only work when both are present or True
                    matches = all(class_matches.values())
                    # 1.jpg
                    # apple : True
                    # banana : True
                    # any(False, true) --> True

                if matches:
                    results.append(item)

            st.session_state.search_results = results

# Displaying Results

if st.session_state.search_results:
    # redundant code to avoid lengthy variable name
    results = st.session_state.search_results
    search_params = st.session_state.search_params

    st.subheader(f"Results: {len(results)} matching images")

    # Display Controls
    with st.expander("Display Options", expanded=True):
        cols = st.columns(3)
        with cols[0]:
            st.session_state.show_boxes = st.checkbox(
                "Show bounding boxes", value=st.session_state.show_boxes
            )
        with cols[1]:
            st.session_state.grid_columns = st.slider(
                "Grid columns",
                min_value=2,
                max_value=6,
                value=st.session_state.grid_columns,
            )
        with cols[2]:
            st.session_state.highlight_matches = st.checkbox(
                "Highlight matching classes", value=st.session_state.highlight_matches
            )

    # Create the grid using streamlit columns
    grid_cols = st.columns(st.session_state.grid_columns)
    col_index = 0

    for result in results:
        with grid_cols[col_index]:
            try:
                img = Image.open(result["image_path"])
                draw = ImageDraw.Draw(img)

                if st.session_state.show_boxes:
                    try:
                        font = ImageFont.truetype("arial.ttf", 12)
                    except:
                        font = ImageFont.load_default()
                    for det in result["detections"]:
                        cls = det["class"]
                        bbox = det["bbox"]

                        if cls in search_params["selected_classes"]:
                            color = "#F70A0A"
                            # color = "#FF4B4B"
                            thickess = 3
                        elif not st.session_state.highlight_matches:
                            color = "#666666"
                            thickess = 1
                        else:
                            continue

                        draw.rectangle(bbox, outline=color, width=thickess)

                        if (
                            cls in search_params["selected_classes"]
                            or not st.session_state.highlight_matches
                        ):
                            label = f"{cls} {det['confidence']:.2f}"
                            text_bbox = draw.textbbox((0, 0), label, font=font)
                            text_width = text_bbox[2] - text_bbox[0]  # x2-x1
                            text_height = text_bbox[3] - text_bbox[1]  # y2-y1

                            draw.rectangle(
                                [
                                    bbox[0],
                                    bbox[1],
                                    bbox[0] + text_width + 8,
                                    bbox[1] + text_height + 4,
                                ],
                                fill=color,
                            )

                            draw.text(
                                (bbox[0] + 4, bbox[1] + 2),
                                label,
                                fill="white",
                                font=font,
                            )

                meta_items = [
                    f"{k}: {v}"
                    for k, v in result["class_counts"].items()
                    if k in search_params["selected_classes"]
                ]

                # Display card
                st.markdown(
                    f"""
                <div class="image-card">
                    <div class="image-container">
                        <img src="data:image/png;base64,{img_to_base64(img)}">
                    </div>
                    <div class="meta-overlay">
                        <strong>{Path(result['image_path']).name}</strong><br>
                        {", ".join(meta_items) if meta_items else "No matches"}
                    </div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

            except Exception as e:
                st.error(f"Error displaying {result['image_path']} : {str(e)}")

        col_index = (col_index + 1) % st.session_state.grid_columns

    with st.expander("Export Options"):
        st.download_button(
            label="Download Results (JSON)",
            data=json.dumps(results, indent=2),
            file_name="search_results.json",
            mime="application/json",
        )
