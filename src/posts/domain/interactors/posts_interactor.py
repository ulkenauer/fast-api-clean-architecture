import logging
from typing import Awaitable, Callable, List, Optional
from src.posts.domain.repositories.posts_repository import CreatePostRequest, PostsRepository
from src.posts.domain.entities.post import Post

logger = logging.getLogger(__name__)


class PostsInteractor:
    def __init__(
        self,
        posts_repository: PostsRepository,
        on_post_deleted: Optional[Callable[[str], Awaitable[None]]] = None
    ) -> None:
        self.on_post_deleted = on_post_deleted
        self.posts_repository = posts_repository

    async def list_posts(self) -> List[Post]:
        return await self.posts_repository.list_posts()
    
    async def get_post(self, post_id: str) -> Optional[Post]:
        return await self.posts_repository.get_post_by_id(post_id)

    async def create_post(self, user_id: str, text: str, alias: str) -> None:
        await self.posts_repository.create_post(
            CreatePostRequest(
                alias=alias,
                text=text,
            )
        )
            
    async def delete_post(self, post_id: str) -> None:
        await self.posts_repository.delete_post(post_id)
        if self.on_post_deleted:
            await self.on_post_deleted(post_id)
