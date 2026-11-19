
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.openai_service import ask_openai


router = APIRouter(
    prefix="/ai",
    tags=["MedGuard AI"],
)


class AIChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    assessment: dict[str, Any] | None = None


@router.post("/chat")
async def chat_with_medguard_ai(request: AIChatRequest):

    try:
        answer = await ask_gemini(
            message=request.message,
            assessment=request.assessment,
        )

        return {
            "answer": answer,
            "assistant": "MedGuard AI",
            "educational_warning": (
                "Educational prototype using synthetic data only. "
                "AI explanations are not clinical recommendations."
            ),
        }

    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc))

    except Exception:
        raise HTTPException(
            status_code=502,
            detail="Unable to obtain an AI response."
        )
