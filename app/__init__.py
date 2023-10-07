import os, shutil
from math import floor,ceil
from flask import Flask, render_template, request, redirect, session, send_from_directory, Response
import psycopg2 
import datetime
import time
import threading
import pyqrcode
import png
from connect import conectar_db
#Imports para la camara
import cv2
import pyqrcode
import png
from pyqrcode import QRCode #Esta tambien es escencial para el funcionamiento del programa
import psycopg2
from pyzbar.pyzbar import decode
import numpy as np
import time

app = Flask(__name__)
app.secret_key="thelmamada"

@app.route("/")
def index():
    if not 'login' in session:
        return redirect('/login')
    n_avisos = verificar_nalertas()
    print(n_avisos)
    return render_template("index.html", n_avisos=n_avisos, usuario=session['usuario'])
#Obtencion de imagen o CSS personalizado
@app.route('/img/<imagen>')
def imagenes(imagen):
    print(imagen)
    return send_from_directory(os.path.join('templates/img'),imagen)

@app.route('/qr/<qrcode>')
def qr(qrcode):
    return send_from_directory(os.path.join("QRCodes/img"),qrcode)

@app.route('/css/<archivocss>')
def css_link(archivocss):
    return send_from_directory(os.path.join("templates/css"),archivocss)

#Rutas de Estacionamiento
@app.route("/estacionamiento/")
def estacionamiento():
    if not 'login' in session:
        return redirect('/login')
    n_avisos = verificar_nalertas()
    return render_template("estacionamiento.html", n_avisos=n_avisos, usuario=session['usuario'])

#Entradas y salidas
@app.route("/estacionamiento/inout")
def entradas_salidas():
    if not 'login' in session:
        return redirect('/login')
    n_avisos = verificar_nalertas()
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM ticket ORDER BY id DESC;")
    tickets = cursor.fetchall()
    conexion.commit()
    conexion.close()
    return render_template("/estacionamiento/inout.html", tickets=tickets, n_avisos=n_avisos, usuario=session['usuario'])

#Seccion de visualizar el estacionamiento
@app.route('/estacionamiento/ver')
def estacionamiento_ver():
    if not 'login' in session:
        return redirect('/login')
    n_avisos = verificar_nalertas()
    find=''
    Autos, aLenght, anL, Discapacitados, dLenght, dnL, Motos, mLenght, mnL = data_for_view_parking()
    return render_template("/estacionamiento/ver.html",  n_avisos=n_avisos, find=find,Autos=Autos, Discapacitados=Discapacitados, Motos=Motos, aLenght=aLenght, dLenght=dLenght, mLenght=mLenght, anL=anL, dnL=dnL, mnL=mnL, usuario=session['usuario'])

#Busqueda de un lugar dentro de visualizar
@app.route('/estacionamiento/ver/search', methods=["POST"])
def estacionamiento_ver_search():
    if not 'login' in session:
        return redirect('/login')
    n_avisos = verificar_nalertas()
    try:
        _lugar = request.form['txtSearch']
        if(_lugar == ''):
            return redirect('/estacionamiento/ver')
        _lugar = _lugar.upper() # Para que todas las busquedas sean con mayusculas ya que no se debe tener ningun campo en minusculas
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM hlugar WHERE id='"+_lugar+"';")
        find = cursor.fetchall()
        if (find[0][3] >= 2):
            idTcket = find[0][5]
            print(idTcket)
            cursor.execute("SELECT entrada, salida FROM ticket WHERE id='"+idTcket+"';")
            entrada = cursor.fetchone()
            if entrada[1] == 'null':
                tiempo = update_time(entrada)
                print(tiempo)
                cursor.execute("UPDATE ticket SET tiempo='"+str(tiempo)+"' WHERE id='"+str(idTcket)+"';") #Actualizamos en la base de datos el tiempo que lleva el lugar ocupado
            qrco = "./app/QRCodes/img/"+str(idTcket)+".png" #Se asigna la direccion de nuestro codigo qr a una variable
            print(qrco)
            try:
                if(os.path.exists(qrco) == False):
                        generator(idTcket)
            except (Exception):
                print("Ya existe QR")
        conexion.commit()
        cursor.close()
        conexion.close()
        Autos, aLenght, anL, Discapacitados, dLenght, dnL, Motos, mLenght, mnL = data_for_view_parking()
        return render_template("/estacionamiento/ver.html",n_avisos=n_avisos, find=find,Autos=Autos, Discapacitados=Discapacitados, Motos=Motos, aLenght=aLenght, dLenght=dLenght, mLenght=mLenght, anL=anL, dnL=dnL, mnL=mnL, usuario=session['usuario'])
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error durante la ejecucion de la consulta: ", error)
    finally:
        Autos, aLenght, anL, Discapacitados, dLenght, dnL, Motos, mLenght, mnL = data_for_view_parking()
    return render_template("/estacionamiento/ver.html",n_avisos=n_avisos, find='',Autos=Autos, Discapacitados=Discapacitados, Motos=Motos, aLenght=aLenght, dLenght=dLenght, mLenght=mLenght, anL=anL, dnL=dnL, mnL=mnL, mensaje='Error', usuario=session['usuario'])

