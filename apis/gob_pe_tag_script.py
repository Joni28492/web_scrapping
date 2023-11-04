import requests
from lxml import html
import json

"""
https://www.gob.pe/busquedas?reason=sheet&sheet=1
"""

headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
}

# #con paginacione
# for i in range(1, 5):
#     url = "https://www.gob.pe/busquedas?contenido[]=normas&institucion[]=mininter&reason=sheet&sheet=" + str(i) + "&term=renuncia"

respuesta = requests.get("https://www.gob.pe/busquedas?reason=sheet&sheet=1", headers=headers)
respuesta.encoding = 'UTF-8'

parser = html.fromstring(respuesta.text)

datos = parser.xpath('//script[contains(text(), "window.initialData")]')[0].text_content()

indice_inicial = datos.find("{")
datos = datos[indice_inicial:]

objeto = json.loads(datos)

resultados = objeto["data"]["attributes"]["results"]

for resultado in resultados:
    if resultado:
        print(resultado["content"])




