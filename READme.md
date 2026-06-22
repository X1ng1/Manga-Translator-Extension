running ocr
.venv-ocr\Scripts\activate
uvicorn ocr_service:app --port 8001

running main app
.venv\Scripts\activate
uvicorn main:app --reload --port 8000