#Seccion buscar lugar o ticket

@app.route('/estacionamiento/search')
def estacionamiento_search():
    if not 'login' in session:
        return redirect('/login')
    
    n_avisos = verificar_nalertas()
    find = ''
    tipo = ''
    return render_template('/estacionamiento/splace.html',n_avisos=n_avisos, find=find, tipo=tipo, usuario=session['usuario'])

@app.route('/estacionamiento/search/find', methods=['POST'])
def estacionamiento_search_find():
    if not 'login' in session:
        return redirect('/login')
    n_avisos = verificar_nalertas()
    try:
        _lugar = request.form['txtSearch']
        _tipo = request.form['tipo']
        if(_lugar == ''):
            return redirect('/estacionamiento/search')
        conexion = conectar_db()
        cursor = conexion.cursor()
        if _tipo == 'lugar':
            _lugar = _lugar.upper()
            cursor.execute("SELECT * FROM hlugar WHERE id='"+_lugar+"';")
            find = cursor.fetchall()
            print(find)
            if (find[0][3] == False):
                qrco = str(route)+"/app/QRCodes/img/"+str(find[0][5])+".png" #Asigna ruta de qr a variable
                print(qrco)
                if(os.path.exists(qrco) == False): # Se verifica que el archivo exista si no se genera
                    generator(find[0][5])
            tipo = 'l'
        if _tipo == 'ticket':
            print('Se intento buscar ticket')
            cursor.execute("SELECT entrada, salida FROM ticket WHERE id='"+_lugar+"';")
            entrada = cursor.fetchone()
            print(entrada[1])
            if entrada[1] is None:
                tiempo = update_time(entrada)
                print(tiempo)
                cursor.execute("UPDATE ticket SET tiempo='"+str(tiempo)+"' WHERE id='"+str(_lugar)+"';") #Actualizamos en la base de datos el tiempo que lleva el lugar ocupado
            qrco = str(route)+"/app/QRCodes/img/"+str(_lugar)+".png" # Asignamos direccion del codigo qr a variable
            print(qrco)
            if(os.path.exists(qrco) == False): # Verificamos que el archivo exista si no lo genera
                generator(_lugar)
            cursor.execute("SELECT * FROM ticket WHERE id='"+_lugar+"';")
            find = cursor.fetchall()
            conexion.commit()
            conexion.close()
            tipo = 't'
        print(find)
        return render_template('/estacionamiento/splace.html',n_avisos=n_avisos, find=find, tipo=tipo, usuario=session['usuario'])
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error durante la ejecucion de la consulta: ", error)
    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()
    return render_template('/estacionamiento/splace.html',n_avisos=n_avisos, find='' , mensaje='ERROR', usuario=session['usuario'])

#Rutas de Notificaciones

