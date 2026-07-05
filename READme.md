running ocr
from root
cd backend/services
.venv-ocr\Scripts\activate
uvicorn ocr_service:app --port 8001

running main app
from root
cd backend
.venv\Scripts\activate
uvicorn main:app --reload --port 8000