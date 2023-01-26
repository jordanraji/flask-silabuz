from app import db
from datetime import datetime

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(200), nullable=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def to_dict(self):
        post = {
            'post_id': self.id,
            'body': self.body,
            'timestamp': self.timestamp,
            'author_id': self.user_id
        }
        return post

    def from_dict(self, data):
        self.body = data.get('body')
