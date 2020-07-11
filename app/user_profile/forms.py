from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Optional


class UserProfileForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    email_address = StringField("EmailAddress", validators=[DataRequired(), Email()])
    first_name = StringField("FirstName", validators=[DataRequired()])
    last_name = StringField("LastName", validators=[DataRequired()])
    street_address = StringField("StreetAddress", validators=[DataRequired()])
    city = StringField("City", validators=[DataRequired()])
    country = StringField("Country", validators=[DataRequired()])
    postal_code = StringField("PostalCode", validators=[DataRequired()])
    about_me = StringField("AboutMe", validators=[Optional()])
    submit = SubmitField("Sign In")
