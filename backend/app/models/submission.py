from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.sql import func
import uuid

from app.database.database import Base


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True,
    )

    submission_type = Column(
        String(20),
        nullable=False,
    )  # text | image

    text = Column(
        Text,
        nullable=True,
    )

    file_path = Column(
        String(500),
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )