from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = '4654f5dfadsrflkjfglskjfdglkjsdlkdfsdr54e6rae'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'zurnalas.db')
# nustatėme, kad mūsų duomenų bazė bus šalia šio failo esants data.sqlite failas
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# neseksime kiekvienos modifikacijos
db = SQLAlchemy(app)
from forms import IrasasForm

class Irasas(db.Model):
    # DB lentelei priskiria pavadinimą, jei nenurodysite, priskirs automatiškai pagal klasės pavadinimą.
    __tablename__ = 'irasai'
    id = db.Column(db.Integer, primary_key=True)  # stulpelis, kurio reikšmės integer. Taip pat jis bus primary_key.
    suma = db.Column(db.Float, nullable=False)
    pajamos = db.Column(db.Boolean, nullable=False)

    def __init__(self, suma, pajamos):
        self.suma = suma
        self.pajamos = pajamos

    def __repr__(self):
        return f'{self.id}: suma - {self.suma}'

db.create_all()

@app.route("/zurnalas", methods=['GET', 'POST'])
def zurnalas():
    form = IrasasForm()
    if form.validate_on_submit():
        irasas = Irasas(suma=form.suma.data, pajamos=form.pajamos.data)
        db.session.add(irasas)
        db.session.commit()
        return redirect(url_for('zurnalas'))
    else:
        zurnalas = Irasas.query.all()
        suma = 0
        for irasas in zurnalas:
            if irasas.pajamos:
                suma += irasas.suma
            else:
                suma -= irasas.suma
        return render_template('zurnalas.html', zurnalas=zurnalas, form=form, suma=suma)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/skaiciavimai")
def skaiciavimai():
    return render_template('skaiciavimai.html')

@app.route("/zmones")
def zmones():
    vardai = ['Jonas', 'Antanas', 'Petras']
    return render_template('zmones.html', sarasas=vardai)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        vardas = request.form['vardas']
        return render_template("greetings.html", vardas=vardas)
    else:
        return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)