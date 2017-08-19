from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, EqualTo, Regexp
from wtforms import ValidationError

from app.models import User


class LoginForm(FlaskForm):
    email = StringField('登录邮箱', validators=[
                        Required(), Length(1, 64), Email()])
    password = PasswordField('密码', validators=[Required()])
    remember_me = BooleanField('记住我？')
    submit = SubmitField('登录')


class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[
        Required(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, '用户名只能包涵字母，数字，_ 或者 .')])
    email = StringField('邮箱', validators=[
        Required(), Length(1, 64), Email()])
    password = PasswordField('密码', validators=[
        Required(), EqualTo('password2', message='两次密码不一致')])
    password2 = PasswordField('密码确认', validators=[Required()])
    submit = SubmitField('登录')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已注册过')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已注册过')