@app.route('/alertas')
def avisos():
    if not 'login' in session:
        return redirect('/login')
    n_avisos = verificar_nalertas()
    return render_template("/notificaciones/alertas.html", n_avisos=n_avisos, usuario=session['usuario'])

@app.route("/alertas/<table>")
def avisos_seleccion(table):
    if not 'login' in session:
        return redirect('/login')
    n_avisos = verificar_nalertas()
    datos, tipo = datos_tipo(table)
    print(datos)
    return render_template("/notificaciones/alertas.html",n_avisos=n_avisos, datos=datos, tipo=tipo, usuario=session['usuario'])

def datos_tipo(table):
    conexion = conectar_db()
    cursor = conexion.cursor()
    if table == 'avisos':
        cursor.execute("SELECT * FROM avisos;")
        tipo = "a"
    elif table == 'historial':
        cursor.execute("SELECT * FROM h_avisos;")
        tipo = "h"
    data = cursor.fetchall()
    conexion.commit()
    conexion.close()
    return data, tipo

@app.route('/alertas/informar', methods=["POST"])
def avisos_informar():
    if not 'login' in session:
        return redirect('/login')
    n_avisos = verificar_nalertas()
    print("entro")
    _id = request.form['txtID']
    _table = request.form['txtTipo']
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM avisos WHERE id='"+str(_id)+"';")
    datos = cursor.fetchone()
    print(datos)
    newid = datos[0]
    newdescrip = datos[1]
    newticket = datos[2]
    now = datetime.datetime.now()
    newtiempo = now.strftime("%Y-%m-%d %H:%M:%S.%f")
    print(newtiempo)
    cursor.execute("INSERT INTO h_avisos(id,descripcion,id_ticket,fecha) VALUES ('"+str(newid)+"','"+str(newdescrip)+"','"+str(newticket)+"','"+str(newtiempo)+"')")
    cursor.execute("DELETE FROM avisos WHERE id='"+str(_id)+"';")
    conexion.commit()
    conexion.close()
    datos, tipo = datos_tipo(_table)
    mensaje = "Alerta atendida se movio al historial con el ID:"+str(newid)
    return render_template('/notificaciones/alertas.html',n_avisos=n_avisos, datos=datos, tipo=tipo, mensaje=mensaje, usuario=session['usuario'])

#Rutas de configuraciones
@app.route('/configuracion/agregar')
def configuracion_agregar():
    if not 'login' in session:
        return redirect('/login')
    if session['usuario'] != 'Administrador':
        return redirect('/')
    n_avisos = verificar_nalertas()
    Autos, aLenght, anL, Discapacitados, dLenght, dnL, Motos, mLenght, mnL = data_for_view_parking()
    return render_template("/configuracion/addplace.html",n_avisos=n_avisos, Autos=Autos, Discapacitados=Discapacitados, Motos=Motos, aLenght=aLenght, dLenght=dLenght, mLenght=mLenght, anL=anL, dnL=dnL, mnL=mnL, usuario=session['usuario'])

@app.route('/configuracion/agregar/add', methods=['POST'])
def configuracion_agregar_add():
    if not 'login' in session:
        return redirect('/login')
    if session['usuario'] != 'Administrador':
        return redirect('/')
    _seccion = request.form['Seccion']
    print(_seccion)
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT count(seccion) FROM hlugar WHERE seccion='"+str(_seccion)+"';") #saber el numero de lugares totales
    nl = cursor.fetchone()
    nl = nl[0]
    nl = nl+1 #Para sacar el numero de lugar segun los ya existentes
    print(nl)
    if _seccion == 'A':
        cursor.execute("INSERT INTO hlugar(id,numero,descripcion,estado,seccion,status) VALUES ('A"+str(nl)+"','"+str(nl)+"','auto',0,'A','disponible');")
        print('a')
    if _seccion == 'D':
        cursor.execute("INSERT INTO hlugar(id,numero,descripcion,estado,seccion,status) VALUES ('D"+str(nl)+"','"+str(nl)+"','discapacitado',0,'D','disponible');")
        print("d")
    if _seccion == 'M':
        cursor.execute("INSERT INTO hlugar(id,numero,descripcion,estado,seccion,status) VALUES ('M"+str(nl)+"','"+str(nl)+"','moto',0,'M','disponible');")
        print('m')
    conexion.commit()
    conexion.close()
    return redirect('/configuracion/agregar')

