import pdfkit
from jinja2 import FileSystemLoader, Environment
from datetime import datetime
import os
import pathlib
import printfactory
import subprocess

route = os.path.abspath(os.getcwd())
print(route)

def gen_Ticket(id):
    path_to_pdf = r'.\.lib-external\wkhtmltopdf\bin\wkhtmltopdf.exe'

    print(id)
    #Datos del ticket
    fecha = str(id[0:4])+"/"+str(id[4:6])+"/"+str(id[6:8])
    print(fecha)
    hora = str(id[8:10])+":"+str(id[10:12])+":"+str(id[12:14])
    print(hora)
    letra = str(id[15])
    print(letra)
    numero = id[16]
    print(numero)
    file_path =route+r'\app\QRCodes\img\\'+id+r'.png'
    logo_path = route+r'\app\boleto\ticket\logo.jpg'
    print(file_path)
    context = {'fecha':fecha, 'hora': hora, 'file_path':file_path, 'letra':letra, 'numero':numero, 'logo_path':logo_path, 'idticket':id}

    #point pdfkit configuration
    config = pdfkit.configuration(wkhtmltopdf = path_to_pdf)
    

    #Generar pdf
    template_loader = FileSystemLoader('./')
    template_env = Environment(loader=template_loader)
    template = template_env.get_template('app/boleto/ticket/boleto.html')
    output_text = template.render(context)

    pdfkit.from_string(output_text, output_path='app/boleto/ticket/ticket.pdf', configuration=config, css='app\\boleto\\ticket\style.css', options={"enable-local-file-access":""})
    config = pdfkit.configuration(wkhtmltopdf=path_to_pdf)
    options = {
        'enable-local-file-access': '',
        'page-size': 'A7',
        'margin-top': '0mm',
        'margin-right': '0mm',
        'margin-bottom': '0mm',
        'margin-left': '0mm',
        'encoding': 'UTF-8',
        'no-outline': None
    }

    pdfkit.from_string(output_text, output_path='app/boleto/ticket/ticket.pdf', configuration=config, css='app\\boleto\\ticket\style.css', options=options)
    

def imprimirboleto():
    printer = printfactory.Printer()
    print_tool = printfactory.AdobeAcrobat(printer)

    filePdf = pathlib.Path('app/boleto/ticket/ticket.pdf')
    print_tool.timeout = 10
    
    print_tool.print_file(filePdf)

def abrirboleto():
    abrir_pdf('app/boleto/ticket/ticket.pdf')

def abrir_pdf(file_path):
    try:
        subprocess.run(['xdg-open', file_path])  # Linux
    except FileNotFoundError:
        try:
            subprocess.run(['open', file_path])  # macOS
        except FileNotFoundError:
            try:
                subprocess.run(['start', file_path], shell=True)  # Windows
            except FileNotFoundError:
                print("No se pudo abrir el archivo PDF.")

# Ejemplo de uso

