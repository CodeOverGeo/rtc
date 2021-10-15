from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length


class StationForm(FlaskForm):
    """Form for searching for stations."""

    address = StringField('Address', validators=[DataRequired()])
