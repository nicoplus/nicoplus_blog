from flask_login import login_user, login_required, logout_user, current_user
from flask import redirect, request, url_for, flash, render_template

from app.models import User
from app.auth import auth
from .forms import LoginForm, RegisterForm
from app.extension import db
from app.utils import send_email


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))

        flash('邮箱或者密码有误')
    return render_template('auth/login.html', form=form)


@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('您已成功登出')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_activation_token()
        send_email(user.email, '激活账户',
                   'auth/email/activate', token=token, user=user)
        flash('请登录你的注册邮箱，激活账户')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/activate/<token>', methods=['GET'])
@login_required
def activate(token):
    if current_user.active:
        return redirect(url_for('main.index'))
    if current_user.activate(token):
        flash('成功激活账户')
    else:
        flash('激活链接无效或者已过期')
    return redirect(url_for('main.index'))
