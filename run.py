from flask import Flask, render_template, request, redirect, url_for, flash, session
import json
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '83d168b4966265e8ae59f10f57a2b535c18668555b1d499b7353c9b9546146d1'

@app.route("/")
def llistar():
    # Llegir json
    with open ('.\static\carros.json') as file:
        llista_carros = json.load(file)
        return render_template('carros.html', llista_carros=llista_carros)

@app.route("/reservar", methods=['GET','POST'])
def reservar():
    if request.method == 'POST':
        session["nom"] = request.form['nom'].strip()
        session["llinatges"] = request.form['llinatges'].strip()
        session["dia_reserva"] = request.form['reserva'].strip()
        session["carro"] = request.form['carro'].strip()

        try:
            data_obj = datetime.datetime.strptime(session["dia_reserva"], '%d-%m-%Y')
        except ValueError:
            flash("⚠️ Format de fetxa incorrecte. Empela el format DD-MM-YYYY")

        reserves = session.get("reserves", [])

        if comprovar_fetxa(data_obj) and comprovar_carro_existent(session["carro"], data_obj, reserves):
                nova_reserva = {
                    "nom": session["nom"],
                    "llinatges": session["llinatges"],
                    "dia_reserva": data_obj.strftime('%d-%m-%y'),
                    "carro": session["carro"]
                }
                print(session['dia_reserva'])
                reserves.append(nova_reserva)
                session["reserves"] = reserves
                return redirect(url_for('comprovar_reserves'))
        else:
            return redirect(url_for('reservar'))
        
    return render_template("carros2.html")

@app.route("/comprovar_reserves")
def comprovar_reserves():
    reserves = session.get("reserves", [])
    return render_template('carros3.html', reserves=reserves)   

# Eliminar sesió per anar fent proves i eliminar les reserves
# @app.route("/eliminar_sessio")
# def eliminar_sessio():
#     session.clear()
#     return redirect(url_for('reservar'))

# mètode per comprovar si la fetxa es posterior a la fetxa actual
def comprovar_fetxa(data_obj):
    # obtenir la fetxa actual
    data = datetime.datetime.now()
    # convertir el parametre a format datetime per poder comparar amb la fetxa actual
    if data.date() > data_obj.date():
        flash("❌ No pots seleccionar una data anterior a avui.")
        return False
    return True

# Mètode per comprovar si el carro ja existeix un dia concret
def comprovar_carro_existent(carro, data_obj, reserves):
    for element in reserves:
        dia_reserva = datetime.datetime.strptime(element['dia_reserva'], "%d-%m-%y").date()
        if element['carro']  == carro and dia_reserva == data_obj.date():
            flash("❌ No pots reservar el carro per el dia seleccionat, ja es troba reservat.")
            return False
    return True

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)