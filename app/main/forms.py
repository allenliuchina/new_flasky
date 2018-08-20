from flask_wtf import FlaskForm as Form
from wtforms import SubmitField, StringField, TextAreaField, BooleanField, SelectField, ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp
from ..models import Role, User
from flask_pagedown.fields import PageDownField


class NameForm(Form):
    name = StringField("what's your name ", validators=[DataRequired()])
    submit = SubmitField('Submit')


class SubmitForm(Form):
    submit = SubmitField('submit')


class EditProfileForm(Form):
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')


class EditProfileAdminForm(Form):
    email = StringField('Email', validators=[Length(1, 64), DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]$', 0,
                                                                                         'Usernames must have only letter,'
                                                                                         'numbers,dots or underscor')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if self.email != field.data and User.query.filter_by(email=field.data).first():
            raise ValidationError("Email already register")

    def validate_username(self, field):
        if self.username != field.data and User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use')


class PostForm(Form):
    body = PageDownField("What's on your mind?", validators=[DataRequired()])
    submit = SubmitField('Submit')


class CommentForm(Form):
    body = StringField('',validators=[DataRequired()])
    submit = SubmitField('Submit')

