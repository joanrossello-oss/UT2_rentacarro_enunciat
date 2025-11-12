from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField, validators, ValidationError
from wtforms.validators import DataRequired, Length
from datetime import date
from flask import session


class PostForm(FlaskForm):
    # mètode per comprovar si la fetxa es posterior a la fetxa actual
    def comprovar_fetxa(form, fetxa):
        if fetxa.data < date.today(): # date.today() -> obtenir la fetxa actual
            raise ValidationError('La fetxa no pot ser anterior a la actual.')
        
    def comprovar_carro_existent(form, camp):
        fetxa = form.fetxa.data.strftime('%d-%m-%y')
        carro = form.carro.data

        reserves = session.get('reserves',[])
        print(reserves)

        for r in reserves:
            # comprar les dades de les reserves existents amb la peticio de post a fer
            if r['dia_reserva'] == fetxa and r['carro'] == carro:
                raise ValidationError('No pots reservar el carro per el dia seleccionat, ja es troba reservat.')
    
    nom = StringField('nom', validators=[DataRequired(), Length(max=128)])
    llinatges = StringField('llinatges', validators=[DataRequired(), Length(max=128)])
    fetxa = DateField('fetxa', format='%Y-%m-%d', default=date.today, validators=[DataRequired(), comprovar_fetxa])
    carro = SelectField('carro', choices=['Carro simple', 'carro 2', 'carro 3'], validators=[DataRequired(), comprovar_carro_existent])
    submit = SubmitField('Enviar')

    
