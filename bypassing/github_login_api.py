import requests
import json


"""
doc
https://api.github.com/


https://api.github.com/user/repos{?type,page,per_page,sort}
son parametros opcionales
"""
headers = { # en la api no suele hacer falta header
  "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
}

endpoint = "https://api.github.com/user/repos?page=3"

usuario = "joni28492"
# este token lo tenemos que crear en nustro github y darle los permisos adecuados
token = open('./token.txt').readline().strip()


response = requests.get(endpoint, headers=headers, auth=(usuario, token))
repositorios =response.json()
for repositorio in repositorios:
  print(repositorio["name"])


# print(json.dumps(repositorios, indent=4)) # da una identacion de 4 espacios



