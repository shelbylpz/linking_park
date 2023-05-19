import keyboard
import psycopg2
import datetime
import random
from QRCodes.QRGenerator import generator
from boleto.ticket import gen_Ticket

def conectar_db():
    conexion = psycopg2.connect(
        user = 'postgres',
        password = '22042003-a',
        host = 'azure-flask-dbapp.postgres.database.azure.com',
        port = '5432',
        database = 'LinkingParkDB'
    )
    return conexion

def on_key_press(event):
    if event.name == 'a':
        print('a')
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM lugar WHERE seccion='A' AND disponible=True ORDER BY numero;")
        disponibles = cursor.fetchall()
        ndisp = len(disponibles)
        if ndisp == 0 :
            print("No hay lugares disponibles Lo Siento")
            conexion.close()
        else:
            now = datetime.datetime.now()
            hnow = now.strftime("%Y%m%d%H%M%S")
            tnow = now.strftime("%Y-%m-%d %H:%M:%S.%f")        
            seleccion = random.randint(0,ndisp-1)
            asignado = disponibles[seleccion][0]
            nticket = str(hnow)+"-"+str(asignado)
            print(ndisp)
            print(disponibles)
            print(asignado)
            print(hnow)
            sql = "INSERT INTO ticket(id,entrada,lugar) VALUES ('"+str(nticket)+"','"+str(tnow)+"','"+str(asignado)+"');"
            cursor.execute(sql)
            cursor.execute("UPDATE lugar SET disponible=False, ticket='"+str(nticket)+"' WHERE id='"+str(asignado)+"';")
            generator(nticket)
            gen_Ticket(nticket)
            conexion.commit()
            print(sql)
            conexion.close()
    if event.name == 'd':
        print('d')
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM lugar WHERE seccion='D' AND disponible=True ORDER BY numero;")
        disponibles = cursor.fetchall()
        ndisp = len(disponibles)
        if ndisp == 0:
            print("No hay lugares disponibles, Lo sentimos")
            conexion.close()
        else:
            now = datetime.datetime.now()
            hnow = now.strftime("%Y%m%d%H%M%S")
            tnow = now.strftime("%Y-%m-%d %H:%M:%S.%f")   
            seleccion = random.randint(0,ndisp-1)
            asignado = disponibles[seleccion][0]
            nticket = str(hnow)+"-"+str(asignado)
            print(ndisp)
            print(disponibles)
            print(asignado)
            print(hnow)
            sql = "INSERT INTO ticket(id,entrada,lugar) VALUES ('"+str(nticket)+"','"+str(tnow)+"','"+str(asignado)+"');"
            cursor.execute(sql)
            cursor.execute("UPDATE lugar SET disponible=False, ticket='"+str(nticket)+"' WHERE id='"+str(asignado)+"';")
            generator(nticket)
            gen_Ticket(nticket)
            conexion.commit()
            print(sql)
            conexion.close()
    if event.name == 'm':
        print('m')
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM lugar WHERE seccion='M' AND disponible=True ORDER BY numero;")
        disponibles = cursor.fetchall()
        ndisp = len(disponibles)
        if ndisp == 0:
            print("No hay lugares disponibles, Lo sentimos")
            conexion.close()
        else:
            now = datetime.datetime.now()
            hnow = now.strftime("%Y%m%d%H%M%S")
            tnow = now.strftime("%Y-%m-%d %H:%M:%S.%f")   
            seleccion = random.randint(0,ndisp-1)
            asignado = disponibles[seleccion][0]
            nticket = str(hnow)+"-"+str(asignado)
            print(ndisp)
            print(disponibles)
            print(asignado)
            print(hnow)
            sql = "INSERT INTO ticket(id,entrada,lugar) VALUES ('"+str(nticket)+"','"+str(tnow)+"','"+str(asignado)+"');"
            cursor.execute(sql)
            cursor.execute("UPDATE lugar SET disponible=False, ticket='"+str(nticket)+"' WHERE id='"+str(asignado)+"';")
            generator(nticket)
            gen_Ticket(nticket)
            conexion.commit()
            print(sql)
            conexion.close()

# Configurar el detector de eventos
keyboard.on_press(on_key_press)

# Mantener el programa en ejecución
while True:
    n=0
    pass