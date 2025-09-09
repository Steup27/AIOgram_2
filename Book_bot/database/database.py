import json
import os
from typing import Dict, Optional
from dataclasses import dataclass, field
from typing import Set

@dataclass
class User:
    user_id: int
    current_page: int = 1
    bookmarks: Set[int] = field(default_factory=set)

    def to_dict(self) -> dict:
        return {
            'user_id': self.user_id,
            'current_page': self.current_page,
            'bookmarks': list(self.bookmarks)
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        user = cls(
            user_id=data['user_id'],
            current_page=data.get('current_page', 1),
            bookmarks=set(data.get('bookmarks', []))
        )
        return user

class JSONDatabase:
    def __init__(self, users_file: str = 'users.json', users_book: str = 'book/about_book.txt'):
        self.users_file = users_file
        self.users: Dict[int, User] = self._load_users()
        self.users_book = users_book
        self.book: str = self._load_book()

    def _load_users(self) -> Dict[int, User]:
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return {int(user_id): User.from_dict(user_data)
                        for user_id, user_data in data.items()}
        return {}

    def _load_book(self) -> str:
        if os.path.exists(self.users_book):
            with open(self.users_book, 'r', encoding='utf-8') as f:
                return f.read()
        return ''

    def _save_users(self):
        """Сохраняет пользователей в файл"""
        data = {str(user_id): user.to_dict()
                for user_id, user in self.users.items()}
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get_user(self, user_id: int) -> User:
        """Получает пользователя или создает нового"""
        if user_id not in self.users:
            self.users[user_id] = User(user_id=user_id)
            self._save_users()
        return self.users[user_id]

    def save_user(self, user: User):
        """Сохраняет пользователя"""
        self.users[user.user_id] = user
        self._save_users()

    def update_user_page(self, user_id: int, page: int):
        """Обновляет текущую страницу пользователя"""
        user = self.get_user(user_id)
        user.current_page = page
        self.save_user(user)

    def add_bookmark(self, user_id: int, page: int):
        """Добавляет страницу в закладки"""
        user = self.get_user(user_id)
        user.bookmarks.add(page)
        self.save_user(user)

    def remove_bookmark(self, user_id: int, page: int):
        """Удаляет страницу из закладок"""
        user = self.get_user(user_id)
        user.bookmarks.discard(page)  # discard не вызывает ошибку если элемента нет
        self.save_user(user)

def init_db():
    return JSONDatabase()

