from components.detect_bubble import detect_bubbles, detect_bubbles_uploaded_image
from components.ocr import ocr_bubbles_from_image_path, ocr_bubbles_from_pil
from components.translation import translate_text
from components.clear_bubble import clear_bubble
from components.add_text import add_text
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import multiprocessing
import cv2
from PIL import Image
import io
import numpy as np

multiprocessing.freeze_support()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/process-imgpath")
def process_test_image():
    image_path = "test-images/image04.jpg"
    img = cv2.imread(image_path)
    boxes = detect_bubbles(image_path)
    ocr_results = ocr_bubbles_from_image_path(image_path, boxes)
    print("OCR results:", ocr_results)
    
    translations = translate_text(ocr_results)
    for r in translations:
        print(r["bbox"], r["original"], r["translation"])

    for box in boxes:
        img = clear_bubble(img, box)

    for box, result in zip(boxes, translations):
        img = add_text(img, result["translation"], "fonts/AnimeAce3BB_Regular.otf", result["bbox"])

    cv2.imwrite("test-images/full_output.jpg", img)

@app.post("/process")
async def process_image(image: UploadFile = File(...)):
    print("1. Request received")

    image_bytes = await image.read()
    print("2. Read image")

    pil_img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    print("3. PIL loaded")

    np_img = np.frombuffer(image_bytes, np.uint8)
    cv_img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
    print("4. OpenCV loaded")

    boxes = detect_bubbles_uploaded_image(cv_img)
    print(f"5. Found {len(boxes)} bubbles")

    ocr_results = ocr_bubbles_from_pil(pil_img, boxes)
    print("6. OCR finished")

    translations = translate_text(ocr_results)
    print("7. Translation finished")

    # for box in boxes:
    #     cv_img = clear_bubble(cv_img, box)

    # print("8. Cleared bubbles")

    # for result in translations:
    #     cv_img = add_text(
    #         cv_img,
    #         result["translation"],
    #         "fonts/AnimeAce3BB_Regular.otf",
    #         result["bbox"]
    #     )

    # print("9. Added text")

    # _, encoded = cv2.imencode(".png", cv_img)
    # print("10. Returning response")

    return JSONResponse({
        "translations": translations
    })