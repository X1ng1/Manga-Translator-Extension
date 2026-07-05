from typing import List, Tuple, Dict, Union
from PIL import Image
import requests
import base64
import io

OCR_SERVICE_URL = "http://localhost:8001/ocr"

def ocr_bubbles_from_image_path(image_path: str, boxes: List[Tuple[int, int, int, int]]):
    img = Image.open(image_path).convert("RGB")
    return ocr_bubbles_from_pil(img, boxes)

def ocr_bubbles_from_pil(img: Image.Image, boxes: List[Tuple[int, int, int, int]]):
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG")
    img_b64 = base64.b64encode(buffer.getvalue()).decode()

    response = requests.post(OCR_SERVICE_URL, json={
        "image_b64": img_b64,
        "boxes": [list(b) for b in boxes]
    })
    return response.json()