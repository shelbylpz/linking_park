import os
from math import floor,ceil
from flask import Flask, render_template, request, redirect, session, send_from_directory
import psycopg2 

app = Flask(__name__)
app.secret_key="thelmamada"

def conectar_db():
    conexion = psycopg2.connect(
        user = 'postgres',
        password = 'password',
        host = 'localhost',
        port = '5432',
        database = 'LinkingParkDB'
    )
    return conexion

@app.route("/")
def index():
    if not 'login' in session:
        return redirect('/login')
    return render_template("index.html")
#Obtencion de imagen o CSS personalizado
@app.route('/img/<imagen>')
def imagenes(imagen):
    print(imagen)
    return send_from_directory(os.path.join('templates/img'),imagen)

@app.route('/css/<archivocss>')
def css_link(archivocss):
    return send_from_directory(os.path.join("templates/css"),archivocss)

#Rutas de Estacionamiento
@app.route("/estacionamiento/")
def estacionamiento():
    return render_template("estacionamiento.html")


@app.route("/estacionamiento/inout")
def entradas_salidas():

    return render_template("/estacionamiento/inout.html")

@app.route('/estacionamiento/ver')
def estacionamiento_ver():
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM lugar where seccion = 'A'")
    Autos = cursor.fetchall()
    aLenght = len(Autos)#Saber la cantidad de registros encontrados
    anL = floor(aLenght/10) #Cuantas lineas son empezando en 0
    print(aLenght)
    print(Autos)
    cursor.execute("SELECT * FROM lugar where seccion = 'D'")
    Discapacitados = cursor.fetchall()
    dLenght = len(Discapacitados)#Saber la cantidad de registros encontrados
    dnL = floor(dLenght/10)#Cuantas lineas son empezando en 0
    print(dLenght)
    print(Discapacitados)
    cursor.execute("SELECT * FROM lugar where seccion = 'M'")
    Motos = cursor.fetchall()
    mLenght = len(Motos)#Saber la cantidad de registros encontrados
    mnL = floor(mLenght/10)#Cuantas lineas son empezando en 0
    print(mLenght)
    print(Motos)
    conexion.close()
    return render_template("/estacionamiento/ver.html", Autos=Autos, Discapacitados=Discapacitados, Motos=Motos, aLenght=aLenght, dLenght=dLenght, mLenght=mLenght, anL=anL, dnL=dnL, mnL=mnL)

#Rutas de Notificaciones

#Rutas de configuraciones


#Rutas de Login y Logout
@app.route("/login")
def login():
    if "login" in session:
        return redirect("/")
    return render_template("login.html")

@app.route("/login", methods=['POST'])
def login_post():
    _usuario = request.form['txtUsuario']
    _password = request.form['txtPassword']
    print(_usuario)
    print(_password)

    if _usuario == "admin" and _password == "123":
        session["login"] = True
        session["usuario"] = "Administrador"
        return redirect("/")
    
    return render_template("login.html", mensaje = "Acceso denegado")

@app.route("/LogOut")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == '__main__':
    app.run(debug=True)