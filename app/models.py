from app.extension import db

from datetime import datetime

import bleach
from markdown import markdown
from flask_login import UserMixin
from app.extension import login_manager
from werkzeug.security import check_password_hash, generate_password_hash


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return '<User:{}>'.format(self.username)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def password(self):
        raise ValueError('Password is not readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    body = db.Column(db.Text)
    created_at = db.Column(db.DateTime, index=True, default=datetime.now)
    author_id = db.Column('User', db.ForeignKey('users.id'))
    body_html = db.Column(db.Text)

    def __repr__(self):
        return '<Post:{}>'.format(self.title)

    @staticmethod
    def generate_fake(count=100):
        import forgery_py

        user = User.query.get(1)
        for i in range(count):
            post = Post(body=forgery_py.lorem_ipsum.sentences(3),
                        title=forgery_py.lorem_ipsum.title(),
                        created_at=forgery_py.date.date(True),
                        author=user)
            db.session.add(post)
            db.session.commit()

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        print('change body is running')
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote',
                        'code', 'em', 'i', 'li', 'ol', 'pre',
                        'strong', 'ul', 'h1', 'h2', 'h3', 'p']

        target.body_html = bleach.linkify(bleach.clean(
                                markdown(value, output_format='html'),
                                tags = allowed_tags, strip=True))


db.event.listen(Post.body, 'set', Post.on_changed_body)
