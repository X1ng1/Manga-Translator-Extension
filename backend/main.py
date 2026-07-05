from components.detect_bubble import detect_bubbles
from components.ocr import ocr_bubbles_from_image_path
from components.translation import translate_text
from components.clear_bubble import clear_bubble
from components.add_text import add_text
from fastapi import FastAPI
import multiprocessing
import cv2

multiprocessing.freeze_support()

app = FastAPI()

@app.get("/process")
def process_test_image():
    image_path = "test-images/image03.jpg"
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