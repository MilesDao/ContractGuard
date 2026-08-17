from dataclasses import dataclass
from typing import Any, List, Optional

@dataclass(frozen=True)
class ApiResponse:
    """Immutable API Envelope per ECC standards."""
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    meta: Optional[dict] = None
