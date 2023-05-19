import pyqrcode
import png
import os, shutil
from pyqrcode import QRCode
import time

route = os.path.abspath(os.getcwd())

def generator(id):
    qr = pyqrcode.create(str(id), error='L')
    qr.png(str(id)+'.png', scale = 6)
    shutil.move(str(route)+'/'+str(id)+'.png',str(route)+'/app/QRCodes/img/')
    
def generator_after_out(id):
    qr = pyqrcode.create(str(id), error='L')
    qr.png(str(id)+'.png', scale = 6)
    shutil.move(str(route)+'/'+str(id)+'.png',str(route)+'/app/QRCodes/img/')