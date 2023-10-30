# -*- coding: utf-8 -*-
"""
OBJETIVO:
    - Extraer resenas escritas por usuarios en Google Places.
    - Aprender a cargar informacion haciendo scrolling.
    - Aprender a manejar varios tabs abiertos al mismo tiempo en Selenium.
CREADO POR: LEONARDO KUFFO
ULTIMA VEZ EDITADO: 12 SEPTIEMBRE 2023
"""
import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager  # pip install webdriver-manager

# User agent
opts = Options()
opts.add_argument(
    "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")


# Funcion para obtener el Script de Scrolling dependiendo de cuantos scrollings ya he hecho
# Es un approach mas inteligente que el utilizado en el video. En donde, mientras mas escrolls llevo dando, mas pixeles voy bajando.
# Simplemente remplazo el 20000 en la cadena del script, por un numero que dependa de la iteracion en que me encuentro actualmente
def getScrollingScript(iteration):
    # Script de scrolling es un script de javascript. Le hago scroll a un contenedor que contenta ciertas clases
    # Estas clases dependen de mi extraccion. Existen otras maneras de hacer scrolling que veremos en el NIVEL EXTRA.
    scrollingScript = """ 
      document.getElementsByClassName('m6QErb DxyBCb kA9KIf dS8AEf')[0].scroll(0, 20000)
    """
    return scrollingScript.replace('20000', str(20000 * (iteration + 1)))


# Selenium 4.10
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
driver.get(
    'https://www.google.com/maps/place/Restaurante+Amazonico/@40.423706,-3.6872655,17z/data=!4m7!3m6!1s0xd422899dc90366b:0xce28a1dc0f39911d!8m2!3d40.423706!4d-3.6850768!9m1!1b1')

# A veces google places necesita una espera adicional
sleep(random.uniform(4.0, 6.0))

# Debemos darle click al boton de disclaimer de cookies que no interrumpa nuestras acciones
# try:  # Esto ya no funciona, darle manualmente
#     disclaimer = driver.find_element(By.XPATH, '//span[text()="Accept all"]')
#     disclaimer.click()  # lo obtenemos y le damos click
# except Exception as e:
#     print(e)
#     None



# Logica de Scrolling
SCROLLS = 0
while (SCROLLS != 2):  # Decido que voy a hacer 3 scrollings
    driver.execute_script(getScrollingScript(SCROLLS))  # Ejecuto el script para hacer scrolling del contenedor
    sleep(random.uniform(1, 2))  # Entre cada scrolling espero un tiempo
    SCROLLS += 1

# Una vez que ha terminado el scrollings...
# Obtengo la Lista de reviews del restaurante
restaurantsReviews = driver.find_elements(By.XPATH, '//div[@data-review-id and not(@aria-label)]')

# Por cada review...
for review in restaurantsReviews:
    sleep(1)
    # Obtengo el contenedor del nombre de usuario
    userLink = review.find_element(By.XPATH, ".//div[contains(@class, 'WNx')]//button")

    try:

        userLink.click()  # Damos click para abrir su perfil. Esto se abre en un nuevo tab.

        # Movemos el contexto del driver al tab en la segunda posicion.  no hacemos esto, no podremos acceder a los elementos del nuevo tab.
        driver.switch_to.window(driver.window_handles[1])


        #  Scrolling de las opiniones
        userReviews = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@data-review-id and not(@aria-label)]'))
        )
        USER_SCROLLS = 0

        # hacemos scroll de las reviews
        while (USER_SCROLLS != 2):
            driver.execute_script(getScrollingScript(USER_SCROLLS))
            sleep(random.uniform(4, 5))
            USER_SCROLLS += 1

        # Obtenemos todos los reviews visibles del usuario
        userReviews = driver.find_elements(By.XPATH, '//div[@data-review-id and not(@aria-label)]')


        for userReview in userReviews:


            reviewRating = userReview.find_element(By.XPATH, './/span[@class="kvMYJc"]').get_attribute('aria-label')
            userParsedRating = float(''.join(filter(str.isdigit or str.isspace,reviewRating)))
            # Codigo para solamente quedarme con los digitos de una cadena. En la clase nos quedamos con toda la cadena.
            reviewText = ""
            try:
                reviewText = userReview.find_element(By.XPATH, './/span[@class="wiI7pd"]').text
            except:
                print('Review sin texto')

            print(userParsedRating)
            print(reviewText)

        # Cerramos el tab
        driver.close()
        # volvemos al primer tab
        driver.switch_to.window(driver.window_handles[0])

    # Si ocurre algun error, cierro el tab abierto, y reinicio el contexto al tab original
    except Exception as e:
        print(e)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])