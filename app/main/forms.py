from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Regexp


class BandNameForm(FlaskForm):
    band_name = TextAreaField('', validators=[DataRequired(), Regexp(regex='^[a-zA-Z0-9\s.\-\"\'!;,?]+$'),
                                              Length(min=1, max=256)])
    submit = SubmitField('Submit Band Name!')
