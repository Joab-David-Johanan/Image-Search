import streamlit as st


def load_css():
    st.markdown(
        """
    <style>

    .block-container {
        max-width: 95%;
        padding-top: 3rem;
    }

    .image-card {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 6px 18px rgba(0,0,0,0.25);
        transition: 0.25s ease;
        margin-bottom: 25px;
        background: #111;
    }

    .image-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 16px 40px rgba(0,0,0,0.45);
    }

    .image-container {
        width: 100%;
        aspect-ratio: 4/3;
        overflow: hidden;
    }

    .image-container img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    .meta-overlay {
        padding: 10px;
        background: rgba(0,0,0,0.9);
        color: white;
        font-size: 13px;
        line-height: 1.4;
        text-align: center;
    }

    </style>
    """,
        unsafe_allow_html=True,
    )
