import os
from math import floor,ceil
from flask import Flask, render_template, request, redirect, session, send_from_directory
import psycopg2 
import random

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
    if not 'login' in session:
        return redirect('/login')
    return render_template("estacionamiento.html")

#Entradas y salidas
@app.route("/estacionamiento/inout")
def entradas_salidas():
    if not 'login' in session:
        return redirect('/login')
    return render_template("/estacionamiento/inout.html")

#Seccion de visualizar el estacionamiento
@app.route('/estacionamiento/ver')
def estacionamiento_ver():
    if not 'login' in session:
        return redirect('/login')
    find=''
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM lugar where seccion = 'A' ORDER BY numero")
    Autos = cursor.fetchall()
    aLenght = len(Autos)#Saber la cantidad de registros encontrados
    anL = floor(aLenght/10) #Cuantas lineas son empezando en 0
    print(aLenght)
    print(Autos)
    cursor.execute("SELECT * FROM lugar where seccion = 'D' ORDER BY numero")
    Discapacitados = cursor.fetchall()
    dLenght = len(Discapacitados)#Saber la cantidad de registros encontrados
    dnL = floor(dLenght/10)#Cuantas lineas son empezando en 0
    print(dLenght)
    print(Discapacitados)
    cursor.execute("SELECT * FROM lugar where seccion = 'M' ORDER BY numero")
    Motos = cursor.fetchall()
    mLenght = len(Motos)#Saber la cantidad de registros encontrados
    mnL = floor(mLenght/10)#Cuantas lineas son empezando en 0
    print(mLenght)
    print(Motos)
    conexion.close()
    return render_template("/estacionamiento/ver.html", find=find,Autos=Autos, Discapacitados=Discapacitados, Motos=Motos, aLenght=aLenght, dLenght=dLenght, mLenght=mLenght, anL=anL, dnL=dnL, mnL=mnL)

#Busqueda de un lugar dentro de visualizar
@app.route('/estacionamiento/ver/search', methods=["POST"])
def estacionamiento_ver_search():
    if not 'login' in session:
        return redirect('/login')
    _lugar = request.form['txtSearch']
    if(_lugar == ''):
        return redirect('/estacionamiento/ver')
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM lugar WHERE id='"+_lugar+"';")
    find = cursor.fetchall()
    cursor.execute("SELECT * FROM lugar where seccion = 'A' ORDER BY numero;")
    Autos = cursor.fetchall()
    aLenght = len(Autos)#Saber la cantidad de registros encontrados
    anL = floor(aLenght/10) #Cuantas lineas son empezando en 0
    print(aLenght)
    print(Autos)
    cursor.execute("SELECT * FROM lugar where seccion = 'D' ORDER BY numero")
    Discapacitados = cursor.fetchall()
    dLenght = len(Discapacitados)#Saber la cantidad de registros encontrados
    dnL = floor(dLenght/10)#Cuantas lineas son empezando en 0
    print(dLenght)
    print(Discapacitados)
    cursor.execute("SELECT * FROM lugar where seccion = 'M' ORDER BY numero")
    Motos = cursor.fetchall()
    mLenght = len(Motos)#Saber la cantidad de registros encontrados
    mnL = floor(mLenght/10)#Cuantas lineas son empezando en 0
    print(mLenght)
    print(Motos)
    conexion.close()
    return render_template("/estacionamiento/ver.html", find=find,Autos=Autos, Discapacitados=Discapacitados, Motos=Motos, aLenght=aLenght, dLenght=dLenght, mLenght=mLenght, anL=anL, dnL=dnL, mnL=mnL)

#Seccion buscar lugar o ticket
@app.route('/estacionamiento/search')
def estacionamiento_search():
    if not 'login' in session:
        return redirect('/login')
    find = ''
    tipo = ''
    return render_template('/estacionamiento/splace.html', find=find, tipo=tipo)

@app.route('/estacionamiento/search/find', methods=['POST'])
def estacionamiento_search_find():
    if not 'login' in session:
        return redirect('/login')
    _lugar = request.form['txtSearch']
    _tipo = request.form['tipo']
    if(_lugar == ''):
        return redirect('/estacionamiento/search')
    conexion = conectar_db()
    cursor = conexion.cursor()
    if _tipo == 'lugar':
        cursor.execute("SELECT * FROM lugar WHERE id='"+_lugar+"';")
        find = cursor.fetchall()
        tipo = 'l'
    if _tipo == 'ticket':
        print('Se intento buscar ticket')
        find = 'h'
        tipo = 't'
    
    return render_template('/estacionamiento/splace.html', find=find, tipo=tipo)
#Rutas de Notificaciones

#Rutas de configuraciones
@app.route('/configuracion/agregar')
def configuracion_agregar():
    if not 'login' in session:
        return redirect('/login')
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM lugar where seccion = 'A' ORDER BY numero")
    Autos = cursor.fetchall()
    aLenght = len(Autos)#Saber la cantidad de registros encontrados
    anL = floor(aLenght/10) #Cuantas lineas son empezando en 0
    print(aLenght)
    print(Autos)
    cursor.execute("SELECT * FROM lugar where seccion = 'D' ORDER BY numero")
    Discapacitados = cursor.fetchall()
    dLenght = len(Discapacitados)#Saber la cantidad de registros encontrados
    dnL = floor(dLenght/10)#Cuantas lineas son empezando en 0
    print(dLenght)
    print(Discapacitados)
    cursor.execute("SELECT * FROM lugar where seccion = 'M' ORDER BY numero")
    Motos = cursor.fetchall()
    mLenght = len(Motos)#Saber la cantidad de registros encontrados
    mnL = floor(mLenght/10)#Cuantas lineas son empezando en 0
    print(mLenght)
    print(Motos)
    conexion.close()
    return render_template("/configuracion/addplace.html",Autos=Autos, Discapacitados=Discapacitados, Motos=Motos, aLenght=aLenght, dLenght=dLenght, mLenght=mLenght, anL=anL, dnL=dnL, mnL=mnL)

