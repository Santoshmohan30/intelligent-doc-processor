from pydantic import BaseModel
from datetime import datetime


class DocumentResponse(BaseModel):
    id: int
    filename: str
    file_type: str
    file_size: int
    extracted_text: str | None
    processing_time: float | None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class DocumentUploadResponse(BaseModel):
    message: str
    document: DocumentResponse
