import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


"""
https://www.google.com/maps/place/Restaurante+Amazonico/@40.423706,-
3.6872655,17z/data=!4m7!3m6!1s0xd422899dc90366b:0xce28a1dc0f39911d!8m2!
3d40.423706!4d-3.6850768!9m1!1b1

"""
# codigo js que usaremos, tenemos que identificar el contenedor que tiene el scroll, y se hace hasta el pixel 20000
scrollingScript = """ 
     document.getElementsByClassName('m6QErb DxyBCb kA9KIf dS8AEf')[0].scroll(0, 20000)
   """

opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
driver.get("https://www.google.com/maps/place/Restaurante+Amazonico/@40.423706,-3.6872655,17z/data=!4m7!3m6!1s0xd422899dc90366b:0xce28a1dc0f39911d!8m2!3d40.423706!4d-3.6850768!9m1!1b1")

sleep(random.uniform(1.0, 2.0))

# Debemos darle click al boton de disclaimer de cookies que no interrumpa nuestras acciones
try:
  disclaimer = driver.find_element(By.XPATH, '//button[@id="W0wltc"]')
  disclaimer.click() # lo obtenemos y le damos click
except Exception as e:
  print (e)
  None

sleep(random.uniform(1.0, 2.0))


SCROLLS = 0 # funciona como un contador

while(SCROLLS != 2):
    driver.execute_script(scrollingScript) # nos permite ejecutar codigo de js
    sleep(random.uniform(1,2))
    SCROLLS += 1


reviews_restaurante = driver.find_elements(By.XPATH, '//div[@class="jftiEf fontBodyMedium"]')

for review in reviews_restaurante:
    user_link = review.find_element(By.XPATH, './/button[@class="al6Kxe"]')

    try:
        user_link.click()
        # cambiamos de pestaña, numeradas como las listas
        driver.switch_to.window(driver.window_handles[1])

        # pestaña de reseñas en el sidebar
        boton_opiniones = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(By.XPATH, '//button[@class="hh2c6 G7m0Af"]')
        )

        boton_opiniones.click()
        #esperamos a que cargue el contenedor del scroll
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(By.XPATH, '//div[@class="m6QErb DxyBCb kA9KIf dS8AEf "]')
        )

        USER_SCROLLS = 0
        while(USER_SCROLLS !=3):
            driver.execute_script(scrollingScript) # es la misma clase en los 2 scrolls, sino lo cambiariamos
            sleep(random.uniform(5,6))
            USER_SCROLLS+=1
        userReviews = driver.find_elements(By.XPATH, '//div[@class="jftiEf fontBodyMedium t2Acle FwTFEc azD0p"]')

        for userReview in userReviews:
            texto = userReview.find_element(By.XPATH, '//span[@class="wiI7pd"]').text
            rating = userReview.find_element(By.XPATH, '//span[@class="kvMYJc"]').get_attribute("aria-label")
            print(texto)
            print(rating)
        driver.close() # cerramos la pestaña
        driver.switch_to.window(driver.window_handles[0]) # volvemos a la inicial
    except Exception as e:
        print(e)
        driver.close()
        # si estamos en otra pestaña volvemos a la inicial
        driver.switch_to.window(driver.window_handles[0])

