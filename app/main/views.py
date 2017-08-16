from flask import render_template, redirect, url_for, request
from flask_login import login_required

from app.models import Post, User, Permissions
from . import main
from app.main.forms import PostForm
from app.extension import db
from app.decorators import permission_required


@main.after_app_request
def session_commit(resp, *args, **kws):
    db.session.commit()
    return resp


@main.teardown_app_request
def session_remove(exception=None):
    try:
        db.session.remove()
    except Exception as e:
        print(e)
    finally:
        pass


@main.app_template_filter('post_datetime')
def post_datetime(datetime):
    return datetime.strftime('%Y-%m-%d %H:%M')


@main.route('/', methods=['GET'])
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)


@main.route('/edit_post/', methods=['GET', 'POST'])
@login_required
@permission_required(Permissions.WRITE_ARTICLES)
def edit_post():
    post_form = PostForm()
    if post_form.validate_on_submit():
        post = Post(title=post_form.title.data,
                    body=post_form.body.data, author=User.query.get(1))
        db.session.add(post)
        return redirect(url_for('.index'))

    post_id = request.args.get('post')
    if post_id:
        post = Post.query.get_or_404(post_id)
        post_form.title.data = post.title
        post_form.body.data = post.body

    return render_template('create_post.html', post_form=post_form)


@main.route('/post/<int:id>', methods=['GET'])
def post(id):
    post = Post.query.get_or_404(id)
    print(type(post.created_at))
    return render_template('post.html', post=post)
