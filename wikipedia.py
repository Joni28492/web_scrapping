import requests
from lxml import html

# en la cabecera "user-agent" nos dice el navegador y el sistema operativo
# hay que sobreescribirla para que no detecten el scrapping
encabezados = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
}


url = "https://web.archive.org/web/20230730045736/https://www.wikipedia.org/" # utilizamos esta para que se parezca a la del curso

respuesta = requests.get(url, headers=encabezados)
parser = html.fromstring(respuesta.text)


# Ejemplo idioma individual
# espanol = parser.get_element_by_id("js-link-box-es") # nos sale una clase
# print(espanol.text_content())

# espanol = parser.xpath("//a[@id='js-link-box-es']/strong/text()")
# print(espanol)

# Todos los idiomas con xpath
idiomas = parser.xpath("//div[contains(@class, 'central-featured-lang')]//strong/text()")
for idioma in idiomas:
    print(idioma)

# ahora con find class
# idiomas = parser.find_class("central-featured-lang")
# for idioma in idiomas:
#     print(idioma.text_content())
