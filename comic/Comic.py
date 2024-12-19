import os
import json

class Comic:
    def __init__(self, title, path, lastСhapter):
        self.title = title
        self.path = path
        self.lastChapter = lastСhapter
    
    def to_dict(self):
        return {
            "title": self.title,
            "path": self.path,
            "lastChapter": self.lastChapter
        }

    @staticmethod
    def from_dict(data):
        return Comic(data["title"], data["path"], data["lastChapter"])    

class ComicService:
    def __init__(self):
        self.file_path = "comics.json"
        self.comics: list[Comic] = self.load_comics()

    def load_comics(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                return [Comic.from_dict(comic) for comic in data]
        return []

    def save_comics(self):
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump([comic.to_dict() for comic in self.comics], file, ensure_ascii=False, indent=4)

    def add_comic(self, comic: Comic):
        self.comics.append(comic)
        self.save_comics()

    def remove_comic(self, title: str):
        self.comics = [comic for comic in self.comics if comic.title != title]
        self.save_comics()

    def get_comics(self):
        return self.comics
    
    def edit_comic(self, updated_comic: Comic):
        for i, comic in enumerate(self.comics):
            if comic.title == updated_comic.title:
                self.comics[i] = updated_comic
                self.save_comics()
                return True
        return False
