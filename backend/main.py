from detect_bubble import detect_bubbles
from ocr import ocr_bubbles_from_image_path
from translation import translate_text
from fastapi import FastAPI
import multiprocessing

multiprocessing.freeze_support()

app = FastAPI()

@app.get("/process")
def process_test_image():
    img = "test-images/image02.jpg"
    boxes = detect_bubbles(img)
    ocr_results = ocr_bubbles_from_image_path(img, boxes)
    print("OCR results:", ocr_results)
    
    translation = translate_text(ocr_results)

    for r in translation:
        print(r["bbox"], r["original"], r["translation"])

    return translation