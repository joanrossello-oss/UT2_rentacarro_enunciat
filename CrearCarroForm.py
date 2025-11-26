from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField, validators, ValidationError, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange
from datetime import date


class CrearCarroForm(FlaskForm):
    nom = StringField('nom', validators=[DataRequired(), Length(max=128)])
    descripcio = StringField('descripcio', validators=[DataRequired(), Length(max=128)])
    clase = SelectField('clase', choices=['basic','1cavall','2cavalls'], validators=[DataRequired()])
    preu = IntegerField('preu', validators=[DataRequired()])
    submit = SubmitField('Enviar')

    
