from typing import Optional
import uuid
from src.posts.domain.repositories.posts_repository import CreatePostRequest, PostsRepository
from src.posts.domain.entities.post import Post

global_storage_posts = {}

class MockPostsRepository(PostsRepository):
    def __init__(self):
        self._posts: dict[str, Post] = global_storage_posts
    
    async def list_posts(self) -> list[Post]:
        """Возвращает список всех постов"""
        return list(self._posts.values())
    
    async def get_post_by_id(self, post_id: str) -> Optional[Post]:
        """Возвращает пост по ID или None если не найден"""
        return self._posts.get(post_id)
    
    async def create_post(self, request: CreatePostRequest) -> Post:
        """Создает новый пост и возвращает его"""
        post_id = str(uuid.uuid4())
        post = Post(
            id=post_id,
            alias=request.alias,
            text=request.text,
        )
        self._posts[post_id] = post
        return post
    
    async def delete_post(self, post_id: str) -> bool:
        """Удаляет пост по ID. Возвращает True если пост был удален, False если не найден"""
        if post_id in self._posts:
            del self._posts[post_id]
            return True
        return False
    
    async def clear(self) -> None:
        """Очищает все посты (удобно для тестирования)"""
        self._posts.clear()