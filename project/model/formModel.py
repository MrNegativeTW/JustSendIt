from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, PasswordField, SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired, InputRequired, Length, NumberRange, Regexp

class UploadForm(FlaskForm):
	submit = SubmitField('LET ME UP')

class ReceiveForm(FlaskForm):
	fileID = StringField('', validators=[
            InputRequired(),
            Regexp("^[0-9A-Za-z]{6}$", message="ID must be exactly 6 charss.")]
        )
	submit = SubmitField('Get')