@app.route('/configuracion/borrar')
def configuracion_borrar():
    if not 'login' in session:
        return redirect('/login')
    if session['usuario'] != 'Administrador':
        return redirect('/')
    n_avisos = verificar_nalertas()
    Autos, aLenght, anL, Discapacitados, dLenght, dnL, Motos, mLenght, mnL = data_for_view_parking()
    return render_template('/configuracion/removeplace.html',n_avisos=n_avisos, Autos=Autos, Discapacitados=Discapacitados, Motos=Motos, aLenght=aLenght, dLenght=dLenght, mLenght=mLenght, anL=anL, dnL=dnL, mnL=mnL, usuario=session['usuario'])

@app.route('/configuracion/borrar/delete', methods=['POST'])
def configuracion_borrar_delete():
    if not 'login' in session:
        return redirect('/login')
    if session['usuario'] != 'Administrador':
        return redirect('/')
    _id = request.form['txtId']
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM hlugar WHERE id='"+str(_id)+"';")
    data = cursor.fetchone()
    print(data)
    if (data[3] == False):
        print("No se puede mijo")
        conexion.commit()
        conexion.close()
        n_avisos = verificar_nalertas()
        Autos, aLenght, anL, Discapacitados, dLenght, dnL, Motos, mLenght, mnL = data_for_view_parking()
        return render_template('/configuracion/removeplace.html',n_avisos=n_avisos, Autos=Autos, Discapacitados=Discapacitados, Motos=Motos, aLenght=aLenght, dLenght=dLenght, mLenght=mLenght, anL=anL, dnL=dnL, mnL=mnL, mensaje="ERROR!", usuario=session['usuario'])
        
    cursor.execute("DELETE FROM hlugar WHERE id='"+str(_id)+"';")
    conexion.commit()
    conexion.close()
    return redirect('/configuracion/borrar')

@app.route('/configuracion/modificar')
def configuracion_modificar():
    if not 'login' in session:
        return redirect('/login')
    if session['usuario'] != 'Administrador':
        return redirect('/')
    Autos, aLenght, anL, Discapacitados, dLenght, dnL, Motos, mLenght, mnL = data_for_view_parking()
    return render_template('/configuracion/modplace.html', n_avisos=verificar_nalertas(), Autos=Autos, Discapacitados=Discapacitados, Motos=Motos, aLenght=aLenght, dLenght=dLenght, mLenght=mLenght, anL=anL, dnL=dnL, mnL=mnL, usuario=session['usuario'])

@app.route('/configuracion/modificar/update', methods=['POST'])
def configuracion_modificar_update():
    if not 'login' in session:
        return redirect('/login')
    if session['usuario'] != 'Administrador':
        return redirect('/')
    _id = request.form['txtId']
    conexion = conectar_db()
    cursor = conexion.cursor()
    
    cursor.execute("SELECT * FROM hlugar WHERE id='"+str(_id)+"';")
    find = cursor.fetchone()
    if find[3] == 0:
        now = datetime.datetime.now()
        hnow = now.strftime("%Y%m%d%H%M%S")
        tnow = now.strftime("%Y-%m-%d %H:%M:%S.%f")
        nticket = str(hnow)+"-"+str(_id)
        print(hnow)
        sql = "INSERT INTO ticket(id,entrada,lugar) VALUES ('"+str(nticket)+"','"+str(tnow)+"','"+str(_id)+"');"
        cursor.execute(sql)
        cursor.execute("UPDATE hlugar SET estado=1, status='no-verficado', ticket='"+str(nticket)+"' WHERE id='"+str(_id)+"'")
        
        generator(nticket)
    else:
        idticket = find[5]
        cursor.execute("SELECT entrada FROM ticket WHERE id='"+str(idticket)+"';")
        entrada = cursor.fetchone()
        now = datetime.datetime.now()
        tnow = now.strftime("%Y-%m-%d %H:%M:%S.%f") #Convierte la hora actual a un string con un formato definido
        tiempo = update_time(entrada=entrada)
        print(tiempo)
        cursor.execute("UPDATE ticket SET salida='"+str(tnow)+"', tiempo='"+str(tiempo)+"' WHERE id='"+str(idticket)+"';")
        cursor.execute("UPDATE hlugar SET estado='0', ticket=null, status='disponible' WHERE id='"+str(_id)+"';")
   
    conexion.commit()
    conexion.close()
    return redirect('/configuracion/modificar')

