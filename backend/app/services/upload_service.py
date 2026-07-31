import os
import shutil
import uuid
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.models.submission import Submission
UPLOAD_DIR = "uploads/images"
ALLOWED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
}

MAX_FILE_SIZE_MB = 20


def _validate_extension(filename: str) -> str:
    ext = os.path.splitext(filename)[1].lower()

    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{ext}'. Allowed: {', '.join(sorted(ALLOWED_EXTENSIONS))}",
        )
    return ext
def save_upload(file: UploadFile, db: Session) -> Submission:
    ext = _validate_extension(file.filename)
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    unique_name = f"{uuid.uuid4().hex}{ext}"
    saved_path = os.path.join(UPLOAD_DIR, unique_name)
    with open(saved_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    size_bytes = os.path.getsize(saved_path)
    max_bytes = MAX_FILE_SIZE_MB * 1024 * 1024
    if size_bytes > max_bytes:
        os.remove(saved_path)
        raise HTTPException(
            status_code=400,
            detail=f"File exceeds {MAX_FILE_SIZE_MB}MB limit.",
        )
    submission = Submission(
        submission_type="image",
        file_path=saved_path,
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)
    return submission