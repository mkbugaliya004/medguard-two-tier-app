import logging
import os

from google import genai
from google.genai import types

logger = logging.getLogger(__name__)

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

# Keep each attempt bounded and retry only transient provider/network failures.
# The SDK's attempts value includes the original request.
client = (
    genai.Client(
        api_key=API_KEY,
        http_options=types.HttpOptions(
            timeout=25_000,
            retry_options=types.HttpRetryOptions(
                attempts=2,
                initial_delay=1.0,
                max_delay=2.0,
                exp_base=2.0,
                jitter=0.5,
                http_status_codes=[408, 429, 500, 502, 503, 504],
            ),
        ),
    )
    if API_KEY
    else None
)

SYSTEM_INSTRUCTION = """
You are MedGuard AI, an educational assistant.

You help users:
- Understand antiarrhythmic medications.
- Understand clinical terminology.
- Explain existing MedGuard assessment alerts.
- Understand medication monitoring concepts.

Safety rules:
- Never diagnose patients.
- Never prescribe or recommend dose changes.
- Never override Python medication assessment rules.
- Never claim that a medicine is safe based on an assessment.
- Only explain supplied assessment results.
- Clearly communicate uncertainty.
- Use synthetic data only.
"""


async def ask_gemini(message: str, assessment: dict | None = None):
    if client is None:
        raise RuntimeError("Gemini API key is not configured.")

    context = ""
    if assessment:
        context = (
            "\nExisting MedGuard assessment result:\n"
            f"{assessment}\n"
            "Explain only the supplied result. "
            "Do not change its risk classification."
        )

    try:
        response = await client.aio.models.generate_content(
            model=MODEL,
            contents=message + context,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                max_output_tokens=700,
            ),
        )
    except Exception as exc:
        logger.exception("Gemini generation request failed")
        status_code = getattr(exc, "code", None)

        if status_code in (408, 429, 500, 502, 503, 504):
            raise RuntimeError(
                "Gemini is temporarily unavailable. Please try again shortly."
            ) from exc

        raise

    if not response.text:
        raise RuntimeError("Gemini returned an empty response.")

    return response.text
