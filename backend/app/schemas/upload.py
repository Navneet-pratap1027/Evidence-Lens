from pydantic import BaseModel


class UploadResponse(BaseModel):
    filename: str
    saved_path: str
    size_bytes: int
    content_type: str
    status: str = "uploaded"