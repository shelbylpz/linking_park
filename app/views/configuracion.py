from flask import Blueprint , render_template, session, redirect, request
from funciones import *

configuracion = Blueprint('configuracion', __name__, template_folder='templates')


@configuracion.route('/configuracion/agregar')
def configuracion_agregar():
    if not 'login' in session:
        return redirect('/login')
    if session['usuario'] != 'Administrador':
        return redirect('/')
    n_avisos = verificar_nalertas()
    Autos, aLenght, anL, Discapacitados, dLenght, dnL, Motos, mLenght, mnL = data_for_view_parking()
    return render_template("/configuracion/addplace.html",n_avisos=n_avisos, Autos=Autos, Discapacitados=Discapacitados, Motos=Motos, aLenght=aLenght, dLenght=dLenght, mLenght=mLenght, anL=anL, dnL=dnL, mnL=mnL, usuario=session['usuario'])

@configuracion.route('/configuracion/agregar/add', methods=['POST'])
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

@configuracion.route('/configuracion/borrar')
def configuracion_borrar():
    if not 'login' in session:
        return redirect('/login')
    if session['usuario'] != 'Administrador':
        return redirect('/')
    n_avisos = verificar_nalertas()
    Autos, aLenght, anL, Discapacitados, dLenght, dnL, Motos, mLenght, mnL = data_for_view_parking()
    return render_template('/configuracion/removeplace.html',n_avisos=n_avisos, Autos=Autos, Discapacitados=Discapacitados, Motos=Motos, aLenght=aLenght, dLenght=dLenght, mLenght=mLenght, anL=anL, dnL=dnL, mnL=mnL, usuario=session['usuario'])

@configuracion.route('/configuracion/borrar/delete', methods=['POST'])
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
    if (data[3] == '1'):
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

@configuracion.route('/configuracion/modificar')
def configuracion_modificar():
    if not 'login' in session:
        return redirect('/login')
    if session['usuario'] != 'Administrador':
        return redirect('/')
    Autos, aLenght, anL, Discapacitados, dLenght, dnL, Motos, mLenght, mnL = data_for_view_parking()
    return render_template('/configuracion/modplace.html', n_avisos=verificar_nalertas(), Autos=Autos, Discapacitados=Discapacitados, Motos=Motos, aLenght=aLenght, dLenght=dLenght, mLenght=mLenght, anL=anL, dnL=dnL, mnL=mnL, usuario=session['usuario'])

@configuracion.route('/configuracion/modificar/update', methods=['POST'])
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
        cursor.execute("UPDATE hlugar SET estado=1, status='no-verificado', ticket='"+str(nticket)+"' WHERE id='"+str(_id)+"'")
        
        generator(nticket)
    else:
        if find[6] == 'no-verificado':
            cursor.execute("UPDATE hlugar SET status='asignado' WHERE id='"+str(_id)+"';")
        else:
            idticket = find[5]
            cursor.execute("SELECT entrada FROM ticket WHERE id='"+str(idticket)+"';")
            entrada = cursor.fetchone()
            entrada = entrada[0]
            now = datetime.datetime.now()
            tnow = now.strftime("%Y-%m-%d %H:%M:%S.%f") #Convierte la hora actual a un string con un formato definido
            tiempo = update_time(entrada)
            print(tiempo)
            cursor.execute("UPDATE ticket SET salida='"+str(tnow)+"', tiempo='"+str(tiempo)+"' WHERE id='"+str(idticket)+"';")
            cursor.execute("UPDATE hlugar SET estado='0', ticket=null, status='disponible' WHERE id='"+str(_id)+"';")
    conexion.commit()
    conexion.close()
    return redirect('/configuracion/modificar')

@configuracion.route("/configuracion/usuarios")
def configuracion_usuarios():
    if not 'login' in session:
        return redirect('/login')
    if session['usuario'] != 'Administrador':
        return redirect('/')
    return render_template('/configuracion/usuarios.html', registros=data_for_users_table(), usuario=session['usuario'], n_avisos=verificar_nalertas())