@app.route('/configuracion/agregar/add', methods=['POST'])
def configuracion_agregar_add():
    if not 'login' in session:
        return redirect('/login')
    _seccion = request.form['Seccion']
    print(_seccion)
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT count(seccion) FROM lugar WHERE seccion='"+str(_seccion)+"';") #saber el numero de lugares totales
    nl = cursor.fetchone()
    nl = nl[0]
    nl = nl+1 #Para sacar el numero de lugar segun los ya existentes
    print(nl)
    if _seccion == 'A':
        cursor.execute("INSERT INTO lugar(id,numero,descripcion,disponible,seccion) VALUES ('A"+str(nl)+"','"+str(nl)+"','auto',true,'A');")
        print('a')
    if _seccion == 'D':
        cursor.execute("INSERT INTO lugar(id,numero,descripcion,disponible,seccion) VALUES ('D"+str(nl)+"','"+str(nl)+"','discapacitado',true,'D');")
        print("d")
    if _seccion == 'M':
        cursor.execute("INSERT INTO lugar(id,numero,descripcion,disponible,seccion) VALUES ('M"+str(nl)+"','"+str(nl)+"','moto',true,'M');")
        print('m')
    conexion.commit()
    conexion.close()
    return redirect('/configuracion/agregar')

@app.route('/configuracion/borrar')
def configuracion_borrar():
    if not 'login' in session:
        return redirect('/login')
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM lugar where seccion = 'A' ORDER BY numero")
    Autos = cursor.fetchall()
    aLenght = len(Autos)#Saber la cantidad de registros encontrados
    anL = floor(aLenght/10) #Cuantas lineas son empezando en 0
    print(aLenght)
    print(Autos)
    cursor.execute("SELECT * FROM lugar where seccion = 'D' ORDER BY numero")
    Discapacitados = cursor.fetchall()
    dLenght = len(Discapacitados)#Saber la cantidad de registros encontrados
    dnL = floor(dLenght/10)#Cuantas lineas son empezando en 0
    print(dLenght)
    print(Discapacitados)
    cursor.execute("SELECT * FROM lugar where seccion = 'M' ORDER BY numero")
    Motos = cursor.fetchall()
    mLenght = len(Motos)#Saber la cantidad de registros encontrados
    mnL = floor(mLenght/10)#Cuantas lineas son empezando en 0
    print(mLenght)
    print(Motos)
    conexion.close()
    return render_template('/configuracion/removeplace.html', Autos=Autos, Discapacitados=Discapacitados, Motos=Motos, aLenght=aLenght, dLenght=dLenght, mLenght=mLenght, anL=anL, dnL=dnL, mnL=mnL)

@app.route('/configuracion/borrar/delete', methods=['POST'])
def configuracion_borrar_delete():
    if not 'login' in session:
        return redirect('/login')
    _id = request.form['txtId']
    conexion = conectar_db()
    cursor = conexion.cursor()
    
    cursor.execute("DELETE FROM lugar WHERE id='"+str(_id)+"';")
   
    conexion.commit()
    conexion.close()
    return redirect('/configuracion/borrar')

@app.route('/configuracion/modificar')
def configuracion_modificar():
    if not 'login' in session:
        return redirect('/login')
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM lugar where seccion = 'A' ORDER BY numero")
    Autos = cursor.fetchall()
    aLenght = len(Autos)#Saber la cantidad de registros encontrados
    anL = floor(aLenght/10) #Cuantas lineas son empezando en 0
    print(aLenght)
    print(Autos)
    cursor.execute("SELECT * FROM lugar where seccion = 'D' ORDER BY numero")
    Discapacitados = cursor.fetchall()
    dLenght = len(Discapacitados)#Saber la cantidad de registros encontrados
    dnL = floor(dLenght/10)#Cuantas lineas son empezando en 0
    print(dLenght)
    print(Discapacitados)
    cursor.execute("SELECT * FROM lugar where seccion = 'M' ORDER BY numero")
    Motos = cursor.fetchall()
    mLenght = len(Motos)#Saber la cantidad de registros encontrados
    mnL = floor(mLenght/10)#Cuantas lineas son empezando en 0
    print(mLenght)
    print(Motos)
    conexion.close()
    return render_template('/configuracion/modplace.html' ,  Autos=Autos, Discapacitados=Discapacitados, Motos=Motos, aLenght=aLenght, dLenght=dLenght, mLenght=mLenght, anL=anL, dnL=dnL, mnL=mnL)

@app.route('/configuracion/modificar/update', methods=['POST'])
def configuracion_modificar_update():
    if not 'login' in session:
        return redirect('/login')
    _id = request.form['txtId']
    conexion = conectar_db()
    cursor = conexion.cursor()
    
    cursor.execute("SELECT * FROM lugar WHERE id='"+str(_id)+"';")
    find = cursor.fetchone()
    if find[3] == True:
        cursor.execute("UPDATE lugar SET disponible='false' WHERE id='"+str(_id)+"';")
    else:
        cursor.execute("UPDATE lugar SET disponible='true' WHERE id='"+str(_id)+"';")
   
    conexion.commit()
    conexion.close()
    return redirect('/configuracion/modificar')

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