import pytest
from flask import current_app

from app import create_app
from app.models import User, Role, Permissions, AnonymousUser
from app.extension import db


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
        assert u.verify_password('cat') == True
        assert u.verify_password('dog') == False

    def test_slat_is_random(self, setup_func):
        u = User(username='john')
        u.password = 'cat'
        u2 = User(username='tom')
        u2.password = 'cat'
        assert u.password_hash != u2.password_hash

    def test_roles_and_permission(self, setup_func):
        u = User(username='john', email='john@qq.com')
        assert u.can(Permissions.COMMENT) == True
        #print(u.role)
        assert u.can(Permissions.WRITE_ARTICLES) == False

    def test_anonymous(self, setup_func):
        u = AnonymousUser()
        assert u.can(Permissions.LIKE) == False
