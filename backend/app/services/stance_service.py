import json
import os

from dotenv import load_dotenv
from fastapi import HTTPException
from google import genai

load_dotenv()

api_key = os.getenv("LLM_API_KEY")

if not api_key:
    raise RuntimeError("LLM_API_KEY not found in .env")

client = genai.Client(api_key=api_key)


STANCE_PROMPT = """
You are a stance classification assistant for a misinformation verification system.

You will receive:
1. One factual claim.
2. A list of evidence items.

For EACH evidence item classify whether it:

- supports
- contradicts
- neutral

Rules:
- Return exactly one result for every evidence item.
- Keep the same order.
- Do NOT judge the overall truth of the claim.
- Only determine the relationship between the claim and the evidence.
- Return ONLY valid JSON.

Claim:
{claim}

Evidence:
{evidence}

Return JSON in this format:

[
  {{
    "stance": "supports",
    "reasoning": "short explanation"
  }}
]
"""


def classify_stances(claim: str, evidence: list[dict]) -> list:
    if not claim.strip():
        raise HTTPException(
            status_code=400,
            detail="Claim cannot be empty",
        )

    if not evidence:
        raise HTTPException(
            status_code=400,
            detail="No evidence provided",
        )

    evidence_text = ""

    for index, item in enumerate(evidence, start=1):
        evidence_text += (
            f"{index}. "
            f"Source: {item.get('source', 'Unknown')}\n"
            f"Text: {item.get('text', '')}\n\n"
        )

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=STANCE_PROMPT.format(
                claim=claim,
                evidence=evidence_text,
            ),
            config={
                "response_mime_type": "application/json"
            },
        )

        raw_text = response.text.strip()

        # Remove Markdown code fences if Gemini still returns them
        if raw_text.startswith("```"):
            raw_text = raw_text.replace("```json", "")
            raw_text = raw_text.replace("```", "")
            raw_text = raw_text.strip()

        print("\n========== STANCE RESPONSE ==========")
        print(raw_text)
        print("=====================================\n")

        parsed = json.loads(raw_text)

        if not isinstance(parsed, list):
            raise HTTPException(
                status_code=500,
                detail="Gemini did not return a JSON array.",
            )

        if len(parsed) != len(evidence):
            raise HTTPException(
                status_code=500,
                detail="Number of stance results does not match evidence count.",
            )

        return parsed

    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail=f"Invalid JSON returned by Gemini:\n{raw_text}",
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Gemini API error: {str(e)}",
        )