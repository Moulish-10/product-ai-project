import requests
import streamlit as st
from PIL import Image, ImageDraw, ImageFont


# ============================================================
# Configuration
# ============================================================

import os

API_URL = os.getenv(
    "API_URL",
    "http://localhost:8000/predict",
)

# ============================================================
# Page Configuration
# ============================================================

st.set_page_config(
    page_title="SteelVision AI",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# Custom CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 0;
    }

    .subtitle {
        font-size: 18px;
        margin-bottom: 30px;
    }

    .section-title {
        font-size: 24px;
        font-weight: 600;
        margin-top: 10px;
        margin-bottom: 15px;
    }

    .result-card {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid rgba(128,128,128,0.25);
        margin-bottom: 12px;
    }

    .defect-name {
        font-size: 20px;
        font-weight: 600;
    }

    .confidence {
        font-size: 16px;
    }

    .footer {
        text-align: center;
        margin-top: 50px;
        padding-top: 20px;
        border-top: 1px solid rgba(128,128,128,0.25);
        font-size: 14px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# Header
# ============================================================

st.markdown(
    '<div class="main-title">🔍 SteelVision AI</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    "Automated Steel Surface Defect Inspection"
    "</div>",
    unsafe_allow_html=True,
)

st.divider()


# ============================================================
# Helper Functions
# ============================================================

def draw_detections(image, detections):
    """
    Draw bounding boxes, class names and confidence
    values on the image.
    """

    result_image = image.copy()
    draw = ImageDraw.Draw(result_image)

    try:
        font = ImageFont.truetype("arial.ttf", 18)
    except:
        font = ImageFont.load_default()

    for detection in detections:

        class_name = detection["class_name"]
        confidence = detection["confidence"]

        bbox = detection["bbox"]

        x1 = int(bbox["x1"])
        y1 = int(bbox["y1"])
        x2 = int(bbox["x2"])
        y2 = int(bbox["y2"])

        label = f"{class_name} {confidence:.1%}"

        # Bounding box
        draw.rectangle(
            [x1, y1, x2, y2],
            outline="red",
            width=4,
        )

        # Label dimensions
        try:
            text_bbox = draw.textbbox(
                (x1, y1),
                label,
                font=font,
            )

            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]

        except:
            text_width = len(label) * 10
            text_height = 20

        label_y = max(
            0,
            y1 - text_height - 6,
        )

        # Label background
        draw.rectangle(
            [
                x1,
                label_y,
                x1 + text_width + 10,
                label_y + text_height + 6,
            ],
            fill="red",
        )

        # Label text
        draw.text(
            (
                x1 + 5,
                label_y + 3,
            ),
            label,
            fill="white",
            font=font,
        )

    return result_image


def show_detection_card(index, detection):

    class_name = detection["class_name"]
    confidence = detection["confidence"]
    bbox = detection["bbox"]

    st.markdown(
        '<div class="result-card">',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="defect-name">'
        f'🔴 Detection {index}: {class_name}'
        f"</div>",
        unsafe_allow_html=True,
    )

    st.progress(
        min(max(confidence, 0.0), 1.0)
    )

    st.markdown(
        f'<div class="confidence">'
        f"Confidence: <b>{confidence:.2%}</b>"
        f"</div>",
        unsafe_allow_html=True,
    )

    st.caption(
        "Bounding box: "
        f"({bbox['x1']:.1f}, {bbox['y1']:.1f}) → "
        f"({bbox['x2']:.1f}, {bbox['y2']:.1f})"
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )


# ============================================================
# Upload
# ============================================================

uploaded_file = st.file_uploader(
    "Upload a steel surface image",
    type=["jpg", "jpeg", "png"],
)


# ============================================================
# Main Application
# ============================================================

