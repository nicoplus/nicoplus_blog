from flask import (redirect,
                   url_for,
                   request,
                   send_from_directory,
                   jsonify,
                   current_app)

from app.api_post import api_post
from app.api_post.file import File


@api_post.route('/upload/image', methods=['post'])
def upload_image():
    file = request.files.get('banner-image')
    print('file', file)
    file = File(file, 'api_post.uploaded_image')
    file_urls = file.save()
    print('file_urls: ', file_urls)

    return jsonify({'success': 'success'})


@api_post.route('/uploaded/image/<filename>/')
def uploaded_image(filename):
    return send_from_directory(
        current_app.config['UPLOADED_PHOTOS_DEST'], filename)


@api_post.route('/upload/post', methods=['post'])
def upload_post():
    form = request.get_json()
    title = form.get('title')
    content = form.get('content')

    print('content', content)
    print('title', title)
    return jsonify({'sucess':
                    'received:{}'.format(title)})
