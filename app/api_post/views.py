from flask import (redirect,
                   url_for,
                   request,
                   send_from_directory,
                   jsonify,
                   current_app)

from app.api_post import api_post
from app.api_post.file import File
from app.main.forms import PostForm


@api_post.route('/upload/image', methods=['post'])
def upload_image():
    file = request.files.get('banner-image')
    print('file', file)
    # file = File(file, 'api_post.uploaded_image')
    # file_urls = file.save()
    # print('file_urls: ', file_urls)

    return jsonify({'success': 'success', 'id': '1'})


@api_post.route('/delete/image')
def delete_image():
    image_id = int(request.args.get('id'))
    # delete image by id
    return jsonify({'delete': 'delete image'})


@api_post.route('/uploaded/image/<filename>/')
def uploaded_image(filename):
    return send_from_directory(
        current_app.config['UPLOADED_PHOTOS_DEST'], filename)


@api_post.route('/upload/post', methods=['post'])
def upload_post():
    post_form = PostForm()
    print('headers', current_app.config.get('WTF_CSRF_FIELD_NAME'))
    print('validete', post_form.validate(), post_form.errors)
    if post_form.validate_on_submit():
        return jsonify({'success': 'upload post successfully'})
    return jsonify({'error': 'fail to validete'})
