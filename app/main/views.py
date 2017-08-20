from flask import render_template, redirect, url_for,\
    request, send_from_directory, current_app, flash
from flask_login import login_required, current_user

from app.models import Post, Permissions, Image
from . import main
from app.main.forms import PostForm
from app.extension import db
from app.decorators import permission_required
from app.utils import save_image


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


@main.app_context_processor
def inject_permissions():
    return dict(Permissions=Permissions)


@main.route('/', methods=['GET'])
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)


@main.route('/edit_post', methods=['GET', 'POST'])
@login_required
@permission_required(Permissions.WRITE_ARTICLES)
def edit_post():
    post_form = PostForm()
    if post_form.validate_on_submit() and 'image' in request.files:
        post = Post(title=post_form.title.data,
                    body=post_form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        images = save_image(request.files.getlist('image'))
        for url in images:
            img = Image(url=url[0], url_t=url[1], post=post)
            db.session.add(img)
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


@main.route('/_uploaded/<filename>')
def _uploaded_filename(filename):
    return send_from_directory(
        current_app.config['UPLOADED_PHOTOS_DEST'], filename)
