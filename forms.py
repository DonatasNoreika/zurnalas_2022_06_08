from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, FloatField


class IrasasForm(FlaskForm):
    pajamos = BooleanField('Pajamos')
    suma = FloatField('Suma')
    submit = SubmitField('Įvesti')