@app.route("/configuracion/usuarios")
def configuracion_usuarios():
    if not 'login' in session:
        return redirect('/login')
    if session['usuario'] != 'Administrador':
        return redirect('/')
    return render_template('/configuracion/usuarios.html', registros=data_for_users_table(), usuario=session['usuario'], n_avisos=verificar_nalertas())

@app.route('/configuracion/usuarios/add', methods=['POST'])
def configuracion_usuarios_add():
    if not 'login' in session:
        return redirect('/login')
    if session['usuario'] != 'Administrador' :
        return redirect('/')
    _username = request.form['txtNombre']
    _password = request.form['txtPassword']
    _tipo = request.form.get("txtTipo")
    print(_username)
    print(_password)
    print(_tipo)
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        query = "INSERT INTO users VALUES(DEFAULT,'"+str(_username)+"','"+str(_password)+"','"+str(_tipo)+"');"
        cursor.execute(query)
        conexion.commit()
        conexion.close()
        mensaje = ["success","Usuario agregado correctamente!", ""]
        return render_template('/configuracion/usuarios.html', mensaje=mensaje, registros=data_for_users_table(),n_avisos=verificar_nalertas())
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error durante la ejecucion de la consulta: ", error)
    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()
    return render_template('/configuracion/usuarios.html', error=True, registros=data_for_users_table(),n_avisos=verificar_nalertas())

@app.route("/configuracion/usuarios/delete", methods=['POST'])
def configuracion_users_delete():
    if not 'login' in session:
        return redirect('/login')
    if session['usuario'] != 'Administrador' :
        return redirect('/')
    _id = request.form['txtID']
    print(session["id"])
    print(_id)
    if int(_id) == int(session["id"]) :
        mensaje = ["warning","Usuario no eliminado!","El Usuario tiene una session abierta!"]
        return render_template('/configuracion/usuarios.html', mensaje=mensaje, registros=data_for_users_table(), n_avisos=verificar_nalertas())
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        query = "DELETE FROM users WHERE id="+str(_id)+";"
        cursor.execute(query)
        conexion.commit()
        conexion.close()
        mensaje = ["success","Usuario eliminado!","El Usuario ha sido eliminado correctamente!"]
        return render_template('/configuracion/usuarios.html',mensaje=mensaje, registros=data_for_users_table(), n_avisos=verificar_nalertas())
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error durante la ejecucion de la consulta: ", error)
    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()
    return render_template('/configuracion/usuarios.html', registros=data_for_users_table(), n_avisos=verificar_nalertas())

@app.route("/configuracion/usuarios/edit", methods=['POST'])
def configuracion_users_edit():
    if not 'login' in session:
        return redirect('/login')
    if session['usuario'] != 'Administrador' :
        return redirect('/')
    _id = request.form['txtID']
    print(session["id"])
    print(_id)
#Funciones modulacion

