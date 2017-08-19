import pytest
from flask import current_app

from app import create_app
from app.extension import db
from app import models


class TestBasic:
    @pytest.fixture(scope='function')
    def setup_function(self, request):
        def teardown_function():
            db.session.remove()
            db.drop_all()
            self.app_context.pop()

        request.addfinalizer(teardown_function)
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def test_app_exist(self, setup_function):
        assert current_app is not None

    def test_app_is_testing(self, setup_function):
        assert self.app.config['TESTING'] == True
