from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    user_id = db.Column(db.ForeignKey("user.id"))

    def __repr__(self):
        return f"{self.body}"



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name= db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='user', lazy=True)

    def hash_password(self, original):
        self.password = generate_password_hash(original)

    def check_password(self, original):
        return check_password_hash(self.password, original)


    def __repr__(self):
        return f"<User: {self.email}>"

@login.user_loader
def login_user(id):
    return User.query.get(int(id))
