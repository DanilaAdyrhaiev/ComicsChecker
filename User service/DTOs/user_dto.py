from dataclasses import dataclass
from typing import Optional

@dataclass
class User_DTO:
    id: Optional[int] = None
    telegram_id: Optional[int] = None
    name: Optional[str] = None
