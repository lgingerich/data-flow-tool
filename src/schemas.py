from pydantic import BaseModel
from typing import Any, Dict, Optional

class URLInput(BaseModel):
    url: str

class APIResponse(BaseModel):
    metadata: Optional[Dict[str, Any]] = None
    schema: Optional[Dict[str, Any]] = None
    data: Optional[Any] = None
    error: Optional[str] = None
