from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.posts.domain.entities.post import Post


@dataclass
class CreatePostRequest:
    alias: str
    text: str


class PostsRepository(ABC):
    @abstractmethod
    async def list_posts(self) -> list[Post]:
        pass

    @abstractmethod
    async def get_post_by_id(self, post_id: str) -> list[Post]:
        pass

    @abstractmethod
    async def create_post(self, request: CreatePostRequest) -> None:
        pass

    @abstractmethod
    async def delete_post(self, post_id: str) -> None:
        pass
