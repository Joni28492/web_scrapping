import requests
import json
from  lxml import html

"""
DEPRECATED
AVISO cambio de funcionalidad de la pagina, ahora las tallas ya no estan en un desplegable con js
el codigo es a modo de ejemplo, no fucniona actualmente

"""

headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
}


url = "https://footdistrict.com/adidas-ultra-boost-ltd-af5836.html"

resp = requests.get(url, headers=headers)
parser = html.fromstring(resp.text)

datos = parser.xpath("//script[contains(@text(), 'spConfig' )]")

texto_script = datos[0].text_content()

inicio = texto_script.find("(") + 1
final =  texto_script.find(")")

objeto = texto_script[inicio:final]
objeto = json.loads(objeto)


tallas = objeto["attributes"]["134"]["options"]


for talla in tallas:
    if "No disponible" not in talla["label"]:
        print(talla["label"])