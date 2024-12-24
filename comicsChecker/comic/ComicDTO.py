import re   
from .Comic import Comic

class ComicDTO:
    def __init__(self, title, path):
        self.title : str = title
        self.path : str = path
        self.chapter = self.getChapter()
    
    def getChapter(self):
        match = re.search(r"(\d+)-glava", self.path)
        if match:
            return int(match.group(1))
        else:
            return 1
    
    def getPath(self):
        return self.path.replace(f"-{self.chapter}-", "-###-")

    def toComic(self):
        title = self.title
        path = self.getPath()
        chapter = self.chapter
        return Comic(title, path, chapter)