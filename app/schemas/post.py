from app import ma
from app.models.post import Post

class PostSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Post
        load_instance = True
        # load_only = 
        dump_only = ("id", "timestamp", "user_id")
        include_fk = True

    id = ma.auto_field()
    body = ma.auto_field()
    timestamp = ma.auto_field()
    user_id = ma.auto_field()
    user = ma.HyperlinkRelated("api_bp.get_user")

post_schema = PostSchema()
posts_schema = PostSchema(many=True)
posts_schema_update = PostSchema(load_instance=False)
