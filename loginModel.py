from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, PasswordField, SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired, InputRequired, Length, NumberRange, Regexp


class UploadForm(FlaskForm):
	submit = SubmitField('LET ME UP')