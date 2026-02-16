# Intelligent Document Processor

A FastAPI service that accepts image/PDF uploads, runs OCR using Tesseract, stores the extracted text and metadata in SQLite, and allows retrieval by document ID.

This project is intentionally backend-focused and emphasizes correctness, clean structure, and testability.

---

## What it does (current state)

- Upload documents (PNG, JPG, PDF)
- Extract text using Tesseract OCR
- Store OCR output and metadata in SQLite
- Retrieve processed documents by ID
- Unit tests using pytest
- Code quality enforced via pre-commit (black, flake8, mypy)

---

## API Endpoints

### Upload a document
`POST /api/v1/documents/upload`

Processes a document and stores OCR results.

### Get a document
`GET /api/v1/documents/{document_id}`

Returns stored metadata and extracted text.

---

## Tech Stack

- **Backend:** FastAPI
- **Database:** SQLite + SQLAlchemy
- **OCR:** Tesseract (pytesseract)
- **PDF Processing:** pdf2image (Poppler)
- **Testing:** pytest
- **Code Quality:** black, flake8, mypy, pre-commit

---

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/Santoshmohan30/intelligent-doc-processor.git
cd intelligent-doc-processor
```

### 2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 4. Install system dependencies (macOS)
```bash
brew install tesseract poppler
```

Verify installation:
```bash
tesseract --version
```

---

## Run the server
```bash
uvicorn backend.main:app --reload
```

Open Swagger UI:
```
http://127.0.0.1:8000/docs
```

---

## Example Usage

### Upload a document
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/documents/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@test.png"
```

Example response:
```json
{
  "message": "Document processed successfully",
  "document": {
    "id": 1,
    "filename": "test.png",
    "file_type": ".png",
    "file_size": 1543769,
    "extracted_text": "...",
    "processing_time": 0.55,
    "status": "completed",
    "created_at": "2026-02-16T02:22:44.817992"
  }
}
```

### Fetch stored document
```bash
curl http://127.0.0.1:8000/api/v1/documents/1
```

---

## Testing
```bash
pytest -v
```

---

## Project Structure

```
backend/
├── api/
│   ├── routes/documents.py
│   └── models/schemas.py
├── database/
│   ├── models.py
│   └── __init__.py
├── services/
│   └── ocr_service.py
├── main.py
backend/tests/
└── unit/
    ├── test_api.py
    └── test_ocr_service.py
```

---

## Roadmap

- Document classification
- Entity extraction (dates, amounts, names)
- Background processing
- Docker and CI pipeline

---

## Author

**Santosh Mohan Jena**  
GitHub: https://github.com/Santoshmohan30
