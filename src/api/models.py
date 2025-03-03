from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<Users {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email
        }

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('Users', backref=db.backref('posts', lazy=True))

    def __repr__(self):
        return f'<Posts {self.id}>'

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id
        }

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment_text = db.Column(db.String(255), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

    author = db.relationship('Users', backref=db.backref('comments', lazy=True))
    post = db.relationship('Posts', backref=db.backref('comments', lazy=True))

    def __repr__(self):
        return f'<Comments {self.id}>'

    def serialize(self):
        return {
            "id": self.id,
            "comment_text": self.comment_text,
            "author_id": self.author_id,
            "post_id": self.post_id
        }

class Followers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_from_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user_to_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user_from = db.relationship('Users', foreign_keys=[user_from_id], backref=db.backref('following', lazy=True))
    user_to = db.relationship('Users', foreign_keys=[user_to_id], backref=db.backref('followers', lazy=True))

    def __repr__(self):
        return f'<Followers {self.user_from_id} follows {self.user_to_id}>'

    def serialize(self):
        return {
            "id": self.id,
            "user_from_id": self.user_from_id,
            "user_to_id": self.user_to_id
        }
