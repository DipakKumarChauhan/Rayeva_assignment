"""
Gemini API client wrapper — single entry point for all AI calls.
"""
import json
import re
import google.generativeai as genai
from app.config import settings
from app.logger import AICallTimer

genai.configure(api_key=settings.GEMINI_API_KEY)
_model = genai.GenerativeModel(settings.GEMINI_MODEL)


def call_gemini(module: str, prompt: str) -> str:
    """
    Send a prompt to Gemini and return the text response.
    All calls are logged automatically via AICallTimer.
    """
    with AICallTimer(module=module, prompt=prompt) as timer:
        response = _model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.3,
                max_output_tokens=4096,  # Increased for larger responses
            ),
        )
        timer.response = response.text
    return response.text


def extract_json(text: str) -> dict:
    """
    Extract the first JSON object found in an AI response string.
    Handles cases where Gemini wraps JSON in markdown code fences.
    """
    # Strip markdown code fences if present (handles both opening and closing)
    cleaned = text.strip()
    
    # Remove opening fence (```json or ```)
    cleaned = re.sub(r"^```(?:json)?\s*\n?", "", cleaned, flags=re.MULTILINE)
    
    # Remove closing fence (```)
    cleaned = re.sub(r"\n?```\s*$", "", cleaned, flags=re.MULTILINE)
    
    cleaned = cleaned.strip()

    # Try to find a JSON object
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError as e:
            # Provide more context about why JSON parsing failed
            truncated_text = text[:500] + "..." if len(text) > 500 else text
            raise ValueError(
                f"Invalid JSON in AI response. Parsing error: {e}. "
                f"Response may be truncated. First 500 chars:\n{truncated_text}"
            ) from e

    # If no match found, show truncated response for debugging
    truncated_text = text[:500] + "..." if len(text) > 500 else text
    raise ValueError(f"No valid JSON object found in AI response:\n{truncated_text}")
