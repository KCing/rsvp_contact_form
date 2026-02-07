from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Optional, Email, Length

class RsvpForm(FlaskForm):
    name = StringField("Full Name:", validators=[DataRequired(), Length(min=4, max=50)])
    email = EmailField("Email:", validators=[Optional(), Email()])
    phone = StringField("Phone Number:")
    attend = SelectField("Will you attend?", choices=[("Please choose an option", "Please choose an option"),("Yes", "Yes"),("No", "No"),("Maybe", "Maybe")])
    member = SelectField("Member of TKH?", choices=[("Please choose an option", "Please choose an option"),("Yes", "Yes"),("No", "No")])
    message = TextAreaField("Anything You Would Like To See?", validators=[Optional(), Length(max=500)])
    submit = SubmitField("Register")