from typing import Annotated

from fastapi import Depends

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.posts.data.repositories.database.database_posts_repository import DatabasePostsRepository
from src.posts.domain.repositories.posts_repository import PostsRepository
from src.reactions.data.repositories.mock.reactions_mock_repository import MockReactionsRepository
from src.reactions.domain.interactors.reactions_interactor import ReactionInteractor
from src.reactions.domain.repositories.reactions_repository import ReactionsRepository
from src.settings import get_database_url

from src.posts.domain.interactors.posts_interactor import PostsInteractor
from src.posts.data.repositories.mock.mock_posts_repository import MockPostsRepository

DATABASE_URL = get_database_url()

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncSession:
    async with SessionLocal() as db:
        yield db
        await db.commit()


def database_posts_repository_factory(db: Annotated[AsyncSession, Depends(get_db)]) -> PostsRepository:
    return DatabasePostsRepository(db=db)


def mock_posts_repository_factory() -> PostsRepository:
    return MockPostsRepository()

def mock_reactions_repository_factory() -> ReactionsRepository:
    return MockReactionsRepository()


# posts_repository_factory = database_posts_repository_factory

posts_repository_factory = mock_posts_repository_factory
reactions_repository_factory = mock_reactions_repository_factory


PostsRepositoryDep = Annotated[PostsRepository, Depends(posts_repository_factory)]
ReactionsRepositoryDep = Annotated[ReactionsRepository, Depends(reactions_repository_factory)]


def posts_interactor_factory(posts_repository: PostsRepositoryDep) -> PostsInteractor:
    # Создаем коллбек с привязкой к reaction_interactor
    async def post_deleted_callback(post_id: str) -> None:
        print(f"Пост удален {post_id}")

    return PostsInteractor(posts_repository=posts_repository, on_post_deleted=post_deleted_callback)

def reactions_interactor_factory(reactions_repositoty: ReactionsRepositoryDep) -> ReactionInteractor:
    return ReactionInteractor(reaction_repo=reactions_repositoty)


PostsInteractorDep = Annotated[PostsInteractor, Depends(posts_interactor_factory)]
ReactionsInteractorDep = Annotated[ReactionInteractor, Depends(reactions_interactor_factory)]
