from dataclasses import asdict
from typing import List, Sequence, Any
import uuid

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.posts.presentation.http.views.schemas.create_post_schema import CreatePostSchema
from src.reactions.domain.entities.reaction import ReactionType
from src.setup import PostsInteractorDep, ReactionsInteractorDep

router = APIRouter()


@router.get("/posts", response_model=Any)
async def get_posts(posts_interactor: PostsInteractorDep, reactions_interactor: ReactionsInteractorDep) -> Any:
    post_id = uuid.uuid4()
    await reactions_interactor.add_reaction(post_id, uuid.uuid4(), ReactionType.LIKE)
    reaction = await reactions_interactor.get_all_reactions()
    print(reaction)
    return await posts_interactor.list_posts()


@router.post("/posts", response_model=Any)
async def add_post(posts_interactor: PostsInteractorDep, request: CreatePostSchema) -> Any:
    return await posts_interactor.create_post(
        user_id=request.user_id,
        alias=request.alias,
        text=request.text,
    )


@router.delete("/posts/{post_id}", response_model=Any)
async def delete_post(posts_interactor: PostsInteractorDep, post_id: str) -> Any:
    await posts_interactor.delete_post(post_id)
    return {"status": "ok"}

# Роуты ниже включают в себя бизнес-логику компонента реакций
# Они могут быть вынесены в слой приложения. Здесь можно оставить роуты
# которые будут работать только с компонентом постов (добавить также
# простой листинг постов, запрос постов по ID). Но если в конкретном
# приложении нужно возвращать реакции при запросе поста, тогда эти роуты
# не будут использоваться. Вместо них будут использоваться кастомные роуты
@router.get("/posts/{post_id}", response_model=Any)
async def get_post(posts_interactor: PostsInteractorDep, reactions_interactor: ReactionsInteractorDep, post_id: str) -> Any:
    post = await posts_interactor.get_post(post_id)
    reactions = await reactions_interactor.get_post_reactions(uuid.UUID(post_id))
    reactions_dicts = [asdict(reaction) for reaction in reactions]
    result = post.model_dump()
    result["reactions"] = reactions_dicts
    return result

class AddReactionRequest(BaseModel):
    user_id: uuid.UUID
    reaction_type: str

@router.post("/posts/{post_id}/reactions")
async def add_reaction(reactions_interactor: ReactionsInteractorDep, post_id: uuid.UUID, request: AddReactionRequest):
    try:
        reaction_type = ReactionType(request.reaction_type)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid reaction type")

    reaction = await reactions_interactor.add_reaction(
        post_id, request.user_id, reaction_type
    )
    return {"message": "Reaction added", "reaction_id": str(reaction.id)}
