import json
import os
from typing import Dict, List


class FavoritesManager:
    """Менеджер для работы с избранными пользователями"""
    
    def __init__(self, filename: str = "favorites.json"):
        self.filename = filename
        self.favorites = self._load_favorites()
    
    def _load_favorites(self) -> Dict:
        """Загрузка избранных из файла"""
        if not os.path.exists(self.filename):
            return {}
        
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    
    def _save_favorites(self) -> None:
        """Сохранение избранных в файл"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.favorites, f, ensure_ascii=False, indent=2)
        except IOError as e:
            raise Exception(f"Ошибка сохранения избранных: {str(e)}")
    
    def add_favorite(self, user_data: Dict) -> None:
        """
        Добавление пользователя в избранное
        
        Args:
            user_data: Данные пользователя
        """
        username = user_data.get('login')
        if not username:
            raise ValueError("Отсутствует имя пользователя")
        
        self.favorites[username] = {
            'login': username,
            'name': user_data.get('name', ''),
            'avatar_url': user_data.get('avatar_url', ''),
            'html_url': user_data.get('html_url', ''),
            'added_at': user_data.get('added_at', '')
        }
        
        self._save_favorites()
    
    def remove_favorite(self, username: str) -> None:
        """
        Удаление пользователя из избранного
        
        Args:
            username: Имя пользователя
        """
        if username in self.favorites:
            del self.favorites[username]
            self._save_favorites()
    
    def is_favorite(self, username: str) -> bool:
        """
        Проверка, находится ли пользователь в избранном
        
        Args:
            username: Имя пользователя
            
        Returns:
            bool: True если в избранном
        """
        return username in self.favorites
    
    def get_favorites(self) -> Dict:
        """
        Получение списка избранных пользователей
        
        Returns:
            Dict: Словарь с избранными пользователями
        """
        return self.favorites.copy()
    
    def get_favorite(self, username: str) -> Dict:
        """
        Получение данных избранного пользователя
        
        Args:
            username: Имя пользователя
            
        Returns:
            Dict: Данные пользователя или None
        """
        return self.favorites.get(username)
