import requests
from lxml import html
import time
from datetime import datetime

import smtplib

botToken = '5140137870:AAEvAV7xaUOyjLR4uMFcIMnUtZG5VhOaMvQ'
chatID = 1101456056
baseUrl = f'https://api.telegram.org/bot{botToken}'

url = 'https://webventas.sofse.gob.ar/calendario.php'
cookies = {"Cookie" : "PHPSESSID=a4b0b785oibjg64f2l0mffghj1; _ga=GA1.1.1492875941.1646085237; G_ENABLED_IDPS=google; _ga_QFTZSXX3LJ=GS1.1.1647381073.16.1.1647436492.0"}

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



def sendMessage(message):
    url= f'{baseUrl}/sendMessage?chat_id={chatID}&text={message}'
    response = requests.get(url)
    return response.json()

sendMessage("Hola!")
segundos = 0
dias_notificados = []
while True: 
    print('-------------------------------')
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("-------------", current_time,"-------------")

    dias, dias_no_disponible = solicitud(255, 481, 27, 7, 2022) #origen, destino, dia, mes, anio

    
    if not dias and not dias_no_disponible:
        print ("cookie vencida en ", segundos," segundos")
        #sendMessage(f"cookie vencida en {segundos} segundos")
        segundos = 0
    else:
        for dia in dias:
            if dia not in dias_notificados:
                dias_notificados.append(dia)
                if dia == 'LUN 19 SEP' or dia == 'MAR 20 SEP': #filtro para notificar solo este dia
                    sendMessage('pasajes disponibles para el '+dia)
                    sendMessageBauti('pasajes disponibles para el '+dia) #borrar es temporal
        for dia_no_disponible in dias_no_disponible:
            if dia_no_disponible in dias_notificados:
                dias_notificados.remove(dia_no_disponible)            
        print("dias disponibles: ",dias)
        print("dias notificados: ",dias_notificados)
        print("dias no disponibles: ",dias_no_disponible)
        

    time.sleep(10)
    segundos += 1
