import streamlit as st
from pathlib import Path

from visionlab.frontend.utils_ui import img_to_base64
from visionlab.frontend.utils_ui import draw_boxes  # if using cached box drawing


def render_display():
    if not st.session_state.search_results:
        return

    results = st.session_state.search_results
    search_params = st.session_state.search_params

    st.subheader(f"Results: {len(results)}")

    # display options
    with st.expander("Display Options", expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.session_state.show_boxes = st.checkbox(
                "Show bounding boxes", value=st.session_state.show_boxes
            )
        with c2:
            st.session_state.grid_columns = st.slider(
                "Grid columns", 2, 6, st.session_state.grid_columns
            )
        with c3:
            st.session_state.highlight_matches = st.checkbox(
                "Highlight matches", value=st.session_state.highlight_matches
            )

    grid_cols = st.columns(st.session_state.grid_columns)
    col_index = 0

    for result in results:
        with grid_cols[col_index]:
            try:
                # draw boxes (cached)
                img = draw_boxes(
                    result["image_path"],
                    result["detections"],
                    search_params["selected_classes"],
                    st.session_state.show_boxes,
                    st.session_state.highlight_matches,
                )

                img_b64 = img_to_base64(img)

                meta_items = [
                    f"{k}: {v}"
                    for k, v in result["class_counts"].items()
                    if k in search_params["selected_classes"]
                ]

                st.markdown(
                    f"""
                <div class="image-card">
                    <div class="image-container">
                        <img src="data:image/png;base64,{img_b64}">
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
                st.error(f"Error displaying {result['image_path']}: {str(e)}")

        col_index = (col_index + 1) % st.session_state.grid_columns
