from ultralytics import YOLO
from pathlib import Path

# this is possible because we added root directory to system path in app.py
from src.config import load_config


class YOLO_V11_Inference:
    def __init__(self, model_name, device="cuda"):
        self.model = YOLO(model=model_name, verbose=True)
        self.device = device
        self.model.to(self.device)

        # loading config from default.yaml
        config = load_config()
        self.conf_threshold = config["model"]["conf_threshold"]
        self.extensions = config["data"]["image_extension"]

    def process_images(self, image_path):
        results = self.model.predict(
            source=image_path,
            conf=self.conf_threshold,
            device=self.device,
        )

        # process results
        detections = []
        class_counts = {}

        for result in results:
            for box in result.boxes:
                cls = result.names[int(box.cls)]
                conf = float(box.conf)
                bbox_coords = box.xyxy[0].tolist()  # [x1, y1, x2, y2]

                # append the detection to the list
                detections.append(
                    {"class": cls, "confidence": conf, "bbox": bbox_coords, "count": 1}
                )

                # update the count for the detected class
                class_counts[cls] = class_counts.get(cls, 0) + 1

        # update the count for each detection in the metadata
        for det in detections:
            det["count"] = class_counts[det["class"]]

        return {
            "image_path": str(image_path),
            "detections": detections,
            "total_objects": len(detections),
            "unique_classes": list(class_counts.keys()),
            "class_counts": class_counts,
        }

    def process_directory(self, directory):
        metadata = []

        patterns = [f"*{ext}" for ext in self.extensions]

        image_paths = []

        for pattern in patterns:
            image_paths.extend(Path(directory).glob(pattern))

        for img_path in image_paths:
            try:
                # add the output of the process_image function in metadata
                metadata.append(self.process_images(image_path=img_path))
            except Exception as e:
                print(f"Error processing {img_path}: {str(e)}")
                continue

        return metadata
