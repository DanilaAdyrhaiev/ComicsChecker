from .EntityDTO import EntityDTO
from datetime import datetime
from typing import Optional, List
from dataclasses import dataclass

@dataclass
class ComicDTO(EntityDTO):
    id: Optional[str] = None
    title: Optional[str] = None
    last_chapter_date: Optional[datetime] = None
    users: Optional[List[str]] = None