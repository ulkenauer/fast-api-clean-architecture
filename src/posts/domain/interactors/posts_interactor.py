import logging
from typing import List, Optional
from src.posts.domain.repositories.posts_repository import CreatePostRequest, PostsRepository
from src.posts.domain.entities.post import Post

logger = logging.getLogger(__name__)


class PostsInteractor:
    def __init__(
        self,
        posts_repository: PostsRepository,
        # users_repository: UsersRepository,
    ) -> None:
        self.posts_repository = posts_repository

    async def list_posts(self) -> List[Post]:
        return await self.posts_repository.list_posts()

    async def create_post(self, user_id: str, text: str, alias: str) -> None:
        # user = await users_repository.fetch_by_id(user_id)
        # user_id != "3" == user.is_banned
        if user_id != "3":
            return await self.posts_repository.create_post(
                CreatePostRequest(
                    alias=alias,
                    text=text,
                )
            )
        return None
