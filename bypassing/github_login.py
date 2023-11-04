import requests
from lxml import html


headers = {
  "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
}


login_from_url = 'https://github.com/login' # esta es para sacar el token

# esta clase nos mantiene la sesion
session = requests.Session()

# hacemos los requerimientos a traves de la sesion
login_form_res = session.get(login_from_url, headers=headers)

# obtenemos el token actualizado
parser = html.fromstring(login_form_res.text)
token_especial = parser.xpath('//input[@name="authenticity_token"]/@value')


login_url = 'https://github.com/session'
# esto sale de los names de los inputs
login_data = {
  "login": "joni28492@gmail.com",
  "password": open('./password.txt').readline().strip(),
  "commit": "Sign in",
  # este authenticity_token sale tambien de un input, estos tokens que se mandan son diferentes en cada pagina
  "authenticity_token": token_especial
}


session.post(
  login_url,
  data=login_data,
  headers=headers,
)

# ahora que ya hemos iniciado sesion
data_url = "https://github.com/Joni28492?tab=repositories"
#iniciamos sesion a traves de la session
respuesta = session.get(
  data_url, headers=headers
)

parser = html.fromstring(respuesta.text)

repositorios = parser.xpath('//h3[@class="wb-break-all"]/a/text()')

for repositorio in repositorios:
  print(repositorio)


