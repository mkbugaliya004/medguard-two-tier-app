import logging
import os

from openai import AsyncOpenAI

logger = logging.getLogger(__name__)

API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("OPENAI_MODEL", "gpt-5.5")

client = (
    AsyncOpenAI(
        api_key=API_KEY,
        timeout=30.0,
        max_retries=1,
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


async def ask_openai(message: str, assessment: dict | None = None) -> str:
    if client is None:
        raise RuntimeError("OpenAI API key is not configured.")

    prompt = message
    if assessment:
        prompt += (
            "\n\nExisting MedGuard assessment result:\n"
            f"{assessment}\n"
            "Explain only the supplied result. "
            "Do not change its risk classification."
        )

    try:
        response = await client.responses.create(
            model=MODEL,
            instructions=SYSTEM_INSTRUCTION,
            input=prompt,
            max_output_tokens=700,
        )
    except Exception as exc:
        logger.exception("OpenAI generation request failed")
        raise RuntimeError(
            "OpenAI is temporarily unavailable. Please try again shortly."
        ) from exc

    answer = response.output_text
    if not answer:
        raise RuntimeError("OpenAI returned an empty response.")

    return answer
