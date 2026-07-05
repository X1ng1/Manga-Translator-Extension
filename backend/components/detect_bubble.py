from typing import List, Tuple
from ultralytics import YOLO
import torch

# Load the model once at import
model = YOLO("models/best.pt")

def detect_bubbles(image_path: str, conf: float = 0.25) -> List[Tuple[int, int, int, int]]:
    """Run the YOLO bubble detector on an image and return a list of bounding boxes.

    Returns boxes as (x1, y1, x2, y2) integer tuples.
    """
    results = model(image_path, conf=conf)
    boxes: List[Tuple[int, int, int, int]] = []

    for result in results:
        if hasattr(result, "boxes") and result.boxes is not None:
            # result.boxes.xyxy should be convertible to a python list
            try:
                xyxys = result.boxes.xyxy.tolist()
            except Exception:
                # Fallback if the structure is different
                xyxys = [list(map(float, x)) for x in result.boxes.xyxy]

            for xy in xyxys:
                x1, y1, x2, y2 = map(int, xy[:4])
                boxes.append((x1, y1, x2, y2))
    return boxes


if __name__ == "__main__":
    import sys

    img = sys.argv[1] if len(sys.argv) > 1 else "test-images/image02.jpg"
    found = detect_bubbles(img)
    print(f"Detected {len(found)} bubble boxes in {img}")