import pytest

from app import create_app
from app.models import User, Role, Permissions, AnonymousUser
from app.extension import db

import time


class TestUserModel:

    @pytest.fixture(scope='function')
    def setup_func(self, request):
        def teardown_func():
            db.session.remove()
            db.drop_all()
            self.app_context.pop()

        request.addfinalizer(teardown_func)
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()

    def test_password_setter(self, setup_func):
        u = User(username='john')
        u.password = 'cat'
        assert u.password_hash is not None

    def test_no_password_getter(self, setup_func):
        u = User(username='john')
        u.password = 'cat'
        with pytest.raises(ValueError):
            u.password

    def test_verify_password(self, setup_func):
        u = User(username='john')
        u.password = 'cat'
        assert u.verify_password('cat')
        assert not u.verify_password('dog')

    def test_slat_is_random(self, setup_func):
        u = User(username='john')
        u.password = 'cat'
        u2 = User(username='tom')
        u2.password = 'cat'
        assert u.password_hash != u2.password_hash

    def test_roles_and_permission(self, setup_func):
        u = User(username='john', email='john@qq.com')
        assert u.can(Permissions.COMMENT)
        # print(u.role)
        assert not u.can(Permissions.WRITE_ARTICLES)

    def test_anonymous(self):
        u = AnonymousUser()
        assert not u.can(Permissions.LIKE)

    def test_valid_activation_token(self, setup_func):
        u = User(username='john')
        db.session.add(u)
        db.session.commit()
        token = u.generate_activation_token()
        assert u.activate(token)

    def test_invalid_activation_token(self, setup_func):
        u1 = User(username='john')
        u2 = User(username='tom')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        token = u1.generate_activation_token()
        assert not u2.activate(token)

    def test_expired_activation_token(self, setup_func):
        u = User(username='john')
        db.session.add(u)
        db.session.commit()
        token = u.generate_activation_token(1)
        time.sleep(4)
        assert not u.activate(token)
