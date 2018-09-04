from flask_wtf import FlaskForm as Form
from wtforms import SubmitField, StringField, TextAreaField, BooleanField, SelectField, ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp
from ..models import Role, User
from flask_pagedown.fields import PageDownField
from flask_wtf.file import  FileField


class NameForm(Form):
    name = StringField("你的名字 ", validators=[DataRequired()])
    submit = SubmitField('提交')


class SubmitForm(Form):
    submit = SubmitField('提交')


class EditProfileForm(Form):
    name = StringField('真实名字', validators=[Length(0, 64)])
    location = StringField('家乡', validators=[Length(0, 64)])
    about_me = TextAreaField('介绍一下自己吧')
    photo = FileField('你的头像')
    submit = SubmitField('提交')


class EditProfileAdminForm(Form):
    email = StringField('邮箱', validators=[Length(1, 64), DataRequired(), Email()])
    username = StringField('用户名', validators=[Length(1, 64), DataRequired(), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                                                    '用户名只能含有数字、字母、下划线，并且要以字母开头')])
    confirmed = BooleanField('确认')
    role = SelectField('角色', coerce=int)
    name = StringField('真实名字', validators=[Length(0, 64)])
    location = StringField('家乡', validators=[Length(0, 64)])
    about_me = TextAreaField('介绍一下自己把')
    submit = SubmitField('提交')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if self.user.email != field.data and User.query.filter_by(email=field.data).first():
            raise ValidationError("邮箱已经被注册")

    def validate_username(self, field):
        if self.user.username != field.data and User.query.filter_by(username=field.data).first():
            raise ValidationError('这个名字已经有人用了')


class PostForm(Form):
    body = PageDownField("你想写下什么", validators=[DataRequired()])
    submit = SubmitField('发布')


class CommentForm(Form):
    body = StringField('', validators=[DataRequired()])
    submit = SubmitField('发布')
