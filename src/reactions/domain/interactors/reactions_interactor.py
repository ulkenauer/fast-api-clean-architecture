from uuid import UUID
from src.reactions.domain.entities.reaction import Reaction, ReactionType
from src.reactions.domain.repositories.reactions_repository import ReactionsRepository


class ReactionInteractor:
    def __init__(self, reaction_repo: ReactionsRepository):
        self.reaction_repo = reaction_repo
    
    async def add_reaction(self, post_id: UUID, user_id: UUID, reaction_type: ReactionType) -> Reaction:
        reaction = Reaction.create(post_id, user_id, reaction_type)
        await self.reaction_repo.save(reaction)
        return reaction
    
    async def delete_reactions_for_post(self, post_id: UUID) -> None:
        await self.reaction_repo.delete_by_post_id(post_id)
    
    async def get_post_reactions(self, post_id: UUID) -> list[Reaction]:
        return await self.reaction_repo.get_by_post_id(post_id)
    
    async def get_all_reactions(self) -> list[Reaction]:
        return await self.reaction_repo.get_all()