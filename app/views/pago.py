from flask import Blueprint , render_template, session, redirect, request
from funciones import *

pagos = Blueprint('pagos', __name__, template_folder='templates')
@pagos.route('/pago/<id>')
def pago(id):
    if not 'login' in session:
        return redirect('/login')
    if session['usuario'] != 'Administrador':
        return redirect('/')
    try:
        conexion =  conectar_db()
        cursor = conexion.cursor()
        query = "SELECT * FROM ticket WHERE id='"+str(id)+"';"
        cursor.execute(query)
        data = cursor.fetchone()
        cursor.execute("SELECT * FROM hlugar WHERE ticket='"+str(id)+"';")
        lugar = cursor.fetchone()
        cursor.close()
        conexion.commit()
        conexion.close()
        print(data)
        if data is None:
            return render_template('/pago/info.html', error='No encontrado',n_avisos=verificar_nalertas(), usuario=session['usuario'])
        if data[2]:
            return render_template('/pago/info.html', error='Boleto Ya pagado',n_avisos=verificar_nalertas(), usuario=session['usuario'])
        if lugar[6] == "no-verificado":
            return render_template('/pago/info.html', error='Boleto no Verificado, Por favor escaneelo en el lugar correspondiente para poder salir.',n_avisos=verificar_nalertas(), usuario=session['usuario'])
        newdata = {
            'id': data[0],
            'entrada': datetime.datetime.strptime(str(data[1]), "%Y-%m-%d %H:%M:%S.%f%z").strftime("%Y-%m-%d %H:%M:%S"),
            'salida': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'tiempo': update_time(data[1]),
            'cobro': monto_pago(data[1])
        }
        return render_template('/pago/info.html',codigo=id, newdata=newdata,n_avisos=verificar_nalertas(), usuario=session['usuario'])
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error durante la ejecucion de la consulta: ", error)
    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()
    return render_template('/pago/info.html', codigo='No encontrado', n_avisos=verificar_nalertas(), usuario=session['usuario'])

@pagos.route('/pago/<id>', methods=['POST'])
def pago_post(id):
    if not 'login' in session:
        return redirect('/login')
    if session['usuario'] != 'Administrador':
        return redirect('/')
    pago = request.form['pago']
    print('Se quizo hacer el pago de '+id)
    print('Se ingreso esta cantidad '+pago)
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM ticket WHERE id='"+str(id)+"';")
    ticket = cursor.fetchone()
    cursor.execute("SELECT * FROM hlugar WHERE ticket='"+str(id)+"';")
    lugar = cursor.fetchone()
    print(ticket)
    print(lugar)
    idticket = ticket[0]
    entrada = ticket[1]
    now = datetime.datetime.now()
    tnow = now.strftime("%Y-%m-%d %H:%M:%S.%f") #Convierte la hora actual a un string con un formato definido
    tiempo = update_time(entrada)
    print(tiempo)
    cursor.execute("UPDATE ticket SET salida='"+str(tnow)+"', tiempo='"+str(tiempo)+"' WHERE id='"+str(idticket)+"';")
    cursor.execute("UPDATE hlugar SET estado='0', ticket=null, status='disponible' WHERE id='"+str(lugar[0])+"';")
    cursor.execute("INSERT INTO public.pago(id_ticket, pago, fecha)	VALUES ('"+str(idticket)+"', "+str(pago)+", '"+str(tnow)+"');")
    conexion.commit()
    conexion.close()
    return redirect('/')