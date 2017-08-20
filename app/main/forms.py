from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required, Length
from flask_pagedown.fields import PageDownField
from flask_wtf.file import FileField, FileAllowed, FileRequired

from app.extension import photos


class PostForm(FlaskForm):
    image = FileField('配图', validators=[FileRequired('你还没有上传图片'),
                                        FileAllowed(photos, '只能上传图片')])
    title = StringField('标题', validators=[Required(), Length(1, 64)])
    body = PageDownField('正文', validators=[Required()], render_kw={
                         'rows': 10, 'placeholder': '使用markdown语法'})
    submit = SubmitField('提交')
