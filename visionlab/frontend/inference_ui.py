import streamlit as st
from visionlab.core.inference import YOLO_V11_Inference
from visionlab.core.utils import save_metadata, load_metadata, get_unique_class_counts


def render_inference_section():
    with st.sidebar:
        st.header("Inference Section")
        user_option = st.radio(
            "Choose an option: ",
            ("Process new images", "Load existing metadata"),
            horizontal=True,
        )

        if user_option == "Process new images":
            with st.expander("Process new images", expanded=True):

                image_dir = st.text_input(
                    "Image directory path", placeholder=r"path\to\images"
                )

                model_weights = st.selectbox(
                    "Model weights",
                    (
                        "yolo11n.pt",
                        "yolo26n.pt",
                        "yolo11m.pt",
                        "yolo26m.pt",
                        "yolo11x.pt",
                        "yolo26x.pt",
                    ),
                )

                if st.button("Start Inference", type="primary"):
                    if image_dir:
                        with st.spinner("Running detection..."):
                            inferencer = YOLO_V11_Inference(model_name=model_weights)
                            metadata = inferencer.process_directory(image_dir)
                            metadata_path = save_metadata(
                                metadata, image_dir, model_weights
                            )

                            st.success(f"Processed {len(metadata)} images")
                            st.code(str(metadata_path))

                            st.session_state.metadata = metadata
                            (
                                st.session_state.unique_class,
                                st.session_state.class_counts,
                            ) = get_unique_class_counts(metadata)

        else:

            uploaded_metadata = st.file_uploader(
                "Upload metadata file",
                type=["json"],
                accept_multiple_files=False,
            )

            if st.button("Load Metadata", type="primary"):

                if uploaded_metadata is None:
                    st.warning("Please upload metadata file first")
                    st.stop()

                try:
                    metadata = load_metadata(uploaded_metadata)

                    st.session_state.metadata = metadata

                    (
                        st.session_state.unique_class,
                        st.session_state.class_counts,
                    ) = get_unique_class_counts(metadata)

                    st.success(f"Loaded {len(metadata)} images")

                except Exception as e:
                    st.error(str(e))

        st.divider()
