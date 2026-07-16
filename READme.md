# Manga Translator Extension

A lightweight toolset for extracting text from manga images, detecting and clearing speech bubbles, performing OCR, and translating text back into images. This repository contains a Python backend (OCR & processing services), model assets, and a browser extension for integration.

## Features
- Bubble detection and clearing
- OCR service for extracting text
- Text translation and reinsertion into images
- Browser extension for in-page translation

## Requirements
- Python 3.10+ (recommended)
- GPU (optional) for faster model inference
- See [backend/requirements.txt](backend/requirements.txt#L1) for Python dependencies

## Quick Setup
1. Create and activate virtual environments for the services (examples use PowerShell on Windows):

```powershell
# OCR service (from repo root)
cd backend/services
python -m venv .venv-ocr
.venv-ocr\Scripts\activate
pip install -r ../ocr_requirements.txt

# Main backend (from repo root)
cd ..
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

2. Place required model files in the `models/` and `offload_cache/` directories. This repo includes a `models/best.pt` placeholder and offloaded weights in `offload_cache/`.

## Running

Start the OCR service (port 8001):

```powershell
cd backend/services
.venv-ocr\Scripts\activate
python -m uvicorn ocr_service:app --port 8001
```

Start the main backend (port 8000):

```powershell
cd backend
.venv\Scripts\activate
python -m uvicorn main:app --reload --port 8000
```

## Project Layout

- [backend/](backend/main.py#L1) — FastAPI backend and processing components
	- [backend/components/](backend/components/) — bubble detection, OCR wrapper, translation, and utilities
	- [backend/services/ocr_service.py](backend/services/ocr_service.py#L1) — OCR microservice
	- [backend/requirements.txt](backend/requirements.txt#L1) — Python dependencies
- [extension/](extension/) — Browser extension assets (content scripts, background, manifest)
- [models/](models/) — Model checkpoints
- [offload_cache/](offload_cache/) — Offloaded model weights
- [fonts/](fonts/) — Font assets used when reinserting translated text

## Usage
1. Run the OCR service and the main backend as shown above.
2. Use the browser extension (load `extension/` as an unpacked extension in your browser) to interact with the translation pipeline.