import requests
import json
from lxml import html
import time
from datetime import datetime

##================= const =================##
botToken = '5140137870:AAEvAV7xaUOyjLR4uMFcIMnUtZG5VhOaMvQ'
baseUrl = f'https://api.telegram.org/bot{botToken}'

recipients_data = {
    'tobias' : '1101456056',
    'mariano' : '1915448150',
    'franco' : '1102019541'
}
admin_list = [recipients_data['tobias']]
user_list = [recipients_data['tobias'],recipients_data['mariano'],recipients_data['franco']]

dias_buscados = ['VIE 19 AGO','SAB 20 AGO']

frecuencia = 30 #frecuencia de requests
notify_time = [1,47] #minutos en los que se notifica que el script esta andando

error_msg = 'Algo salio mal, la aplicacion paro.'
success_msg = 'Pasajes disponibles para el: '
start_msg = 'Hola! Estoy buscando pasajes para ' + str(dias_buscados)

##================= functions =================##
def sendMessage(message,recipients):
    response = []
    for chatID in recipients:
        url= f'{baseUrl}/sendMessage?chat_id={chatID}&text={message}'
        response.append(requests.get(url))
    return response


##================= main =================##
dias_notificados = []
on = True

s = requests.Session()
r = s.post('https://webventas.sofse.gob.ar/ajax/busqueda/obtener_busqueda.php')
r = s.get('https://webventas.sofse.gob.ar/ajax/busqueda/obtener_estaciones.php?id_unico_estacion_seleccionada=0')
estaciones_ida = json.loads(r.text)['estaciones']
r = s.get('https://webventas.sofse.gob.ar/ajax/busqueda/obtener_estaciones.php?id_unico_estacion_seleccionada=255')
estaciones_vuelta = json.loads(r.text)['estaciones']

headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'} #necesario para mandar raw data ya sea URLencoded o no
r = s.post('https://webventas.sofse.gob.ar/ajax/busqueda/obtener_cantidad_maxima_pasajeros.php', data = 'id_unico_origen=255&id_unico_destino=481', headers = headers)

sendMessage(start_msg,admin_list)
while on:
    r = s.post('https://webventas.sofse.gob.ar/calendario.php', data = 'busqueda%5Btipo_viaje%5D=2&busqueda%5Borigen%5D=255&busqueda%5Bdestino%5D=481&busqueda%5Bfecha_ida%5D=19%2F08%2F2022&busqueda%5Bfecha_vuelta%5D=22%2F08%2F2022&busqueda%5Bcantidad_pasajeros%5D%5Badulto%5D=4&busqueda%5Bcantidad_pasajeros%5D%5Bjubilado%5D=0&busqueda%5Bcantidad_pasajeros%5D%5Bmenor%5D=0&busqueda%5Bcantidad_pasajeros%5D%5Bbebe%5D=0', headers = headers)

    tree = html.fromstring(r.content)
    dias = tree.xpath('//span[@class="dia_numero"]/text()')
    dias_no_disponible = tree.xpath('//span[@class="dia_numero_no_disponible"]/text()')
    

    now = datetime.now()
    if now.minute in notify_time and now.second < frecuencia: #cada 15 minutos
        mensaje = now.strftime("%H:%M:%S")
        sendMessage(mensaje,admin_list)
        print(mensaje)
    if not dias and not dias_no_disponible:
        mensaje = error_msg
        sendMessage(mensaje,user_list)
        print(mensaje)
    else:
        for dia in dias:
            if dia not in dias_notificados:
                dias_notificados.append(dia) 
                if dia in dias_buscados: #filtro para notificar solo este dia
                    sendMessage(success_msg + dia, user_list)
        for dia_no_disponible in dias_no_disponible:
            if dia_no_disponible in dias_notificados:
                dias_notificados.remove(dia_no_disponible)            
        print("dias disponibles: ",dias)
        print("dias notificados: ",dias_notificados)
        print("dias no disponibles: ",dias_no_disponible)
        

        time.sleep(frecuencia)