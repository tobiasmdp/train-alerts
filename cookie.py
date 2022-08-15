import requests
from lxml import html
import time
from datetime import datetime
import smtplib

init_url = 'https://webventas.sofse.gob.ar'
req_url = 'https://webventas.sofse.gob.ar/servicio.php'
body = {"text":"busqueda%5Btipo_viaje%5D=1&busqueda%5Borigen%5D=16&busqueda%5Bdestino%5D=496&busqueda%5Bfecha_ida%5D=18%2F08%2F2022&busqueda%5Bfecha_vuelta%5D=&busqueda%5Bcantidad_pasajeros%5D%5Badulto%5D=4&busqueda%5Bcantidad_pasajeros%5D%5Bjubilado%5D=0&busqueda%5Bcantidad_pasajeros%5D%5Bmenor%5D=0&busqueda%5Bcantidad_pasajeros%5D%5Bbebe%5D=0"}
s=requests.Session()
init_r = s.post(init_url, data=body)
cookies = init_r.cookies.get_dict()
req_r = s.post(init_url, data=body, cookies=init_r.cookies)

tree = html.fromstring(req_r.content)
dias = tree.xpath('//span[@class="dia_numero"]/text()')
dias_no_disponible = tree.xpath('//span[@class="dia_numero_no_disponible"]/text()')
print(req_r.cookies.get_dict())
print(dias)
print(dias_no_disponible)
