import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import time
from pathlib import Path


class OCRService:
    def __init__(self):
        self.supported_formats = {".png", ".jpg", ".jpeg", ".pdf"}

    def extract_text(self, file_path: str) -> tuple[str, float]:
        """Extract text from image or PDF. Returns (text, processing_time)"""
        start_time = time.time()
        path = Path(file_path)

        if path.suffix.lower() not in self.supported_formats:
            raise ValueError(f"Unsupported format: {path.suffix}")

        if path.suffix.lower() == ".pdf":
            text = self._extract_from_pdf(file_path)
        else:
            text = self._extract_from_image(file_path)

        processing_time = time.time() - start_time
        return text.strip(), processing_time

    def _extract_from_image(self, file_path: str) -> str:
        image = Image.open(file_path)
        return pytesseract.image_to_string(image)

    def _extract_from_pdf(self, file_path: str) -> str:
        images = convert_from_path(file_path)
        text = ""
        for image in images:
            text += pytesseract.image_to_string(image) + "\n"
        return text
