import requests
import json
from typing import Dict, Optional


class GitHubAPIClient:
    """Клиент для работы с GitHub API"""
    
    BASE_URL = "https://api.github.com"
    
    def __init__(self, token: Optional[str] = None):
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/vnd.github.v3+json'
        })
        
        if token:
            self.session.headers.update({
                'Authorization': f'token {token}'
            })
    
    def get_user(self, username: str) -> Dict:
        """
        Получение информации о пользователе GitHub
        
        Args:
            username: Имя пользователя GitHub
            
        Returns:
            Dict: Данные пользователя
            
        Raises:
            Exception: При ошибке запроса или если пользователь не найден
        """
        url = f"{self.BASE_URL}/users/{username}"
        
        try:
            response = self.session.get(url)
            
            if response.status_code == 404:
                raise Exception(f"Пользователь '{username}' не найден")
            elif response.status_code == 403:
                raise Exception("Достигнут лимит запросов к API. Попробуйте позже или используйте токен.")
            elif response.status_code != 200:
                raise Exception(f"Ошибка API: {response.status_code}")
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка соединения: {str(e)}")
    
    def search_users(self, query: str, per_page: int = 10) -> list:
        """
        Поиск пользователей по запросу
        
        Args:
            query: Поисковый запрос
            per_page: Количество результатов на странице
            
        Returns:
            list: Список найденных пользователей
        """
        url = f"{self.BASE_URL}/search/users"
        params = {
            'q': query,
            'per_page': per_page
        }
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get('items', [])
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка при поиске: {str(e)}")
