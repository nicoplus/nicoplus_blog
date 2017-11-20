from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import InputRequired, Length, Required, DataRequired
from app.flask_pagedown.fields import PageDownField


class PostForm(FlaskForm):
    image_id = HiddenField(render_kw={'ref': 'imageId'})
    title = StringField('标题', validators=[DataRequired(), Length(
        1, 64)], render_kw={'v-model': 'title', 'ref': 'title'})
    body = PageDownField('正文', validators=[DataRequired()], render_kw={
                         'rows': 10, 'placeholder': '使用markdown语法',
                         'v-model': 'body', 'ref': 'body'})
    submit = SubmitField('提交', render_kw={'@click': 'submit'})
