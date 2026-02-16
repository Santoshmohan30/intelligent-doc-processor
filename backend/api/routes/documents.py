from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from pathlib import Path
import shutil

from backend.database import get_db
from backend.database.models import Document
from backend.api.models.schemas import DocumentUploadResponse, DocumentResponse
from backend.services.ocr_service import OCRService

router = APIRouter(prefix="/documents", tags=["documents"])
ocr_service = OCRService()

UPLOAD_DIR = Path("./uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload and process a document"""

    # Validate file type
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ocr_service.supported_formats:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Supported: {ocr_service.supported_formats}",
        )

    # Save file
    file_path = UPLOAD_DIR / file.filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_size = file_path.stat().st_size

    # Extract text
    try:
        extracted_text, processing_time = ocr_service.extract_text(str(file_path))
        status = "completed"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR failed: {str(e)}")

    # Save to database
    doc = Document(
        filename=file.filename,
        file_type=file_ext,
        file_size=file_size,
        extracted_text=extracted_text,
        processing_time=processing_time,
        status=status,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    return DocumentUploadResponse(
        message="Document processed successfully",
        document=DocumentResponse.from_orm(doc),
    )


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(document_id: int, db: Session = Depends(get_db)):
    """Get document by ID"""
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc
