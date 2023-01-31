from app import ma
from app.models.user import User

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = False
        load_only = ("password_hash", )
        

    id = ma.auto_field()
    full_name = ma.auto_field()
    email = ma.auto_field()
    username = ma.auto_field()
    description = ma.auto_field()
    password_hash = ma.auto_field()
    posts = ma.auto_field()

user_schema = UserSchema()
users_schema = UserSchema(many=True)
