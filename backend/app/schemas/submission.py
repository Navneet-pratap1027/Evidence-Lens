from typing import Optional

from pydantic import BaseModel


# ==========================
# Submission
# ==========================

class SubmissionResponse(BaseModel):
    submission_id: str
    message: str


# ==========================
# OCR
# ==========================

class OCRResponse(BaseModel):
    submission_id: str
    extracted_text: str


# ==========================
# Claim Extraction
# ==========================

class ClaimExtractionRequest(BaseModel):
    submission_id: str
    text: Optional[str] = None


class ClaimExtractionResponse(BaseModel):
    submission_id: str
    claim: str


# ==========================
# Retrieval / RAG
# ==========================

class EvidenceItem(BaseModel):
    text: str
    source: str
    url: str
    reliability: float
    similarity: float


class RetrievalResponse(BaseModel):
    submission_id: str
    claim: str
    evidence: list[EvidenceItem]


# ==========================
# Stance Classification
# ==========================

class StanceItem(BaseModel):
    text: str
    source: str
    url: str
    reliability: float
    similarity: float
    stance: str
    stance_reasoning: str


# ==========================
# Verdict
# ==========================

class VerdictRequest(BaseModel):
    submission_id: str
    claim: str
    evidence: list[EvidenceItem]


class VerdictResponse(BaseModel):
    submission_id: str
    claim: str
    verdict: str
    fusion_score: float
    evidence: list[StanceItem]
    explanation: str