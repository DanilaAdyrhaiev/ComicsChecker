from ComicsLibrary.services import UserService, ComicService
from ComicsLibrary.DTO import UserDTO, ComicDTO


class Orchestrator:
    def __init__(self):
        self.user_service = UserService()
        self.comic_service = ComicService()

    def add_user(self, user: UserDTO):
        return self.user_service.add(user)

    def add_comic(self, comic: ComicDTO):
        return self.comic_service.add(comic)

    def get_comic(self, id=None, title=None):
        if id is not None:
            return self.comic_service.get_by_id(id)
        elif title is not None:
            return self.comic_service.get_by_title(title)
        return None

    def get_user(self, chat_id=None, id=None):
        if id is not None:
            return self.user_service.get_by_id(id)
        elif chat_id is not None:
            return self.user_service.get_by_chat_id(chat_id)
        return None

    def get_comics(self):
        return self.comic_service.get_all()

    def add_comic_to_user(self, comic_id: str, user_id: str):
        comic = self.get_comic(id = comic_id)
        if comic is not None:
            user = self.get_user(id=user_id)
            user.comics.append(comic)
            comic.users.append(user_id)
            return self.comic_service.update(comic)
        else:
            return None