from typing import List, Sequence, Any

from fastapi import APIRouter

from src.posts.presentation.http.views.schemas.create_post_schema import CreatePostSchema
from src.setup import PostsInteractorDep

router = APIRouter()


@router.get("/posts", response_model=Any)
async def get_posts(posts_interactor: PostsInteractorDep) -> Any:
    return await posts_interactor.list_posts()


@router.post("/posts", response_model=Any)
async def add_post(posts_interactor: PostsInteractorDep, request: CreatePostSchema) -> Any:
    return await posts_interactor.create_post(
        user_id=request.user_id,
        alias=request.alias,
        text=request.text,
    )