@configuracion.route("/configuracion/usuarios", methods=['POST'])
def configuracion_usuarios_post():
    if not 'login' in session:
        return redirect('/login')
    if session['usuario'] != 'Administrador':
        return redirect('/')
    accion = request.form['accion']
    if accion == 'delete':
        return configuracion_users_delete(request.form['id'])
    if accion == 'add':
        return configuracion_usuarios_add(request)
    if accion == 'edit':
        return configuracion_users_edit(request)
    return redirect('/configuracion/usuarios')

def configuracion_usuarios_add(request):
    if not 'login' in session:
        return redirect('/login')
    if session['usuario'] != 'Administrador':
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
        return render_template('/configuracion/usuarios.html', mensaje=mensaje, registros=data_for_users_table(),n_avisos=verificar_nalertas(), usuario=session['usuario'])
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error durante la ejecucion de la consulta: ", error)
    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()
    return render_template('/configuracion/usuarios.html', error=True, registros=data_for_users_table(),n_avisos=verificar_nalertas(), usuario=session['usuario'])

def configuracion_users_delete(_id):
    if not 'login' in session:
        return redirect('/login')
    if session['usuario'] != 'Administrador':
        return redirect('/')
    print(session["id"])
    print(_id)
    if int(_id) == int(session["id"]) :
        mensaje = ["warning","Usuario no eliminado!","El Usuario tiene una session abierta!"]
        return render_template('/configuracion/usuarios.html', mensaje=mensaje, registros=data_for_users_table(), n_avisos=verificar_nalertas(), usuario=session['usuario'])
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        query = "DELETE FROM users WHERE id="+str(_id)+";"
        cursor.execute(query)
        conexion.commit()
        conexion.close()
        mensaje = ["success","Usuario eliminado!","El Usuario ha sido eliminado correctamente!"]
        return render_template('/configuracion/usuarios.html',mensaje=mensaje, registros=data_for_users_table(), n_avisos=verificar_nalertas(), usuario=session['usuario'])
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error durante la ejecucion de la consulta: ", error)
    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()
    return render_template('/configuracion/usuarios.html', registros=data_for_users_table(), n_avisos=verificar_nalertas(), usuario=session['usuario'])

def configuracion_users_edit():
    if not 'login' in session:
        return redirect('/login')
    if session['usuario'] != 'Administrador':
        return redirect('/')
    _id = request.form['txtID']
    print(session["id"])
    print(_id)

@configuracion.route("/configuracion/precios")
def configuracion_precios():
    if not 'login' in session:
        return redirect('/login')
    if session['usuario'] != 'Administrador':
        return redirect('/')
    precios = datos_pago_parking_fixed()
    return render_template('/configuracion/precios.html', usuario=session['usuario'], precios=precios, n_avisos=verificar_nalertas())
    
@configuracion.route("/configuracion/precios", methods=['POST'])
def configuracion_precios_add():
    if not 'login' in session:
        return redirect('/login')
    if session['usuario'] != 'Administrador':
        return redirect('/')
    accion = request.form['accion']
    if accion == 'eliminar':
        return configuracion_precios_delete(request.form['id'])
    if accion == 'agregar':    
        _precio = request.form['txtPrecio']
        _dia = request.form['dia']
        _hora = request.form['hora']
        _minuto = request.form['minuto']
        _segundo = request.form['segundo']
        _tiempo = int(_dia)*86400 + int(_hora)*3600 + int(_minuto)*60 + int(_segundo)
        print(_precio)
        print(_tiempo)
        try:
            conexion = conectar_db()
            cursor = conexion.cursor()
            query = "INSERT INTO conversion VALUES(DEFAULT,'"+str(_precio)+"','"+str(_tiempo)+"','"+str(_dia)+"');"
            cursor.execute(query)
            conexion.commit()
            conexion.close()
            mensaje = ["success","Precio agregado correctamente!", ""]
            return render_template('/configuracion/precios.html', mensaje=mensaje, precios=datos_pago_parking_fixed(), n_avisos=verificar_nalertas(), usuario=session['usuario'])
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error durante la ejecucion de la consulta: ", error)
        finally:
            if cursor is not None:
                cursor.close()
            if conexion is not None:
                conexion.close()
        return render_template('/configuracion/precios.html', error=True, usuario=session['usuario'], precios=datos_pago_parking_fixed(), n_avisos=verificar_nalertas())



