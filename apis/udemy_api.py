import requests

"""
tenemos que buscar la api en las herramientas de desarrollador
en la pestaña de network, y darle al preview, normalmente tenemos que buscar un json 
"""

headers = {
    # El encabezado de referer es importante. Sin esto, este API en especifico me respondera 403
    # este encabezado lo buscamos tambien en la pestaña de network, cabeceras de peticion
    "Referer": "https://www.udemy.com/courses/search/?p=2&q=python&src=ukw",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
}

for i in range(1, 4):
    url_api ="https://www.udemy.com/api-2.0/search-courses/?src=ukw&q=python&skip_price=true&p="+str(i)


    response = requests.get(url_api, headers=headers)

    data = response.json()

    cursos = data["courses"]

    for curso in cursos:
        print(curso["title"])
        print("num_reviews",  curso["num_reviews"])
        print("rating", curso["rating"])
        print()




