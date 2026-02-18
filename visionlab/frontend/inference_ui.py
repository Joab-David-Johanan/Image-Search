import streamlit as st
from visionlab.core.inference import YOLO_V11_Inference
from visionlab.core.utils import save_metadata, load_metadata, get_unique_class_counts


def render_inference_section():
    user_option = st.radio(
        "Choose an option: ",
        ("Process new images", "Load existing metadata"),
        horizontal=True,
    )

    if user_option == "Process new images":
        with st.expander("Process new images", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                image_dir = st.text_input(
                    "Image directory path", placeholder=r"path\to\images"
                )
            with col2:
                model_weights = st.text_input("Model weights", "yolo11m.pt")

            if st.button("Start Inference"):
                if image_dir:
                    with st.spinner("Running detection..."):
                        inferencer = YOLO_V11_Inference(model_name=model_weights)
                        metadata = inferencer.process_directory(image_dir)
                        metadata_path = save_metadata(metadata, image_dir)

                        st.success(f"Processed {len(metadata)} images")
                        st.code(str(metadata_path))

                        st.session_state.metadata = metadata
                        (
                            st.session_state.unique_class,
                            st.session_state.class_counts,
                        ) = get_unique_class_counts(metadata)

    else:
        with st.expander("Load existing metadata", expanded=True):
            metadata_file_path = st.text_input(
                "Metadata file path", placeholder=r"path\to\metadata.json"
            )

            if st.button("Load Metadata"):
                metadata = load_metadata(metadata_file_path)
                st.session_state.metadata = metadata
                (
                    st.session_state.unique_class,
                    st.session_state.class_counts,
                ) = get_unique_class_counts(metadata)

                st.success(f"Loaded {len(metadata)} images")
