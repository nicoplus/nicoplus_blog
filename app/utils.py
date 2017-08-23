from app.extension import mail, photos

from flask_mail import Message
from flask import render_template, current_app, url_for
from flask_login import current_user
from PIL import Image

import time
import hashlib
import os


def send_email(msg):
    mail.send(msg)


def get_msg(to, subjct, template, **kw):
    msg = Message(current_app.config['FLASK_MAIL_SUBJECT_PREFIX'] + subjct,
                  sender=current_app.config['FLASK_MAIL_SENDER'],
                  recipients=[to])
    msg.body = render_template(template + '.txt', **kw)
    msg.html = render_template(template + '.html', **kw)
    return msg


def create_thumbnail(image):
    '''创建缩略图
       param:
            image:图片的文件名'''
    filename, ext = os.path.splitext(image)
    base_width = 250
    img = Image.open(photos.path(image))
    if img.size[0] <= base_width:
        return photos.url(image)
    w_percent = base_width / float(img.size[0])
    h_size = int(float(img.size[1]) * w_percent)
    img = img.resize((base_width, h_size))
    img.save(os.path.join(
        current_app.config['UPLOADED_PHOTOS_DEST'], filename + '_t' + ext))
    return url_for('main._uploaded_filename',
                   filename=filename + '_t' + ext,
                   _external=True)


def save_image(files):
    '''param:
            files:从request中获得的图片列表,需用files_getlist()。若不是列表，会抛出TypeError
       创建图片名；
       创建缩略图尺寸图.
       warning:
            werkzeug.utils.secure_filename使用ascii编码，不支持中文文件名。
            需修改flask.uploads.extension()'''
    if not isinstance(files, list):
        raise TypeError('param files must be a list')
    images = []
    for img in files:
        filename = hashlib.md5((current_user.username +
                                str(time.time())).encode()).hexdigest()[:10]
        image = photos.save(img, name=filename + '.')
        file_url = photos.url(image)
        file_url_t = create_thumbnail(image)
        images.append((file_url, file_url_t))
    print('images-----------', images)
    return images
