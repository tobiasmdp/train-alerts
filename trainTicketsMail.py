import requests
from lxml import html
import time
import telegram_send
from datetime import datetime

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

 
def solicitud(origen, destino, dia, mes, anio):
    if dia < 10:
        dia = '0' + str(dia)
    else:
        dia = str(dia)
    if mes < 10:
        mes = '0' + str(mes)
    else:
        mes = str(mes)
    body = {'texto':'busqueda%5Btipo_viaje%5D=1&busqueda%5Borigen%5D='+ str(origen) + '&busqueda%5Bdestino%5D='+ str(destino) +'&busqueda%5Bfecha_ida%5D='+ dia +'%2F'+ mes +'%2F'+ str(anio) +'&busqueda%5Bfecha_vuelta%5D=&busqueda%5Bcantidad_pasajeros%5D%5Badulto%5D=1&busqueda%5Bcantidad_pasajeros%5D%5Bjubilado%5D=0&busqueda%5Bcantidad_pasajeros%5D%5Bdiscapacitado%5D=0&busqueda%5Bcantidad_pasajeros%5D%5Bmenor%5D=0&busqueda%5Bcantidad_pasajeros%5D%5Bbebe%5D=0'}
    r=requests.post(url, data=body, headers=cookies)
    tree = html.fromstring(r.content)
    dias = tree.xpath('//span[@class="dia_numero"]/text()')
    dias_no_disponible = tree.xpath('//span[@class="dia_numero_no_disponible"]/text()')  
    return dias, dias_no_disponible
    #255 mar del plata / 481 Beunos Aires#

def sendMail(mensaje):
    # create message object instance
    msg = MIMEMultipart()
 
 
    message = mensaje
 
    # setup the parameters of the message
    password = "XFjHYRUREXat5EkcnG13"
    msg['From'] = "tobiasperiodicchecker@gmail.com"
    msg['To'] = "tobiasgiacri@gmail.com"
    msg['Subject'] = "pasaje disponible"
 
    # add in the message body
    msg.attach(MIMEText(message, 'plain'))
 
    #create server
    server = smtplib.SMTP('smtp.gmail.com: 587')
 
    server.starttls()
 
    # Login Credentials for sending the mail
    server.login(msg['From'], password)
 
 
    # send the message via the server.
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    print("mail enviado")
 
    server.quit()



apikeyBOT = '5102379715:AAFdBNW_pQuEIqpfOLK1s1Ixtp6it6KfK6c'

url = 'https://webventas.sofse.gob.ar/calendario.php'
cookies = {"Cookie" : "PHPSESSID=a4b0b785oibjg64f2l0mffghj1; _ga=GA1.1.1492875941.1646085237; G_ENABLED_IDPS=google; _ga_QFTZSXX3LJ=GS1.1.1650987511.26.1.1650999831.0"}


primera_vez_1 = True
primera_vez_2 = True
primera_vez_3 = True
primera_vez_4 = True


while True: 
    print('-------------------------------')
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("-------------", current_time,"-------------")

###################
    dias, dias_no_disponible = solicitud(255, 481, 2, 5, 2022) #origen, destino, dia, mes, anio  
    if not dias and not dias_no_disponible:
        sendMail("me rompi")
        print ("me rompi bro")
    else: 
        print("dias disponibles: "+ str(dias) + "\nDias no disponibles: " + str(dias_no_disponible) + "\n")

        if 'LUN 2 MAY' in dias and primera_vez_4:
            sendMail("hay para el LUN 2 MAY")
            print("hay para el LUN 2 MAY")
            primera_vez_4 = False
        else:
            if 'LUN 2 MAY' not in dias:
                primera_vez_4 = True
    time.sleep(120)
""" 
###################
    dias, dias_no_disponible = solicitud(481, 255, 2, 5, 2022) #origen, destino, dia, mes, anio
    if not dias and not dias_no_disponible:
        sendMail("me rompi")
        print ("me rompi bro")
    else: 
        print("dias disponibles: "+ str(dias) + "\nDias no disponibles: " + str(dias_no_disponible) + "\n")

        if 'LUN 2 MAY' in dias and primera_vez_2:
            sendMail("hay para el LUN 2 MAY")
            print("hay para el LUN 2 MAY")
            primera_vez_2 = False
        else:
            if 'LUN 2 MAY' not in dias:
                primera_vez_2 = True
 """
