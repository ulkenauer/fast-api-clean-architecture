from src.posts.data.repositories.database.models.post import PostModel
from src.posts.domain.entities.post import Post


class DatabasePostMapper:
    @staticmethod
    def map_post_model_to_entity(model: PostModel) -> Post:
        return Post(
            alias=model.alias,
            id=model.id,
            text=model.text,
        )