def update_time(entrada):
    now = datetime.datetime.now()
    delta = datetime.datetime.strptime(str(entrada[0]), "%Y-%m-%d %H:%M:%S.%f%z")#Transforma el string de la hora de entrada al tipo de dato datetime
    fecha = delta.strftime("%Y-%m-%d %H:%M:%S.%f")#Transforma lo anterior a string con un nuevo formato de datetime para evitar corrupciones
    fecha1 = datetime.datetime.strptime(str(fecha), "%Y-%m-%d %H:%M:%S.%f") #Convertimos el string nuevamente a un dato tipo datetime
    fecha2 = datetime.datetime.strptime(str(now), "%Y-%m-%d %H:%M:%S.%f") #Convertimos el string a un dato tipo datetime
    tiempo = fecha2 - fecha1  #Hacemos la resta teniendo como primer fecha la actual para no tener un valor negativo en el tiempo
    time_oobj = time.gmtime(tiempo.total_seconds())
    dias = tiempo.days
    testi = time.strftime(":%H:%M:%S",time_oobj)
    tiempo = str(dias) + str(testi)
    return tiempo

def datos_detalle_parking():
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM detail_parking;")
    data = cursor.fetchall()
    cursor.close()
    conexion.close()
    return data

def data_for_view_parking(): #Obtiene todos los datos necesarios para poder crear la visualizacion del estacionamiento
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM hlugar where seccion = 'A' ORDER BY numero")
    Autos = cursor.fetchall()
    aLenght = len(Autos)#Saber la cantidad de registros encontrados
    anL = floor(aLenght/10) #Cuantas lineas son empezando en 0\
    cursor.execute("SELECT * FROM hlugar where seccion = 'D' ORDER BY numero")
    Discapacitados = cursor.fetchall()
    dLenght = len(Discapacitados)#Saber la cantidad de registros encontrados
    dnL = floor(dLenght/10)#Cuantas lineas son empezando en 0\
    cursor.execute("SELECT * FROM hlugar where seccion = 'M' ORDER BY numero")
    Motos = cursor.fetchall()
    mLenght = len(Motos)#Saber la cantidad de registros encontrados
    mnL = floor(mLenght/10)#Cuantas lineas son empezando en 0\
    conexion.close()
    return Autos, aLenght, anL, Discapacitados, dLenght, dnL, Motos, mLenght, mnL 

def data_for_users_table():
    conexion = conectar_db()
    cursor = conexion.cursor()
    query = "SELECT * FROM users ORDER BY id;"
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    conexion.close()
    return data

route = os.path.abspath(os.getcwd())

def generator(id):
    qr = pyqrcode.create(str(id), error='L')
    qr.png(str(id)+'.png', scale = 6)
    shutil.move(str(route)+'/'+str(id)+'.png',str(route)+'/app/QRCodes/img/')

def verificar_nalertas():
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM avisos;")
    avisos = cursor.fetchall()
    n_avisos = len(avisos)
    print("numero de aviso: "+str(n_avisos))
    return n_avisos

    
#Hilos
def verificar_tiempo():
    while True:
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("SELECT ticket FROM hlugar WHERE estado>2")
        ocupados = cursor.fetchall()
        for ocupado in ocupados:
            cursor.execute("SELECT * FROM ticket WHERE id='"+str(ocupado[0])+"'")
            ticket = cursor.fetchone()
            
            if ticket[2] is None:
                formato = "%Y-%m-%d %H:%M:%S.%f"
                now = datetime.datetime.now()
                delta = datetime.datetime.strptime(str(ticket[1]), "%Y-%m-%d %H:%M:%S.%f%z") #Transforma el string de la hora de entrada al tipo de dato datetime
                fecha = delta.strftime(formato) #Transforma lo anterior a string con un nuevo formato de datetime para evitar corrupciones
                fecha1 = datetime.datetime.strptime(str(fecha), formato) #Convertimos el string nuevamente a un dato tipo datetime
                fecha2 = datetime.datetime.strptime(str(now), formato) #Convertimos el string a un dato tipo datetime
                tiempo = fecha2 - fecha1 #Hacemos la resta teniendo como primer fecha la actual para no tener un valor negativo en el tiempo
                
                time_delta = datetime.timedelta(days=1, seconds=43200)
                if (tiempo > time_delta):
                    cursor.execute("SELECT COUNT(*) FROM avisos WHERE id_ticket = '"+str(ticket[0])+"';")
                    n = cursor.fetchone()
                    if (n[0] == 0):
                        cursor.execute("INSERT INTO avisos VALUES (DEFAULT,'"+str(ticket[4])+" ha excedido el tiempo limite', '"+str(ticket[0])+"');")
                time_oobj = time.gmtime(tiempo.total_seconds())
                dias = tiempo.days
                testi = time.strftime(":%H:%M:%S",time_oobj)
                tiempo = str(dias) + str(testi)
                cursor.execute("UPDATE ticket SET tiempo='"+str(tiempo)+"' WHERE id='"+str(ticket[0])+"';") #Actualizamos en la base de datos el tiempo que lleva el lugar ocupado
        conexion.commit()
        conexion.close()
        time.sleep(15)


