from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.submission import Submission

from app.schemas.submission import (
    SubmissionResponse,
    OCRResponse,
    ClaimExtractionRequest,
    ClaimExtractionResponse,
    RetrievalResponse,
    VerdictRequest,
    VerdictResponse,
    StanceItem,
)

from app.services.submission_service import (
    create_text_submission,
    create_image_submission,
)

from app.services.ocr_service import extract_text_from_image
from app.services.claim_extraction_service import extract_claim
from app.services.retrieval_service import retrieve_evidence
from app.services.verdict_service import generate_verdict

router = APIRouter(tags=["Submission"])


# =====================================
# Submit Text
# =====================================

@router.post("/text", response_model=SubmissionResponse)
def submit_text(
    text: str = Form(...),
    db: Session = Depends(get_db),
):
    submission = create_text_submission(db, text)

    return SubmissionResponse(
        submission_id=str(submission.id),
        message="Text submitted successfully."
    )


# =====================================
# Submit Image
# =====================================

@router.post("/image", response_model=SubmissionResponse)
def submit_image(
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    submission = create_image_submission(db, image)

    return SubmissionResponse(
        submission_id=str(submission.id),
        message="Image uploaded successfully."
    )


# =====================================
# OCR
# =====================================

@router.post("/ocr", response_model=OCRResponse)
def run_ocr(
    submission_id: str,
    db: Session = Depends(get_db),
):
    submission = (
        db.query(Submission)
        .filter(Submission.id == submission_id)
        .first()
    )

    if submission is None:
        raise HTTPException(
            status_code=404,
            detail="Submission not found."
        )

    if submission.file_path is None:
        raise HTTPException(
            status_code=400,
            detail="This submission has no image."
        )

    extracted_text = extract_text_from_image(
        submission.file_path
    )

    return OCRResponse(
        submission_id=submission_id,
        extracted_text=extracted_text,
    )


# =====================================
# Claim Extraction
# =====================================

@router.post("/claim", response_model=ClaimExtractionResponse)
def claim_extraction(
    request: ClaimExtractionRequest,
):
    result = extract_claim(request.text)

    return ClaimExtractionResponse(
        submission_id=request.submission_id,
        claim=result["claim"],
    )


# =====================================
# Evidence Retrieval
# =====================================

@router.get("/retrieve", response_model=RetrievalResponse)
def retrieve(
    submission_id: str,
    claim: str,
):
    evidence = retrieve_evidence(claim)

    return RetrievalResponse(
        submission_id=submission_id,
        claim=claim,
        evidence=evidence,
    )


# =====================================
# Final Verdict
# =====================================

@router.post("/verdict", response_model=VerdictResponse)
def get_verdict(
    request: VerdictRequest,
):
    evidence_dicts = [
        item.model_dump()
        for item in request.evidence
    ]

    result = generate_verdict(
        claim=request.claim,
        evidence=evidence_dicts,
    )

    return VerdictResponse(
        submission_id=request.submission_id,
        claim=request.claim,
        verdict=result["verdict"],
        fusion_score=result["fusion_score"],
        evidence=[
            StanceItem(**item)
            for item in result["evidence"]
        ],
        explanation=result["explanation"],
    )