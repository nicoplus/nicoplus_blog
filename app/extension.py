from flask_bootstrap import Bootstrap
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from flask_pagedown import PageDown
from flask_login import LoginManager
from flask_mail import Mail
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_admin import Admin


bootstrap = Bootstrap()

toolbar = DebugToolbarExtension()

db = SQLAlchemy()

pagedown = PageDown()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
from app.models import AnonymousUser
login_manager.anonymous_user = AnonymousUser

mail = Mail()

photos = UploadSet('photos', IMAGES)

admin = Admin(name='后台系统', template_mode='bootstrap3')
