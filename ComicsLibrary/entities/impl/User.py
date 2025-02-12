from .BaseEntity import BaseEntity as Entity


class User(Entity):
    def __init__(self, _id: str = None,chat_id: int = None, name: str = None, comics: list[str] = None):
        super().__init__(_id=_id)
        self.chat_id = chat_id
        self.name = name
        self.comics = comics

    def to_dict(self):
        return {
            'chat_id': self.chat_id,
            'name': self.name,
            'comics': self.comics
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            _id=str(data['_id']),
            chat_id=data['chat_id'],
            name=data['name'],
            comics=data['comics']
        )
    def __repr__(self):
        return f'<User(Id: {self._id}, Chat_id: {self.chat_id}, Name: {self.name}, Comics: {self.comics})>'

    def __str__(self):
        return f'User(Id: {self._id}, Chat_id: {self.chat_id}, Name: {self.name}, Comics: {self.comics})'
