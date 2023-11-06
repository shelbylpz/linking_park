from flask import Blueprint , render_template, session, redirect, request
from funciones import *

notificaciones = Blueprint('notificaciones', __name__, template_folder='templates')
@notificaciones.route('/alertas')
def avisos():
    if not 'login' in session:
        return redirect('/login')
    n_avisos = verificar_nalertas()
    return render_template("/notificaciones/alertas.html", n_avisos=n_avisos, usuario=session['usuario'])

@notificaciones.route("/alertas/<table>")
def avisos_seleccion(table):
    if not 'login' in session:
        return redirect('/login')
    n_avisos = verificar_nalertas()
    datos, tipo = datos_tipo(table)
    print(datos)
    return render_template("/notificaciones/alertas.html",n_avisos=n_avisos, datos=datos, tipo=tipo, usuario=session['usuario'])

@notificaciones.route('/alertas/informar', methods=["POST"])
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
