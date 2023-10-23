import requests
from bs4 import BeautifulSoup

encabezados = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
}

url = "https://stackoverflow.com/questions/"


respuesta = requests.get(url, headers=encabezados)

# tenemos una sopa de tags, el soup seria como el parser
soup = BeautifulSoup( respuesta.text )

contenedor_de_preguntas = soup.find(id="questions")
lista_de_preguntas = contenedor_de_preguntas.find_all('div', class_="s-post-summary" )

## Forma 1
# for pregunta in lista_de_preguntas: # pregunta es el contenedor de la pregunta,un html
#     texto_pregunta = pregunta.find('h3').text
#     descripcion_pregunta = pregunta.find(class_="s-post-summary--content-excerpt").text
#     descripcion_pregunta = descripcion_pregunta.replace('\n', '').replace('\r', '').strip() # strip es como un trim()
#     print(texto_pregunta, end='')
#     print(descripcion_pregunta, end="")
#     print()

# forma 2 (por si no tenemos clase especifica)
for pregunta in lista_de_preguntas: # pregunta es el contenedor de la pregunta,un html
    elemento_texto_pregunta = pregunta.find('h3')
    texto_pregunta = elemento_texto_pregunta.text
    descripcion_pregunta = elemento_texto_pregunta.find_next_sibling('div').text

    descripcion_pregunta = descripcion_pregunta.replace('\n', '').replace('\r', '').strip() # strip es como un trim()
    print(texto_pregunta, end='')
    print(descripcion_pregunta, end="")
    print()