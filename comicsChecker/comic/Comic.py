class Comic:
    def __init__(self, title: str, path: str, lastChapter: int):
        self.title: str = title
        self.path: str = path
        self.lastChapter: int = lastChapter

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "path": self.path,
            "lastChapter": self.lastChapter
        }

    @staticmethod
    def from_dict(data: dict) -> 'Comic':
        return Comic(data["title"], data["path"], data["lastChapter"])