import psycopg2
import datetime
import time
import os

def conectar_db():
    conexion = psycopg2.connect(
        user = 'postgres',
        password = '22042003-a',
        host = 'azure-flask-dbapp.postgres.database.azure.com',
        port = '5432',
        database = 'LinkingParkDB'
    )
    return conexion

def verificar_tiempo():
    while True:
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("SELECT ticket FROM lugar WHERE disponible=False")
        ocupados = cursor.fetchall()
        cantidad = len(ocupados)
        print(cantidad)
        print(ocupados)
        for ocupado in ocupados:
            cursor.execute("SELECT * FROM ticket WHERE id='"+str(ocupado[0])+"'")
            ticket = cursor.fetchone()
            print(ticket)
            if ticket[2] is None:
                    formato = "%Y-%m-%d %H:%M:%S.%f"
                    now = datetime.datetime.now()
                    delta = datetime.datetime.strptime(str(ticket[1]), "%Y-%m-%d %H:%M:%S.%f%z") #Transforma el string de la hora de entrada al tipo de dato datetime
                    fecha = delta.strftime(formato) #Transforma lo anterior a string con un nuevo formato de datetime para evitar corrupciones
                    fecha1 = datetime.datetime.strptime(str(fecha), formato) #Convertimos el string nuevamente a un dato tipo datetime
                    fecha2 = datetime.datetime.strptime(str(now), formato) #Convertimos el string a un dato tipo datetime
                    tiempo = fecha2 - fecha1 #Hacemos la resta teniendo como primer fecha la actual para no tener un valor negativo en el tiempo
                    time_oobj = time.gmtime(tiempo.total_seconds())
                    dias = tiempo.days
                    testi = time.strftime(":%H:%M:%S",time_oobj)
                    tiempo = str(dias) + str(testi)
                    print(testi)
                    print(tiempo)
                    cursor.execute("UPDATE ticket SET tiempo='"+str(tiempo)+"' WHERE id='"+str(ticket[0])+"';") #Actualizamos en la base de datos el tiempo que lleva el lugar ocupado
        conexion.commit()
        conexion.close()
        time.sleep(60)


def eliminar_qr():
    while True:
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("SELECT ticket FROM lugar WHERE disponible=False;")
        ocupados = cursor.fetchall()
        cursor.execute("SELECT id FROM ticket;")
        tickets = cursor.fetchall()
        for ticket in tickets:
            necesario = False
            for ocupado in ocupados:
                if ocupado[0] == ticket[0]:
                    necesario = True
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

