from app.extension import admin, db
from app.models import User, Post, Role, Image

from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.base import MenuLink
from flask_login import current_user
from flask import url_for, redirect, request


class MyModelView(ModelView):

    def is_accessible(self):
        return current_user.is_admin()

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login', next=request.url))


class UserModelView(MyModelView):

    column_exclude_list = ['password_hash', ]
    create_modal = True


class PostModelView(MyModelView):

    can_create = False


class ImageModelView(MyModelView):

    can_create = False


class MyMenuLink(MenuLink):

    def __init__(self, name, endpoint=None, *args, **kwargs):

        super(MyMenuLink, self).__init__(name, endpoint=endpoint, **kwargs)

    def get_url(self):
        next = ''
        if self.endpoint == 'auth.login':
            next = request.url
        return self.url or url_for(self.endpoint, next=next)


class AuthenticatedMenuLink(MyMenuLink):

    def is_accessible(self):
        return current_user.is_admin()


class NotAuthenticatedMenuLink(MyMenuLink):

    def is_accessible(self):
        return not current_user.is_admin()


admin.add_view(UserModelView(User, db.session))
admin.add_view(PostModelView(Post, db.session))
admin.add_view(MyModelView(Role, db.session))
admin.add_view(ImageModelView(Image, db.session))
admin.add_link(MyMenuLink(
    name='返回博客', endpoint='main.index'))
admin.add_link(NotAuthenticatedMenuLink(
    name='登录', endpoint='auth.login'))
admin.add_link(AuthenticatedMenuLink(name='登出', endpoint='auth.logout'))
