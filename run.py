from flask import Flask, render_template, request, redirect, url_for, flash, session
import json
from datetime import datetime
from PostForm import PostForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '83d168b4966265e8ae59f10f57a2b535c18668555b1d499b7353c9b9546146d1'

@app.route("/")
def llistar():
    # Llegir json
    with open ('.\static\carros.json') as file:
        llista_carros = json.load(file)
        return render_template('carros.html', llista_carros=llista_carros)

@app.route("/reservar", methods=['GET', 'POST'])
def reservar():
    form = PostForm()
    if form.validate_on_submit():
        session["nom"] = form.nom.data
        session["llinatges"] = form.llinatges.data
        session["dia_reserva"] = form.fetxa.data.strftime('%d-%m-%y') # Verifica el nombre del campo
        session["carro"] = form.carro.data


        print(session['dia_reserva'])
        reserves = session.get("reserves", [])

        nova_reserva = {
            "nom": session['nom'],
            "llinatges": session['llinatges'],
            "dia_reserva": session['dia_reserva'],
            "carro": session['carro']
        }

        reserves.append(nova_reserva)
        session['reserves'] = reserves
        return redirect(url_for('comprovar_reserves'))

        # if comprovar_fetxa() and comprovar_carro_existent(session["carro"], reserves):
        #     fetxa_obj = datetime.strptime(session['dia_reserva'], '%Y-%m-%d')
        #     fetxa_formateada = fetxa_obj.strftime('%d-%m-%y')
        #     nova_reserva = {
        #         "nom": session["nom"],
        #         "llinatges": session["llinatges"],
        #         "dia_reserva": fetxa_formateada, 
        #         "carro": session["carro"]
        #     }
        #     print(session['dia_reserva'])
        #     reserves.append(nova_reserva)
        #     session["reserves"] = reserves
        #     return redirect(url_for('comprovar_reserves'))
        # else:
        #     return redirect(url_for('reservar'))

    return render_template('carros2.html', form=form)


@app.route("/comprovar_reserves")
def comprovar_reserves():
    reserves = session.get("reserves", [])
    return render_template('carros3.html', reserves=reserves)   

# Eliminar sesió per anar fent proves i eliminar les reserves
# @app.route("/eliminar_sessio")
# def eliminar_sessio():
#     session.clear()
#     return redirect(url_for('reservar'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)