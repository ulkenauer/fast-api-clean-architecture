
from dataclasses import dataclass
from enum import Enum
from uuid import UUID, uuid4


class ReactionType(Enum):
    LIKE = "like"
    DISLIKE = "dislike"

@dataclass
class Reaction:
    id: UUID
    post_id: UUID
    user_id: UUID
    reaction_type: ReactionType
    
    @classmethod
    def create(cls, post_id: UUID, user_id: UUID, reaction_type: ReactionType) -> "Reaction":
        return cls(id=uuid4(), post_id=post_id, user_id=user_id, reaction_type=reaction_type)