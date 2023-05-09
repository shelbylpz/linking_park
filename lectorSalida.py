# Importamos librerias para lecturas
import cv2
import pyqrcode
import png
from pyqrcode import QRCode
import psycopg2
from pyzbar.pyzbar import decode
import numpy as np
import time
import datetime


def conectar_db():
    conexion = psycopg2.connect(
        user = 'postgres',
        password = '22042003-a',
        host = 'azure-flask-dbapp.postgres.database.azure.com',
        port = '5432',
        database = 'LinkingParkDB'
    )
    return conexion

# Creamos la videocaptura
cap = cv2.VideoCapture(0)

# Empezamos
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
            try:
                conexion = conectar_db()
                cursor = conexion.cursor()
                cursor.execute("SELECT * FROM lugar WHERE ticket='"+str(id_t)+"';")
                ticket = cursor.fetchone()
                print(ticket)
                print(ticket[3])
                print(ticket[6])
                if(ticket[6] == True and ticket[3] == False):
                    _id = ticket[0]
                    idticket = ticket[5]
                    cursor.execute("SELECT entrada FROM ticket WHERE id='"+str(idticket)+"';")
                    entrada = cursor.fetchone()
                    now = datetime.datetime.now()
                    tnow = now.strftime("%Y-%m-%d %H:%M:%S.%f") #Convierte la hora actual a un string con un formato definido   
                    delta = datetime.datetime.strptime(str(entrada[0]), "%Y-%m-%d %H:%M:%S.%f%z")#Transforma el string de la hora de entrada al tipo de dato datetime
                    fecha = delta.strftime("%Y-%m-%d %H:%M:%S.%f")#Transforma lo anterior a string con un nuevo formato de datetime para evitar corrupciones
                    fecha1 = datetime.datetime.strptime(str(fecha), "%Y-%m-%d %H:%M:%S.%f") #Convertimos el string nuevamente a un dato tipo datetime
                    fecha2 = datetime.datetime.strptime(str(now), "%Y-%m-%d %H:%M:%S.%f") #Convertimos el string a un dato tipo datetime
                    tiempo = fecha2 - fecha1  #Hacemos la resta teniendo como primer fecha la actual para no tener un valor negativo en el tiempo
                    print(tiempo)
                    cursor.execute("UPDATE ticket SET salida='"+str(tnow)+"', tiempo='"+str(tiempo)+"' WHERE id='"+str(idticket)+"';")
                    cursor.execute("UPDATE lugar SET disponible=DEFAULT, ticket=null, validado=DEFAULT WHERE id='"+str(_id)+"';")
                conexion.commit()
                conexion.close()
                time.sleep(2)
            except(Exception, psycopg2.DatabaseError):
                print("No hay lugar con ese ticket")
            finally:
                if cursor is not None:
                    cursor.close()
                if conexion is not None:
                    conexion.close()
                time.sleep(2)
        # Imprimimos

    # Mostramos FPS
    cv2.imshow(" LECTOR DE QR", frame)
    # Leemos teclado
    t = cv2.waitKey(5)
    if t == 27:
        break

cv2.destroyAllWindows()
cap.release()