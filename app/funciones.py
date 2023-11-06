from flask import render_template, session
from math import floor,ceil
import datetime
import time
import pyqrcode
import os, shutil
import psycopg2
from pyqrcode import QRCode #Esta tambien es escencial para el funcionamiento del programa

def conectar_db():
    conn = psycopg2.connect(
      database="linking_park", 
      user='postgres', 
      password='RTvAsfCAv3neSn', 
      host='serverproyectoxdbbdd.postgres.database.azure.com', 
      port= '5432'
   )
    return conn

def verificar_nalertas():
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM avisos;")
    avisos = cursor.fetchall()
    n_avisos = len(avisos)
    print("numero de aviso: "+str(n_avisos))
    return n_avisos

def configuracion_precios_delete(id):
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        query = "DELETE FROM conversion WHERE id="+str(id)+";"
        cursor.execute(query)
        conexion.commit()
        conexion.close()
        mensaje = ["success","Precio eliminado!","El precio ha sido eliminado correctamente!"]
        return render_template('/configuracion/precios.html',mensaje=mensaje, precios=datos_pago_parking_fixed(), n_avisos=verificar_nalertas())
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error durante la ejecucion de la consulta: ", error)
    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()
    return render_template('/configuracion/precios.html', precios=datos_pago_parking_fixed(), usuario=session['usuario'], n_avisos=verificar_nalertas())

#Funciones modulacion

def update_time(entrada):
    now = datetime.datetime.now()
    delta = datetime.datetime.strptime(str(entrada), "%Y-%m-%d %H:%M:%S.%f%z")#Transforma el string de la hora de entrada al tipo de dato datetime
    fecha = delta.strftime("%Y-%m-%d %H:%M:%S.%f")#Transforma lo anterior a string con un nuevo formato de datetime para evitar corrupciones
    fecha1 = datetime.datetime.strptime(str(fecha), "%Y-%m-%d %H:%M:%S.%f") #Convertimos el string nuevamente a un dato tipo datetime
    fecha2 = datetime.datetime.strptime(str(now), "%Y-%m-%d %H:%M:%S.%f") #Convertimos el string a un dato tipo datetime
    tiempo = fecha2 - fecha1  #Hacemos la resta teniendo como primer fecha la actual para no tener un valor negativo en el tiempo
    time_oobj = time.gmtime(tiempo.total_seconds())
    dias = tiempo.days
    testi = time.strftime(":%H:%M:%S",time_oobj)
    tiempo = str(dias) + str(testi)
    return tiempo

def obtener_conversiones(segundos, dias):
    data = datos_pago_parking()
    cobro = 0
    ld = len(data)
    i = 0
    for x in data:
        if (segundos <= x[2] and dias <= x[3]):
            cobro = x[1]
            return cobro
        if (i+1) == ld:
            cobro = x[1]   
        i = i + 1
    return cobro

def monto_pago(entrada):
    now = datetime.datetime.now()
    delta = datetime.datetime.strptime(str(entrada), "%Y-%m-%d %H:%M:%S.%f%z")#Transforma el string de la hora de entrada al tipo de dato datetime
    fecha = delta.strftime("%Y-%m-%d %H:%M:%S.%f")#Transforma lo anterior a string con un nuevo formato de datetime para evitar corrupciones
    fecha1 = datetime.datetime.strptime(str(fecha), "%Y-%m-%d %H:%M:%S.%f") #Convertimos el string nuevamente a un dato tipo datetime
    fecha2 = datetime.datetime.strptime(str(now), "%Y-%m-%d %H:%M:%S.%f") #Convertimos el string a un dato tipo datetime
    tiempo = fecha2 - fecha1  #Hacemos la resta teniendo como primer fecha la actual para no tener un valor negativo en el tiempo
    segundos = int(tiempo.total_seconds())#da los segundos en el tiempo hasta llegar al dia
    
    dias = tiempo.days
    cobro = obtener_conversiones(segundos, dias)

    return cobro

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

def datos_pago_parking():
    conexion = conectar_db()
    cursor = conexion.cursor()
    query = "SELECT * FROM conversion ORDER BY precio ASC;"
    cursor.execute(query)
    data = cursor.fetchall()
    conexion.commit()
    cursor.close()
    conexion.close()
    return data

def datos_pago_parking_fixed():
    conexion = conectar_db()
    cursor = conexion.cursor()
    query = "SELECT * FROM conversion ORDER BY precio ASC;"
    cursor.execute(query)
    data = cursor.fetchall()
    conexion.commit()
    cursor.close()
    conexion.close()
    precios = []
    for dato in data:
        segundos = dato[2]
        tiempo = str(datetime.timedelta(seconds=segundos))
        new = [dato[0],dato[1],tiempo]
        precios.append(new)
    return precios

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