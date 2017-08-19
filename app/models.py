from app.extension import db

from datetime import datetime

import bleach
from markdown import markdown
from flask_login import UserMixin, AnonymousUserMixin
from app.extension import login_manager
from werkzeug.security import check_password_hash, generate_password_hash
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Permissions:
    LIKE = 0x01
    COMMENT = 0X02
    WRITE_ARTICLES = 0x04
    ADMIN = 0x80


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    description = db.Column(db.String(128))
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permissions.LIKE | Permissions.COMMENT, True, 'like, comment',),
            'Operator': (Permissions.LIKE | Permissions.COMMENT | Permissions.WRITE_ARTICLES, False, 'like, comment, wtite article',),
            'Admin': (0xff, False, 'top authority',)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            role.description = roles[r][2]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role: {}>'.format(self.name)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True,
                         nullable=False, index=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    active = db.Column(db.Boolean, default=False)
    role_id = db.Column('Role', db.ForeignKey('roles.id'))

    def __init__(self, **kws):
        super(User, self).__init__(**kws)
        if not self.role:
            if self.email == current_app.config['FLASK_ADMIN']:
                self.role = Role.query.filter_by(permissions=0Xff).first()
            else:
                self.role = Role.query.filter_by(default=True).first()

    def __repr__(self):
        return '<User:{}>'.format(self.username)

    def generate_activation_token(self, expiration=3600):
        s = TimedJSONWebSignatureSerializer(
            current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'activation': self.id})

    def activate(self, token):
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
            #print('data----------', data)
        except Exception as e:
            return False
        if data.get('activation') != self.id:
            #print('不匹配', data.get('activation'), self.id)
            return False
        self.active = True
        db.session.add(self)
        return True

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def password(self):
        raise ValueError('Password is not readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def can(self, permissions):
        return self.role and (self.role.permissions & permissions) == permissions

    def is_admin(self):
        return self.can(Permissions.ADMIN)


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_admin(self):
        return False


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
            markdown(value, output_format='html'), tags=allowed_tags, strip=True))


db.event.listen(Post.body, 'set', Post.on_changed_body)
