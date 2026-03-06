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
                max_output_tokens=8192,  # Increased for larger proposal responses
            ),
        )
        timer.response = response.text
    return response.text


def extract_json(text: str) -> dict:
    """
    Extract the first JSON object found in an AI response string.
    Handles cases where Gemini wraps JSON in markdown code fences.
    Also attempts to fix common JSON issues like truncated responses.
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
        json_str = match.group()
        
        # First attempt: try parsing as-is
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            # Second attempt: try to fix common truncation issues
            # If JSON appears incomplete, try to close it properly
            fixed_json = _try_fix_truncated_json(json_str)
            if fixed_json != json_str:
                try:
                    return json.loads(fixed_json)
                except json.JSONDecodeError:
                    pass  # Fall through to error reporting
            
            # Provide detailed error with more context
            error_pos = getattr(e, 'pos', None)
            if error_pos:
                start = max(0, error_pos - 200)
                end = min(len(json_str), error_pos + 200)
                context = json_str[start:end]
                error_msg = (
                    f"Invalid JSON in AI response. Parsing error: {e}. "
                    f"Error position: {error_pos}. "
                    f"Context around error:\n{context}\n\n"
                    f"Full response length: {len(text)} chars. "
                    f"JSON length: {len(json_str)} chars."
                )
            else:
                error_msg = (
                    f"Invalid JSON in AI response. Parsing error: {e}. "
                    f"Full response length: {len(text)} chars. "
                    f"JSON length: {len(json_str)} chars."
                )
            
            # Include full response in error for debugging (truncated if too long)
            if len(text) > 2000:
                error_msg += f"\n\nFirst 1000 chars of response:\n{text[:1000]}..."
            else:
                error_msg += f"\n\nFull response:\n{text}"
            
            raise ValueError(error_msg) from e

    # If no match found, show truncated response for debugging
    truncated_text = text[:1000] + "..." if len(text) > 1000 else text
    raise ValueError(f"No valid JSON object found in AI response:\n{truncated_text}")


def _try_fix_truncated_json(json_str: str) -> str:
    """
    Attempt to fix common JSON truncation issues.
    Returns the original string if no fixes can be applied.
    """
    fixed = json_str.strip()
    
    # Count opening and closing braces
    open_braces = fixed.count('{')
    close_braces = fixed.count('}')
    
    # If we're missing closing braces, try to add them
    if open_braces > close_braces:
        # Check if we're in the middle of a string (don't add braces then)
        if not fixed.rstrip().endswith('"') and not fixed.rstrip().endswith("'"):
            # Try to close arrays first
            open_brackets = fixed.count('[')
            close_brackets = fixed.count(']')
            if open_brackets > close_brackets:
                fixed = fixed.rstrip().rstrip(',') + ']'
            
            # Then close objects
            missing_braces = open_braces - close_braces
            fixed = fixed.rstrip().rstrip(',') + '}' * missing_braces
    
    # Try to close incomplete strings in arrays/objects
    # This is a simple heuristic - if we end with an incomplete string, close it
    if fixed.rstrip().endswith('"') and fixed.count('"') % 2 != 0:
        # Odd number of quotes suggests incomplete string
        pass  # Don't modify, let it fail naturally
    
    return fixed
