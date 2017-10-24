from flask import (current_app,
                   url_for)
from flask_login import current_user
from PIL import Image

import time
import hashlib
import os


class File:

    def __init__(self, file, url_func, upload_folder=None,
                 allowed_extensions=None):
        self.file = file
        self.filename = file.filename
        self.url_func = url_func
        self.raw_name, self.ext = self.filename.rsplit('.', 1)
        self.upload_folder = upload_folder or \
            current_app.config['UPLOAD_FOLDER']
        self.allowed_extensions = allowed_extensions or \
            current_app.config['ALLOWED_EXTENSIONS']

    def allowed_file(self):
        return '.' in self.filename and self.ext in self.allowed_extensions

    def modify_filename(self):
        new_name = hashlib.md5((current_user.username +
                                str(time.time())).encode()).hexdigest()[:10]

        self.filename = '{}.{}'.format(new_name, self.ext)
        self.raw_name = new_name
        return self.filename

    def generate_image_url(self, filename=None):
        filename = filename or self.filename
        url = url_for(self.url_func,
                      filename=filename,
                      _external=True)
        self.url = url
        return url

    def create_thumbnail(self):
        base_width = 250
        img = Image.open(self.file_path)

        if img.size[0] <= base_width:
            return self.url

        w_percent = base_width / float(img.size[0])
        h_size = int(float(img.size[1]) * w_percent)
        img = img.resize((base_width, h_size))
        filename_t = '{}_t.{}'.format(self.raw_name, self.ext)
        img.save(os.path.join(self.upload_folder, filename_t))
        return self.generate_image_url(filename_t)

    def save(self):
        if self.allowed_file():
            self.filename = self.modify_filename()
            self.file_path = os.path.join(self.upload_folder, self.filename)
            self.file.save(self.file_path)

            image_url = self.generate_image_url()
            image_url_t = self.create_thumbnail()
            return (image_url, image_url_t)
        else:
            raise ValueError('file extension is not valid')
