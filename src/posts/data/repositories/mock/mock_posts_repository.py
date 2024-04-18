from src.posts.domain.repositories.posts_repository import PostsRepository
from src.posts.domain.entities.post import Post


class MockPostsRepository(PostsRepository):
    async def list_posts(self) -> list[Post]:
        return [
            Post(
                alias='qwe',
                id='1',
                text='Lorem ipsum'
            )
        ]

    async def create_post(self, request) -> None:
        pass