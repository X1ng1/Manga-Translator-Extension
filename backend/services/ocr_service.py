from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Tuple
from PIL import Image
import base64
import io
from manga_ocr import MangaOcr

app = FastAPI()
_mocr = None

def _get_mocr():
    global _mocr
    if _mocr is None:
        _mocr = MangaOcr()
    return _mocr

class OcrRequest(BaseModel):
    image_b64: str
    boxes: List[List[int]]

@app.post("/ocr")
def ocr(req: OcrRequest):
    img_bytes = base64.b64decode(req.image_b64)
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    mocr = _get_mocr()
    results = []
    for box in req.boxes:
        x1, y1, x2, y2 = box
        crop = img.crop((x1, y1, x2, y2))
        text = mocr(crop)
        results.append({"bbox": box, "text": text})
    return results