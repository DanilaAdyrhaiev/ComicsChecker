import os
import json
from typing import List, Optional
from ..comic.Comic import Comic

class User:
    def __init__(self, name: str, chatId: int, comics: Optional[List[Comic]] = None):
        self.name: str = name
        self.chatId: int = chatId
        self.comics: List[Comic] = comics if comics is not None else []

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "chatId": self.chatId,
            "comics": [comic.to_dict() for comic in self.comics]
        }

    @staticmethod
    def from_dict(data: dict) -> 'User':
        comics = [Comic.from_dict(comic_data) for comic_data in data.get("comics", [])]
        return User(data["name"], data["chatId"], comics)


class UserService:
    def __init__(self):
        self.file_path = "users.json"
        self.users: List[User] = self.load_users()

    def load_users(self) -> List[User]:
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                return [User.from_dict(user) for user in data]
        return []

    def save_users(self) -> None:
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump([user.to_dict() for user in self.users], file, ensure_ascii=False, indent=4)

    def add_user(self, user: User) -> None:
        existing_user = self.get_user_by_chat_id(user.chatId)
        if existing_user:
            print(f"Пользователь с chatId={user.chatId} уже существует. Добавление не требуется.")
            return
        self.users.append(user)
        self.save_users()
        print(f"Пользователь с chatId={user.chatId} успешно добавлен.")
        


    def get_user_by_chat_id(self, chat_id: int) -> Optional[User]:
        for user in self.users:
            if user.chatId == chat_id:
                return user
        return None

    def update_user(self, user: User) -> bool:
        for i, existing_user in enumerate(self.users):
            if existing_user.chatId == user.chatId:
                self.users[i] = user
                self.save_users()

    def add_comic(self, chat_id: int, comic: Comic) -> bool:
        user = self.get_user_by_chat_id(chat_id)
        if user:
            user.comics.append(comic)
            self.update_user(user)

    def edit_comic(self, chat_id: int, updated_comic: Comic) -> bool:
        user = self.get_user_by_chat_id(chat_id)
        if user:
            for i, comic in enumerate(user.comics):
                if comic.title == updated_comic.title:
                    user.comics[i] = updated_comic
                    self.update_user(user)
    
global_service = UserService()