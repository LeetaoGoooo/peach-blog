from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email

class CommentForm(FlaskForm):
    user_name = StringField('*用户名', validators=[DataRequired()])
    email = StringField('*邮箱', validators=[DataRequired(),Email(message="请确保邮箱有效😄")])
    website = StringField('网址')
    comment = TextAreaField('*评论', validators=[DataRequired()])
    submit = SubmitField("评论")