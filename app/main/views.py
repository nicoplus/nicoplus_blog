from flask import render_template, redirect, url_for,\
    request, send_from_directory, current_app, flash, jsonify
from flask_login import login_required, current_user

from app.models import Post, Permissions, Image
from . import main
from app.main.forms import PostForm
from app.extension import db
from app.decorators import permission_required, admin_required
from app.utils import save_image
from app.mc import cache


@main.route('/', methods=['GET'])
def index():
    page = request.args.get('page', 1, type=int)
    pagination, posts = get_pagination_posts(page)

    return render_template('index.html', posts=posts, pagination=pagination)


@main.route('/edit_post/', methods=['GET', 'POST'])
@login_required
@permission_required(Permissions.WRITE_ARTICLES)
def edit_post():
    post_form = PostForm()
    post_id = request.args.get('post')
    img_url = None

    if post_form.validate_on_submit() and 'image' in request.files:
        if post_id and Post.query.get(post_id):
            post = Post.query.get(post_id)
            post.title = post_form.title.data
            post.body = post_form.body.data
            img = Image.query.filter_by(post_id=post_id).first()
            images = save_image(request.files.getlist('image'))
            for url in images:
                img.url = url[0]
                img.url_t = url[1]
            db.session.add(img)
            db.session.add(post)
            flash('文章修改成功')
        else:
            post = Post(title=post_form.title.data,
                        body=post_form.body.data,
                        author=current_user._get_current_object())
            db.session.add(post)
            images = save_image(request.files.getlist('image'))
            for url in images:
                img = Image(url=url[0], url_t=url[1], post=post)
                db.session.add(img)
            flash('文章创建成功')

        return redirect(url_for('.index'))

    if post_id:
        post = Post.query.get_or_404(post_id)
        post_form.title.data = post.title
        post_form.body.data = post.body
        img_url = post.images.first().url_t

    return render_template('create_post.html',
                           post_form=post_form, img_url=img_url)


@main.route('/post/<int:id>/', methods=['GET'])
@cache('main', expire=60 * 60)
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html', post=post)


@main.route('/_uploaded/<filename>/')
def _uploaded_filename(filename):
    return send_from_directory(
        current_app.config['UPLOADED_PHOTOS_DEST'], filename)


@main.route('/hide_post/<id>/', methods=[r'PUT'])
@login_required
@admin_required
def hide_post(id):
    post = Post.query.get_or_404(id)
    post.activation = False
    db.session.add(post)
    return jsonify(success='delete success')


@cache('main', expire=30)
def get_pagination_posts(page=1):
    pagination = Post.query.filter_by(activation=True).\
        order_by(Post.created_at.desc()).paginate(
        page,
        per_page=current_app.config['FLASK_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items

    return pagination, posts

