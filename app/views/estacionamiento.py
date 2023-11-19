from flask import Blueprint , render_template, session, redirect, request
from funciones import *

estacionamientoView = Blueprint('estacionamiento', __name__, template_folder='templates')
@estacionamientoView.route("/estacionamiento/")
def estacionamiento():
    if not 'login' in session:
        return redirect('/login')
    n_avisos = verificar_nalertas()
    return render_template("estacionamiento.html", n_avisos=n_avisos, usuario=session['usuario'])

@estacionamientoView.route("/estacionamiento/inout")
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
@estacionamientoView.route('/estacionamiento/ver')
def estacionamiento_ver():
    if not 'login' in session:
        return redirect('/login')
    n_avisos = verificar_nalertas()
    find=''
    Autos, aLenght, anL, Discapacitados, dLenght, dnL, Motos, mLenght, mnL = data_for_view_parking()
    return render_template("/estacionamiento/ver.html",  n_avisos=n_avisos, find=find,Autos=Autos, Discapacitados=Discapacitados, Motos=Motos, aLenght=aLenght, dLenght=dLenght, mLenght=mLenght, anL=anL, dnL=dnL, mnL=mnL, usuario=session['usuario'])

#Busqueda de un lugar dentro de visualizar
@estacionamientoView.route('/estacionamiento/ver/search', methods=["POST"])
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
        if (find[0][3] == 1):
            idTcket = find[0][5]
            print(idTcket)
            cursor.execute("SELECT entrada, salida FROM ticket WHERE id='"+idTcket+"';")
            entrada = cursor.fetchone()
            if entrada[1] == 'null':
                tiempo = update_time(entrada[0])
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

@estacionamientoView.route('/estacionamiento/search')
def estacionamiento_search():
    if not 'login' in session:
        return redirect('/login')
    
    n_avisos = verificar_nalertas()
    find = ''
    tipo = ''
    return render_template('/estacionamiento/splace.html',n_avisos=n_avisos, find=find, tipo=tipo, usuario=session['usuario'])

@estacionamientoView.route('/estacionamiento/search/find', methods=['POST'])
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
            if (find[0][3] == 1):
                qrco = str(route)+"/app/QRCodes/img/"+str(find[0][5])+".png" #Asigna ruta de qr a variable
                print(qrco)
                if(os.path.exists(qrco) == False): # Se verifica que el archivo exista si no se genera
                    print('Se intento generar QR')
                    print(find[0][5])
                    generator(find[0][5])
            tipo = 'l'
        if _tipo == 'ticket':
            print('Se intento buscar ticket')
            cursor.execute("SELECT entrada, salida FROM ticket WHERE id='"+_lugar+"';")
            entrada = cursor.fetchone()
            print(entrada[1])
            if entrada[1] is None:
                tiempo = update_time(entrada[0])
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
