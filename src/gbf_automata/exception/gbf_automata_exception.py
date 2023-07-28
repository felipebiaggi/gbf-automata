from typing import Any, Dict, Optional

class GBFAutomataError(Exception):

    def __init__(self, message: str, /, *, details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message)
        self.details = details  or {}
