from flask_wtf import FlaskForm as Form
from wtforms import SubmitField,StringField,validators
from wtforms.validators import DataRequired

class NameForm(Form):
    name = StringField("what's your name ", validators=[DataRequired()])
    submit = SubmitField('Submit')


class SubmitForm(Form):
    submit = SubmitField('submit')

