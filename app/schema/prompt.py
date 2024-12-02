from pydantic import BaseModel
from typing import Optional


class RequestBodyPrompt(BaseModel):
    prompt: str
    img: Optional[str] = None
