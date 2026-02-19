import json
from pathlib import Path

# "c:\abc\def\image_01000.jpg" ->path.name ---> image_01000.jpg
# path.parent ---> c:\abc\def
# path.parent.parent ---> c:\abc
# path.parent.parent / "processed" / path.parent.name ---> c:\abc\processed\def
# path.parent.parent / "processed" / path.parent.name / (path.stem + "_metadata.json") ---> c:\abc\processed\def\image_01000_metadata.json


# ensure the processed directory exists and return the path to save metadata
def ensure_processed_path(raw_path):
    raw_path = Path(raw_path)
    processed_path = (
        raw_path.parent / "Yolo_image_search" / "processed" / raw_path.parent.name
    )
    processed_path.mkdir(parents=True, exist_ok=True)
    return processed_path


# save metadata to the processed directory with the same name as the raw image
def save_metadata(metadata, raw_path, model_weights):
    processed_path = ensure_processed_path(raw_path)
    # extract model name without path
    model_name = Path(model_weights).stem  # yolo11m.pt → yolo11m
    output_path = processed_path / f"metadata_{model_name}.json"
    with open(output_path, "w") as f:
        json.dump(metadata, f, indent=2)
    return output_path


# process the uploaded metadata from user
def load_metadata(metadata_uploaded):

    if metadata_uploaded is None:
        raise ValueError("No file uploaded")

    try:
        metadata_json = json.load(metadata_uploaded)

        # wrapped format
        if "data" in metadata_json:
            metadata = metadata_json["data"]
        else:
            metadata = metadata_json

        if not isinstance(metadata, list):
            raise ValueError("Invalid metadata format")

        return metadata

    except Exception as e:
        raise ValueError(f"Failed to read metadata: {str(e)}")


# get unique class counts from metadata
def get_unique_class_counts(metadata):

    unique_classes = set()
    class_counts = {}

    for item in metadata:
        for cls in item["detections"]:

            # add the class to the unique_classes set
            unique_classes.add(cls["class"])

            # add the number of images for each class to the class_counts dictionary
            if cls["class"] not in class_counts:
                class_counts[cls["class"]] = set()
            class_counts[cls["class"]].add(cls["count"])

    # order the sets in class_counts and convert to lists, also sort the unique_classes
    unique_classes = sorted(unique_classes)
    for cls in class_counts:
        class_counts[cls] = sorted(class_counts[cls])

    return unique_classes, class_counts
