import io
import base64
from PIL import Image, ImageDraw, ImageFont
import streamlit as st


def img_to_base64(image: Image.Image) -> str:
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()


@st.cache_data(show_spinner=False)
def draw_boxes(
    image_path: str,
    detections: list,
    selected_classes: list,
    show_boxes: bool,
    highlight_matches: bool,
):
    """
    Draw bounding boxes on image and return PIL image.
    Cached for performance.
    """

    img = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(img)

    if not show_boxes:
        return img

    try:
        font = ImageFont.truetype("arial.ttf", 12)
    except:
        font = ImageFont.load_default()

    for det in detections:
        cls = det["class"]
        bbox = det["bbox"]

        # highlight selected classes
        if cls in selected_classes:
            color = "#FF2D2D"
            thickness = 3
        elif not highlight_matches:
            color = "#666666"
            thickness = 1
        else:
            continue

        draw.rectangle(bbox, outline=color, width=thickness)

        label = f"{cls} {det['confidence']:.2f}"
        text_bbox = draw.textbbox((0, 0), label, font=font)
        tw = text_bbox[2] - text_bbox[0]
        th = text_bbox[3] - text_bbox[1]

        draw.rectangle(
            [bbox[0], bbox[1], bbox[0] + tw + 6, bbox[1] + th + 4], fill=color
        )
        draw.text((bbox[0] + 3, bbox[1] + 2), label, fill="white", font=font)

    return img
