
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

"""
https://listado.mercadolibre.com.ec/repuestos-autos-camionetas-bujias

"""

opts = Options()

opts.add_argument(
    "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)

driver.get('https://listado.mercadolibre.com.ec/repuestos-autos-camionetas-bujias')


while True:
    links_productos = driver.find_elements(By.XPATH, '//a[@class="ui-search-item__group__element ui-search-link"]')
    links_de_la_pagina = []


    for tag_a in links_productos:
        links_de_la_pagina.append(tag_a.get_attribute("href"))

    for link in links_de_la_pagina:
        try:
            # vamos a la pagina del producto
            driver.get(link)
            titulo = driver.find_element(By.XPATH, '//h1[@class="ui-pdp-title"]').text
            precio = driver.find_element(By.XPATH, '//span[@class="andes-money-amount__fraction"]').text
            print(titulo)
            print(precio)
            # y ahora volveriamos a la pagina anterior
            driver.back()
        except Exception as e:
            print(e)
            driver.back()
            print("Error!!!")


    try:
        # ahora nos toca la paginacion, pero tenemos que hacer click en el btn siguiente no en los numeros
        boton_siguiente = driver.find_element(By.XPATH, '//span[text()="Siguiente"]')
        boton_siguiente.click()

    except:
        print("Boton siguiente ya no existe")
        break




