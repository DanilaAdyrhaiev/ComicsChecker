from datetime import datetime
from .BaseEntity import BaseEntity as Entity


class Comic(Entity):
    def __init__(self, _id: str = None, title: str = None, last_chapter_date: datetime = None, users: list[str] = None):
        super().__init__(_id=_id)
        self.title = title
        self.last_chapter_date = last_chapter_date
        self.users = users if users is not None else []

    def to_dict(self):
        return {
            'title': self.title,
            'last_chapter_date': self.last_chapter_date.isoformat() if self.last_chapter_date else None,
            'users': self.users
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            _id=str(data['_id']),
            title=data['title'],
            last_chapter_date=datetime.fromisoformat(data['last_chapter_date']) if data['last_chapter_date'] else None,
            users=data['users']
        )

    def __repr__(self):
        return f'<Comic(Id: {self.id}, Title: {self.title}, LastChapterDate: {self.last_chapter_date}, Users: {self.users})>'

    def __str__(self):
        return f'Comic(Id: {self.id}, Title: {self.title}, LastChapterDate: {self.last_chapter_date}, Users: {self.users})'