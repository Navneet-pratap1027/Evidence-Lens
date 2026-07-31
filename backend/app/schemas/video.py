from datetime import datetime
from pydantic import BaseModel


class VideoStatusResponse(BaseModel):
    id: str
    filename: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class FrameExtractionResponse(BaseModel):
    video_id: str
    status: str
    frame_count: int
    frames_dir: str


class TranscriptionResponse(BaseModel):
    video_id: str
    status: str
    transcript: str
    language: str


class ClaimExtractionRequest(BaseModel):
    caption: str | None = None


class ClaimExtractionResponse(BaseModel):
    video_id: str
    claim: str
    notes: str