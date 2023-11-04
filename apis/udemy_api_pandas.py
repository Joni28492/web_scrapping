import requests
import pandas as pd

"""
en este caso usaremos pandas 
"""

headers = {
    # El encabezado de referer es importante. Sin esto, este API en especifico me respondera 403
    # este encabezado lo buscamos tambien en la pestaña de network, cabeceras de peticion
    "Referer": "https://www.udemy.com/courses/search/?p=2&q=python&src=ukw",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
}

# cursos_totales = [# EJEMPLO ESTRUCTURA
#     {
#         "titulo":"titulo1"
#     },
#     {
#         "titulo":"titulo2"
#     },
# ]

cursos_totales = []

for i in range(1, 4):
    url_api = "https://www.udemy.com/api-2.0/search-courses/?src=ukw&q=python&skip_price=true&p=" + str(i)

    response = requests.get(url_api, headers=headers)

    data = response.json()

    cursos = data["courses"]

    for curso in cursos:
        cursos_totales.append({
            "title": curso["title"],
            "num_reviews": curso["num_reviews"],
            "rating": curso["rating"]
        })

df = pd.DataFrame(cursos_totales)

print(df)
df.to_csv("cursos_udemy.csv")
