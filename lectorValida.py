# Importamos librerias para lecturas
import cv2
import pyqrcode
import png
from pyqrcode import QRCode
import psycopg2
from pyzbar.pyzbar import decode
import numpy as np
import time


def conectar_db():
    conexion = psycopg2.connect(
        user = 'postgres',
        password = 'password',
        host = 'localhost',
        port = '5432',
        database = 'LinkingParkDB'
    )
    return conexion

# Creamos la videocaptura
cap = cv2.VideoCapture(1)

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
                print(ticket[6])
                if(ticket[6] == False):
                    id = ticket[0]
                    print(id)
                    cursor.execute("UPDATE lugar SET validado='True' WHERE id='"+str(id)+"';")
                    cursor.execute("SELECT * FROM lugar WHERE id='"+str(id)+"';")
                    lugar = cursor.fetchone()
                    print(lugar)
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