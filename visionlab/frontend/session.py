import streamlit as st


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
