# import requests
from bs4 import BeautifulSoup
import cloudscraper

"""
si nos da un 403 es de no autorizado porque no pasamos el cloudflare

cloudscraper, esta montado sobre request y tiene rotacion de headers y otros 
mecanismos para hacer bypass, en esta ya no necesitariamos requests
"""

headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
}


url = 'https://www.zonaprop.com.ar/cocheras-alquiler-capital-federal.html'

# nos setea el agente con los headers y las demas conf
scraper = cloudscraper.create_scraper()
# este se usa igual que el session
# session = requests.session()
# resp = session.get(url, headers=headers)
resp = scraper.get(url)





# a partir de aqui empezamos a parsear
soup = BeautifulSoup(resp.text, features='lxml')

anuncios = soup.find_all('div', {"data-qa": "posting PROPERTY"} )

for anuncio in anuncios:
    titulo = anuncio.find('h2').text
    print(titulo)

print(resp) # si esta bien recibimos un <Response [200]>