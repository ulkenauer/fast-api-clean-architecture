from abc import ABC, abstractmethod
from uuid import UUID
from src.reactions.domain.entities.reaction import Reaction


class ReactionsRepository(ABC):
    def __init__(self):
        self.reactions = {}
        self.post_reactions = {}

    @abstractmethod
    async def save(self, reaction: Reaction) -> None:
        pass

    @abstractmethod
    async def delete_by_post_id(self, post_id: UUID) -> None:
        pass

    @abstractmethod
    async def get_by_post_id(self, post_id: UUID) -> list[Reaction]:
        pass
