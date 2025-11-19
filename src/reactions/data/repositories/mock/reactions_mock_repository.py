from uuid import UUID
from src.reactions.domain.entities.reaction import Reaction
from src.reactions.domain.repositories.reactions_repository import ReactionsRepository

global_storage_reactions = {}
global_storage_post_reactions = {}

class MockReactionsRepository(ReactionsRepository):
    def __init__(self):
        self.reactions = global_storage_reactions
        self.post_reactions = global_storage_post_reactions
    
    async def save(self, reaction: Reaction) -> None:
        self.reactions[reaction.id] = reaction
        if reaction.post_id not in self.post_reactions:
            self.post_reactions[reaction.post_id] = []
        self.post_reactions[reaction.post_id].append(reaction.id)
    
    async def delete_by_post_id(self, post_id: UUID) -> None:
        if post_id in self.post_reactions:
            for reaction_id in self.post_reactions[post_id]:
                if reaction_id in self.reactions:
                    del self.reactions[reaction_id]
            del self.post_reactions[post_id]
    
    async def get_by_post_id(self, post_id: UUID) -> list[Reaction]:
        reaction_ids = self.post_reactions.get(post_id, [])
        return [self.reactions[rid] for rid in reaction_ids if rid in self.reactions]
    
    async def get_all(self) -> list[Reaction]:
        return self.post_reactions