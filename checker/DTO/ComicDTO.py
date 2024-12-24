import re
import Comi

class ComicDTO:
    def __init__(self, title, path):
        self.title : str = title
        self.path : str = path
        self.chapter = self.getChapter()
    
    def getChapter(self):
        match = re.search(r"(\d+)-glava", self.title)
        if match:
            return int(match.group(1))
        else:
            return 1
    
    def getPath(self):
        return self.title.replace(f"-{self.chapter}-", "-###-")

    def toComic(self):
        return Comic(self.title, self.getPath, self.chapter)