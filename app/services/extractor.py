import io
from typing import BinaryIO

from PyPDF2 import PdfReader


def extract_text_from_upload(file_storage, filename: str) -> str:
    """
    Recebe Werkzeug FileStorage.
    """
    ext = filename.rsplit(".", 1)[1].lower()

    data = file_storage.read()
    if ext == "txt":
        # tenta UTF-8; se falhar, latin-1 comum em PT-BR
        try:
            return data.decode("utf-8", errors="ignore").strip()
        except Exception:
            return data.decode("latin-1", errors="ignore").strip()

    if ext == "pdf":
        return _extract_pdf_text(io.BytesIO(data)).strip()

    return ""


def _extract_pdf_text(pdf_stream: BinaryIO) -> str:
    reader = PdfReader(pdf_stream)
    parts = []
    for page in reader.pages:
        txt = page.extract_text() or ""
        parts.append(txt)
    return "\n".join(parts)
