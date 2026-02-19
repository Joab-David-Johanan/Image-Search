import streamlit as st
from pathlib import Path


def render_search_section():
    with st.sidebar:

        if not st.session_state.metadata:
            return

        st.header("Search Section")

        st.success(f"Using: {Path(str(st.session_state.metadata)).stem}")

        with st.container():

            st.session_state.search_params["search_mode"] = st.radio(
                "Search mode",
                ("Any of selected classes (OR)", "All selected classes (AND)"),
                horizontal=False,
            )

            st.session_state.search_params["selected_classes"] = st.multiselect(
                "Classes", options=st.session_state.unique_class
            )

            if st.session_state.search_params["selected_classes"]:
                st.subheader("Count thresholds (optional)")

                for i, cls in enumerate(
                    st.session_state.search_params["selected_classes"]
                ):

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
                            class_matches[cls] = (
                                class_count >= 1 and class_count <= int(threshold)
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

        st.divider()
