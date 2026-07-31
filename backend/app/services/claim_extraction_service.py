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
EXTRACTION_PROMPT = """
You are a claim-extraction assistant for a misinformation-verification system.
Your ONLY job is to extract the single most important, checkable factual claim from the text below.
Do NOT judge whether it's true or false.
Do NOT add opinions.
Just extract and clarify.
Text (transcript + optional caption):
---
{content}
---
Respond ONLY in this exact JSON format:
{{
  "claim": "<the single clearest checkable factual claim, rewritten as a standalone sentence>",
  "notes": "<1 sentence on why this is the main claim, or 'No clear factual claim found' if none exists>"
}}
"""
def extract_claim(transcript: str, caption: str | None = None) -> dict:
    if not transcript or not transcript.strip():
        raise HTTPException(
            status_code=400,
            detail="No transcript available to extract a claim from",
        )
    combined = transcript.strip()
    if caption:
        combined = f"Caption: {caption.strip()}\nTranscript: {combined}"
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=EXTRACTION_PROMPT.format(content=combined),
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
        print("\n========== GEMINI RESPONSE ==========")
        print(raw_text)
        print("=====================================\n")

        parsed = json.loads(raw_text)
        return {
            "claim": parsed.get("claim", "").strip(),
            "notes": parsed.get("notes", "").strip(),
        }
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