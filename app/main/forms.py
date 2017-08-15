from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required, Length
from flask_pagedown.fields import PageDownField


class PostForm(FlaskForm):
    title = StringField('标题', validators=[Required(), Length(1, 64)])
    body = PageDownField('正文', validators=[Required()])
    submit = SubmitField('Submit')
