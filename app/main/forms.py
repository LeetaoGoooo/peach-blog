from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Email


class CommentForm(FlaskForm):
    user_name = StringField('*用户名', validators=[DataRequired()])
    email = StringField(
        '*邮箱', validators=[DataRequired(), Email(message="请确保邮箱有效,以确保可以收到回复")])
    website = StringField('网址')
    comment = TextAreaField('*评论', validators=[DataRequired()])
    parent_id = HiddenField()
    submit = SubmitField("评论")