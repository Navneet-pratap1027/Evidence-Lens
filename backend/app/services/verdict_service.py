from app.services.stance_service import classify_stances


STANCE_SCORE = {
    "supports": 1.0,
    "contradicts": -1.0,
    "neutral": 0.0,
}


def compute_fusion_score(evidence: list[dict]) -> float:
    """
    Weighted fusion score using
    similarity × reliability × stance.
    """

    weighted_sum = 0.0
    total_weight = 0.0

    for item in evidence:

        weight = (
            item["similarity"]
            * item["reliability"]
        )

        stance_value = STANCE_SCORE.get(
            item["stance"],
            0.0,
        )

        weighted_sum += weight * stance_value
        total_weight += weight

    if total_weight == 0:
        return 0.0

    return round(weighted_sum / total_weight, 3)


def map_verdict(
    fusion_score: float,
    evidence: list[dict],
) -> str:
    """
    Convert fusion score into
    final human-readable verdict.
    """

    if not evidence:
        return "Insufficient Evidence"

    supports = sum(
        1
        for e in evidence
        if e["stance"] == "supports"
    )

    contradicts = sum(
        1
        for e in evidence
        if e["stance"] == "contradicts"
    )

    if supports > 0 and contradicts > 0:
        return "Conflicting Evidence"

    if fusion_score >= 0.70:
        return "Verified"

    if fusion_score >= 0.35:
        return "Likely Verified"

    if fusion_score <= -0.70:
        return "Misleading"

    if fusion_score <= -0.35:
        return "Likely Misleading"

    return "Needs Verification"


def generate_explanation(
    claim: str,
    verdict: str,
    evidence: list[dict],
) -> str:

    explanation = []

    explanation.append(
        f'Claim: "{claim}"'
    )

    explanation.append(
        f"Verdict: {verdict}"
    )

    explanation.append("Evidence Summary:")

    for item in evidence:

        explanation.append(
            (
                f"- [{item['stance'].upper()}] "
                f"{item['source']} "
                f"(Similarity={item['similarity']})"
            )
        )

    return "\n".join(explanation)


def generate_verdict(
    claim: str,
    evidence: list[dict],
) -> dict:
    """
    Complete verdict pipeline.

    Claim
        ↓
    Stance Classification
        ↓
    Fusion Score
        ↓
    Verdict
        ↓
    Explainable Report
    """

    stance_results = classify_stances(
        claim,
        evidence,
    )

    enriched = []

    for item, stance in zip(
        evidence,
        stance_results,
    ):

        enriched.append(
            {
                **item,
                "stance": stance["stance"],
                "stance_reasoning": stance["reasoning"],
            }
        )

    fusion_score = compute_fusion_score(
        enriched,
    )

    verdict = map_verdict(
        fusion_score,
        enriched,
    )

    explanation = generate_explanation(
        claim,
        verdict,
        enriched,
    )

    return {
        "verdict": verdict,
        "fusion_score": fusion_score,
        "evidence": enriched,
        "explanation": explanation,
    }