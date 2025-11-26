from flask import Flask, render_template, redirect, url_for, session, request
from datetime import datetime
from PostForm import PostForm
from CrearCarroForm import CrearCarroForm
from db import db, Carros, Reservas
from rentacarro import *

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '83d168b4966265e8ae59f10f57a2b535c18668555b1d499b7353c9b9546146d1'
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/rentacarro"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    
    @app.route("/")
    def llistar():
        carros = carrega_carros()
        return render_template('carros.html', carros=carros)
    
    @app.route("/reservar", methods=['GET', 'POST'])
    def reservar():
        form = PostForm()
        if form.validate_on_submit():
            session["usuario"] = form.nom.data + form.llinatges.data
            session["iniciReserva"] = form.iniciReserva.data
            session["finalReserva"]  = form.finalReserva.data
            idcarro = form.idcarro.data
            # form.horareserva.data - form.horaretorno.data

            reserves = session.get("reserves", [])

            nova_reserva = {
                "carro": idcarro,
                "iniciReserva": session['iniciReserva'],
                "finalReserva": session['finalReserva'],
                "usuario": session['usuario']
            }

            reserves.append(nova_reserva)
            session['reserves'] = reserves
            crear_reserva(session['iniciReserva'], session['finalReserva'], session['usuario'])
            return redirect(url_for('comprovar_reserves'))

        return render_template('carros2.html', form=form)
    
    @app.route("/comprovar_reserves")
    def comprovar_reserves():
        reserves = obtenir_reserves()
        return render_template('carros3.html', reserves=reserves)   

    @app.route("/intranet", methods=['GET','POST'])
    def intranet():
        carros = carrega_carros()
        for carro in carros:
            carro['actualitzant'] = False
        return render_template('carros4.html', carros=carros)
    
    @app.route("/crear_carro", methods=['GET','POST'])
    def crear():
        form = CrearCarroForm()
        if form.validate_on_submit():
            nom = form.nom.data
            descripcio = form.descripcio.data
            clase = form.clase.data
            preu = form.preu.data
            crear_carro(nom, descripcio, clase, preu)
            return redirect(url_for('intranet'))    

        return render_template('crear_carro.html', form=form)

    @app.route("/borrar_carro")
    def borrar_carro():
        id = request.args.get('id')
        borrar_carro = borrar_carros(id)
        return redirect(url_for('intranet'))
    
    @app.route("/actualitzar")
    def actualitzar_carro():
        id = request.args.get('id')
        # nom = request.args.get('nom')
        # descripcio = request.args.get('descripcio')
        # preu = request.args.get()
        carros = carrega_carros()
        # for carro in carros:
            # if carro['id'] == id
            # carro.actualitzant = True
        return redirect(url_for('intranet'))
        
    return app

# Eliminar sesió per anar fent proves i eliminar les reserves
# @app.route("/eliminar_sessio")
# def eliminar_sessio():
#     session.clear()
#     return redirect(url_for('reservar'))

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)