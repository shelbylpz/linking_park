import os, shutil
from math import floor,ceil
from flask import Flask, render_template, request, redirect, session, send_from_directory, Response, url_for, make_response
import psycopg2 
import datetime
import time
import threading
#Blueprints
from views.funciones import *
from views.configuracion import configuracion
from views.login import loginLogout
from views.notificaciones import notificaciones
from views.estacionamiento import estacionamientoView
from views.pago import pagos


app = Flask(__name__)
app.register_blueprint(configuracion)
app.register_blueprint(loginLogout)
app.register_blueprint(notificaciones)
app.register_blueprint(estacionamientoView)
app.register_blueprint(pagos)

app.secret_key="bolañazo"

@app.route('/')
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

#hilos
hilo1 = threading.Timer(5, function=verificar_tiempo)
hilo2 = threading.Timer(10, function=eliminar_qr)
hilo1.start()
hilo2.start()

if __name__ == '__main__':
    app.run(debug=True)

