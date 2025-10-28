from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms.validators import DataRequired, Length
from datetime import date

class PostForm(FlaskForm):
    nom = StringField('nom', validators=[DataRequired(), Length(max=128)])
    llinatges = StringField('llinatges', validators=[Length(max=128)])
    fetxa = DateField('Fecha', format='%Y-%m-%d', default=date.today)
    submit = SubmitField('Enviar')