if uploaded_file is not None:

    image = Image.open(uploaded_file).convert("RGB")

    st.divider()

    image_col, result_col = st.columns(
        [1, 1],
        gap="large",
    )

    # --------------------------------------------------------
    # Input Image
    # --------------------------------------------------------

    with image_col:

        st.markdown(
            '<div class="section-title">'
            "📷 Input Image"
            "</div>",
            unsafe_allow_html=True,
        )

        st.image(
            image,
            use_container_width=True,
        )

    # --------------------------------------------------------
    # Prediction
    # --------------------------------------------------------

    with result_col:

        st.markdown(
            '<div class="section-title">'
            "🎯 Inspection"
            "</div>",
            unsafe_allow_html=True,
        )

        predict_clicked = st.button(
            "🔍 Run Inspection",
            type="primary",
            use_container_width=True,
        )

        if predict_clicked:

            with st.spinner(
                "Analyzing steel surface..."
            ):

                try:

                    files = {
                        "file": (
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            uploaded_file.type,
                        )
                    }

                    response = requests.post(
                        API_URL,
                        files=files,
                        timeout=60,
                    )

                    if response.status_code != 200:

                        st.error(
                            "Prediction failed."
                        )

                        st.code(
                            response.text
                        )

                        st.stop()

                    result = response.json()

                    detections = result.get(
                        "detections",
                        [],
                    )

                    # Draw detections
                    annotated_image = draw_detections(
                        image,
                        detections,
                    )

                    st.image(
                        annotated_image,
                        caption="Detection Result",
                        use_container_width=True,
                    )

                    st.divider()

                    # ------------------------------------------------
                    # Metrics
                    # ------------------------------------------------

                    metric1, metric2, metric3 = st.columns(3)

                    with metric1:

                        st.metric(
                            "Detections",
                            result["detection_count"],
                        )

                    with metric2:

                        st.metric(
                            "Inference",
                            f'{result["inference_time_ms"]:.1f} ms',
                        )

                    with metric3:

                        st.metric(
                            "Model",
                            result["model_version"],
                        )

                except requests.exceptions.ConnectionError:

                    st.error(
                        "Cannot connect to the FastAPI server."
                    )

                    st.info(
                        "Make sure the Docker API is running "
                        "on port 8000."
                    )

                except requests.exceptions.Timeout:

                    st.error(
                        "Prediction request timed out."
                    )

                except Exception as e:

                    st.error(
                        f"Unexpected error: {str(e)}"
                    )


# ============================================================
# Detection Details
# ============================================================

if uploaded_file is not None:

    # We only display details after prediction has happened.
    if "result" in locals():

        detections = result.get(
            "detections",
            [],
        )

        st.divider()

        st.markdown(
            '<div class="section-title">'
            "📊 Detection Details"
            "</div>",
            unsafe_allow_html=True,
        )

        if not detections:

            st.info(
                "No defects detected in this image."
            )

        else:

            for index, detection in enumerate(
                detections,
                start=1,
            ):

                show_detection_card(
                    index,
                    detection,
                )


# ============================================================
# Footer
# ============================================================

st.markdown(
    """
    <div class="footer">
        SteelVision AI • AI-powered steel surface defect inspection
    </div>
    """,
    unsafe_allow_html=True,
)

def fetch_prediction_history():
    """Fetch prediction history from FastAPI."""

    try:
        response = requests.get(
            API_URL.replace("/predict", "/predictions"),
            timeout=10,
        )

        if response.status_code != 200:
            return None

        return response.json()

    except requests.exceptions.RequestException:
        return None


# ============================================================
# Prediction History
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">'
    "📜 Prediction History"
    "</div>",
    unsafe_allow_html=True,
)

history = fetch_prediction_history()

if history is None:

    st.warning(
        "Unable to load prediction history."
    )

else:

    predictions = history.get(
        "predictions",
        [],
    )

    if not predictions:

        st.info(
            "No prediction history available yet."
        )

    else:

        for prediction in predictions:

            with st.expander(
                f"#{prediction['id']} — "
                f"{prediction['image_name']}"
            ):

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.write(
                        "**Detections**"
                    )
                    st.write(
                        prediction["detection_count"]
                    )

                with col2:
                    st.write(
                        "**Model**"
                    )
                    st.write(
                        prediction["model_version"]
                    )

                with col3:
                    st.write(
                        "**Inference**"
                    )
                    st.write(
                        f'{prediction["inference_time_ms"]:.2f} ms'
                    )

                with col4:
                    st.write(
                        "**Request ID**"
                    )
                    st.code(
                        prediction["request_id"],
                        language=None,
                    )

                st.caption(
                    f'Created: {prediction["created_at"]}'
                )