import requests 
from lxml import html

cookie_url = 'https://webventas.sofse.gob.ar/'
calendar_url = 'https://webventas.sofse.gob.ar/calendario.php'
#a4b0b785oibjg64f2l0mffghj1

#PHPSESSID=a4b0b785oibjg64f2l0mffghj1; 
#_ga=GA1.1.1492875941.1646085237; 
#G_ENABLED_IDPS=google; 
#_ga_QFTZSXX3LJ=GS1.1.1658002178.36.1.1658003451.0



r = requests.post(cookie_url)
cookie = r.cookies.get('PHPSESSID')
cookie = "a4b0b785oibjg64f2l0mffghj1"
cookies_string = "PHPSESSID="+ cookie +"; _ga=GA1.1.1492875941.1646085237; G_ENABLED_IDPS=google; _ga_QFTZSXX3LJ=GS1.1.1647381073.16.1.1647436492.0"
cookies_dic = {"Cookie" : cookies_string}
print(f'Cookies from a common post request {cookies_dic}')

body = 'busqueda%5Btipo_viaje%5D=1&busqueda%5Borigen%5D=481&busqueda%5Bdestino%5D=255&busqueda%5Bfecha_ida%5D=28%2F04%2F2022&busqueda%5Bfecha_vuelta%5D=&busqueda%5Bcantidad_pasajeros%5D%5Badulto%5D=1&busqueda%5Bcantidad_pasajeros%5D%5Bjubilado%5D=0&busqueda%5Bcantidad_pasajeros%5D%5Bdiscapacitado%5D=0&busqueda%5Bcantidad_pasajeros%5D%5Bmenor%5D=0&busqueda%5Bcantidad_pasajeros%5D%5Bbebe%5D=0'

r = requests.post(calendar_url, data=body, headers=cookies_dic)
tree = html.fromstring(r.content)
dias = tree.xpath('//span[@class="dia_numero"]/text()')
dias_no_disponible = tree.xpath('//span[@class="dia_numero_no_disponible"]/text()')

print("hola")   


session = requests.session()
r_session = session.get(calendar_url)
print(r_session.cookies)
cookie = r_session.cookies.get('PHPSESSID')
cookies_string = "PHPSESSID="+ cookie +"; _ga=GA1.1.1492875941.1646085237; G_ENABLED_IDPS=google; _ga_QFTZSXX3LJ=GS1.1.1647381073.16.1.1647436492.0"
cookies_dic = {"Cookie" : cookies_string}
print(f'Cookies from a common post request {cookies_dic}')

body = 'busqueda%5Btipo_viaje%5D=1&busqueda%5Borigen%5D=481&busqueda%5Bdestino%5D=255&busqueda%5Bfecha_ida%5D=28%2F04%2F2022&busqueda%5Bfecha_vuelta%5D=&busqueda%5Bcantidad_pasajeros%5D%5Badulto%5D=1&busqueda%5Bcantidad_pasajeros%5D%5Bjubilado%5D=0&busqueda%5Bcantidad_pasajeros%5D%5Bdiscapacitado%5D=0&busqueda%5Bcantidad_pasajeros%5D%5Bmenor%5D=0&busqueda%5Bcantidad_pasajeros%5D%5Bbebe%5D=0'

r = session.post(calendar_url, data=body)
tree = html.fromstring(r.content)
dias = tree.xpath('//span[@class="dia_numero"]/text()')
dias_no_disponible = tree.xpath('//span[@class="dia_numero_no_disponible"]/text()')

print('hola')