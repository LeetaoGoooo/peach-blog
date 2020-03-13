from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Email


class CommentForm(FlaskForm):
    user_name = StringField('用户名', validators=[DataRequired()],render_kw={"class_":"form-control","placeholder":"昵称(必填)"})
    email = StringField('邮箱', validators=[DataRequired(), Email(message="请确保邮箱有效,以确保可以收到回复")],render_kw={"class_":"form-control","type":"email","placeholder":"邮箱(必填)"})
    website = StringField('网址',render_kw={"class_":"form-control","placeholder":"网址"})
    comment = TextAreaField('', validators=[DataRequired()],render_kw={"class_":"form-control","rows":"3"})
    parent_id = HiddenField()
    submit = SubmitField("评论")