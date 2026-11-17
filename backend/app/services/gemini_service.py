
import os

from google import genai
from google.genai import types


API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

client = genai.Client(api_key=API_KEY) if API_KEY else None

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

    response = await client.aio.models.generate_content(
        model=MODEL,
        contents=message + context,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            temperature=0.2,
            max_output_tokens=700,
        ),
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty response.")

    return response.text
