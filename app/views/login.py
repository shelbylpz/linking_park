from flask import Blueprint , render_template, session, redirect, request
from funciones import *

loginLogout = Blueprint('loginLogout', __name__, template_folder='templates')
#Rutas de Login y Logout
@loginLogout.route("/login")
def login():
    if "login" in session:
        return redirect("/")
    return render_template("login.html")

@loginLogout.route("/login", methods=['POST'])
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

@loginLogout.route("/LogOut")
def logout():
    session.clear()
    return redirect("/login")