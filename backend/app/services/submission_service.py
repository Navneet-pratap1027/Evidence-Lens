import os
import uuid

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.models.submission import Submission


UPLOAD_DIR = "uploads"


def create_text_submission(db: Session, text: str):
    submission = Submission(
        submission_type="text",
        text=text,
    )

    db.add(submission)
    db.commit()
    db.refresh(submission)

    return submission


def create_image_submission(db: Session, image: UploadFile):
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    extension = os.path.splitext(image.filename)[1]

    filename = f"{uuid.uuid4()}{extension}"

    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as f:
        f.write(image.file.read())

    submission = Submission(
        submission_type="image",
        file_path=file_path,
    )

    db.add(submission)
    db.commit()
    db.refresh(submission)

    return submission