def eliminar_qr():
    while True:
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("SELECT ticket FROM hlugar WHERE estado>2;")
        ocupados = cursor.fetchall()
        cursor.execute("SELECT id FROM ticket;")
        tickets = cursor.fetchall()
        for ticket in tickets:
            necesario = False
            for ocupado in ocupados:
                if ocupado[0] == ticket[0]:
                    necesario = True
                    qrco = "./app/QRCodes/img/"+ticket[0]+".png"
                    if(os.path.exists(qrco) == False):
                        generator(ticket[0])
            #endFor
            if necesario is False:
                qrco = "./app/QRCodes/img/"+ticket[0]+".png"
                if(os.path.exists(qrco) == True):
                    os.remove(path=qrco)
        #endFor
        conexion.commit()
        conexion.close()
        time.sleep(30)
    #endWhile

#Rutas de prueba
@app.route("/testview")
def testview():
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM hlugar ORDER BY id ASC;')
    data = cursor.fetchall()
    conexion.close()
    cursor.close()
    return render_template('/estacionamiento/view-detailed.html', find='', data=data, n_avisos=verificar_nalertas())

def generate():
    
    cap = cv2.VideoCapture(0)
    while True:
    # Leemos los frames
        ret, frame = cap.read()

        # Leemos los codigos QR
        for codes in decode(frame):
            # Extraemos info
            #info = codes.data

            # Decodidficamos
            info = codes.data.decode('utf-8')

            # Tipo de persona LETRA
            

            # Extraemos coordenadas
            pts = np.array([codes.polygon], np.int32)
            xi, yi = codes.rect.left, codes.rect.top

            # Redimensionamos
            pts = pts.reshape((-1,1,2))

            
            cv2.polylines(frame, [pts], True, (255, 255, 0), 5)
            cv2.putText(frame, str(info), (xi - 15, yi - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 55, 0), 2)
            print(" Numero de Ticket: ", str(info))
            if(info != ''):
                id_t = info
                with app.app_context(), app.test_request_context():
                    return render_template('/test/info.html', codigo=id_t)
                    cap.release()
            # Imprimimo
            # Mostramos FPS
            # Leemos teclado
        (flag, encodeImage) = cv2.imencode(".jpg", frame)
        if not flag:
            continue
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodeImage) + b'\r\n')
    cap.release()

@app.route("/testcamera")
def testcamera():
    return render_template('/test/camera.html')

@app.route("/video_feed")
def video_feed():
    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")

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
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        query = "SELECT * FROM users WHERE usuario='"+str(_usuario)+"';"
        cursor.execute(query)
        find = cursor.fetchone()
        cursor.close()
        conexion.close()
        if find[2] == _password:
            session["login"] = True
            session["usuario"] = find[3]
            session["id"] = find[0]
            session["view"] = find[4]
            print(find[3])
            print(find[0])
            print(session["id"])
            return redirect("/")
    except (Exception, psycopg2.DatabaseError) as error:
        print("No encontrado")
    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()
    return render_template("login.html", mensaje = "Acceso denegado")

@app.route("/LogOut")
def logout():
    session.clear()
    return redirect("/login")

#hilos
#hilo1 = threading.Timer(5, function=verificar_tiempo)
#hilo2 = threading.Timer(10, function=eliminar_qr)
#hilo1.start()
#hilo2.start()

if __name__ == '__main__':
    app.run(debug=True)

