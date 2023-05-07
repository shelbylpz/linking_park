import pyqrcode
import png
import os, shutil
from pyqrcode import QRCode
import time

def generator(id):
    qr = pyqrcode.create(str(id), error='L')
    qr.png(str(id)+'.png', scale = 6)
    shutil.move('./'+str(id)+'.png','./app/QRCodes/img/')
    
def generator_after_out(id):
    qr = pyqrcode.create(str(id), error='L')
    qr.png(str(id)+'.png', scale = 6)
    shutil.move('./'+str(id)+'.png','./app/QRCodes/img/')