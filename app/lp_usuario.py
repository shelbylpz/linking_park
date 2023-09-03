import keyboard
import psycopg2
import datetime
import random
from QRCodes.QRGenerator import generator
from boleto.ticket import gen_Ticket, imprimirboleto
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from _tkinter import TclError
from connect import conectar_db



def asignar_lugar(seccion):
    print(seccion)
    conexion = conectar_db()
    cursor = conexion.cursor()
    if (seccion == 'a'):
        cursor.execute("SELECT * FROM lugar WHERE seccion='A' AND disponible=True ORDER BY numero;")
    if (seccion == 'd'):
        cursor.execute("SELECT * FROM lugar WHERE seccion='D' AND disponible=True ORDER BY numero;")
    if (seccion == 'm'):
        cursor.execute("SELECT * FROM lugar WHERE seccion='M' AND disponible=True ORDER BY numero;")
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

def on_key_press(event):
    if event.name == 'a':
        asignar_lugar('a')
    if event.name == 'd':
        asignar_lugar('d')
    if event.name == 'm':
        asignar_lugar('m')

#programa de cesar
def boletos(seccion):
    if seccion == 'a':
        try:
            asignar_lugar('a')
        except:
            TIME_TO_WAIT = 3500
            root = Tk() 
            root.withdraw()
            try:
                root.after(TIME_TO_WAIT, root.destroy) 
                messagebox.Message(title="Cajones no disponibles", message="Ya no hay cajones de automovil disponibles", master=root).show()
            except TclError:
                pass
    if seccion == 'd':
        try:
            asignar_lugar('d')
        except:
            TIME_TO_WAIT = 3500
            root = Tk() 
            root.withdraw()
            try:
                root.after(TIME_TO_WAIT, root.destroy) 
                messagebox.Message(title="Cajones no disponibles", message="Ya no hay cajones especiales disponibles", master=root).show()
            except TclError:
                pass
    if seccion == 'm':
        try:
            asignar_lugar('m')
        except:
            TIME_TO_WAIT = 3500
            root = Tk() 
            root.withdraw()
            try:
                root.after(TIME_TO_WAIT, root.destroy) 
                messagebox.Message(title="Cajones no disponibles", message="Ya no hay cajones de motos disponibles", master=root).show()
            except TclError:
                pass



#Nuestro programa



# Configurar el detector de eventos
keyboard.on_press(on_key_press)
# Mantener el programa en ejecución

root = Tk()
root.title('LINKING PARK')
root.iconbitmap('app\\templates\\img\\icono.ico')
root.resizable(False, False)
root.config(width=650, height=300)

# --------------------Header--------------------
header = Label(root, text='')
header.config(bg='#080F1B', width=1200, height=6)
header.place(x=0, y=0)

bienvenida = Label(root, bg='#080F1B', text='Bienvenido al estacionamiento' ,fg='white',  font=('Helvetica', 25, 'bold'))
bienvenida.place(x=150, y=25)

logoImagen = PhotoImage(file='app\\templates\\img\\logo-test.gif')
labelImagen = Label(root, image=logoImagen)
labelImagen.config(width=100, height=85, bg='black')
labelImagen.place(x=10, y=5)

# --------------------Body----------------------
botonDiscapacitado = Button(root, padx=10, fg='black', bg='#C3E0FC', font=('Helvetica', 30, 'bold'), text='Discapacitado', command=lambda: boletos('d'))
botonDiscapacitado.place(x=160, y=155)

botonNormal = Button(root, padx=10, fg='black', bg='#FDFF8E', font=('Helvetica', 30, 'bold'), text='Auto', command=lambda: boletos('a'))
botonNormal.place(x=10, y=155)

botonMoto = Button(root, padx=10, fg='black', bg='#FDFF8E', font=('Helvetica', 30, 'bold'), text='Moto', command=lambda: boletos('m'))
botonMoto.place(x=490, y=155)

root.mainloop()
while True:
    n=0
    pass