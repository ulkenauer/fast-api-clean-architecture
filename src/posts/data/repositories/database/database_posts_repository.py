from sqlalchemy import func
from sqlalchemy.future import select
from src.posts.data.repositories.database.mappers.database_post_mapper import DatabasePostMapper
from src.posts.data.repositories.database.models.post import PostModel
from src.posts.domain.repositories.posts_repository import CreatePostRequest, PostsRepository
from src.posts.domain.entities.post import Post
from sqlalchemy.ext.asyncio import AsyncSession


class DatabasePostsRepository(PostsRepository):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def list_posts(self) -> list[Post]:
        items = (await self.db.execute(select(PostModel))).scalars().all()

        return [DatabasePostMapper.map_post_model_to_entity(item) for item in items]

    async def create_post(self, request: CreatePostRequest) -> None:
        created_object = PostModel(
            alias=request.alias,
            text=request.text,
        )
        self.db.add(created_object)
        await self.db.commit()
