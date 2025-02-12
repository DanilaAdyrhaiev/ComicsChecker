from .EntityDTO import EntityDTO
from dataclasses import dataclass
from typing import Optional, List


@dataclass
class UserDTO(EntityDTO):
    id: Optional[str] = None
    chat_id: Optional[int] = None
    name: Optional[str] = None
    comics: Optional[List[str]] = None
