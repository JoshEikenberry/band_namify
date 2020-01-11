from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import ValidationError, DataRequired, Length, Regexp, EqualTo
from app.models import User, BandName


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')


class BandNameForm(FlaskForm):
    band_name = TextAreaField('', validators=[DataRequired(), Regexp(regex='^[a-zA-Z0-9\s.\-\"\'!;,?]+$'),
                                              Length(min=1, max=256), ])
    submit = SubmitField('Submit Band Name!')
