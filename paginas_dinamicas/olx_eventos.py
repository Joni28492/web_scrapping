
from time import sleep
from selenium.webdriver.common.by import By
from selenium import webdriver # pip install selenium
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

"""
en este caso la pagina es dinamica, y para cargar los demas vehiculos hay que darle a un boton
https://www.olx.in/cars_c84

ejecutar con comando python, no usar el run de pycharm

"""

# Asi podemos setear el user-agent en selenium
opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")


# Instancio el driver de selenium que va a controlar el navegador
# ahora no hace falta el .exe ni necesitamos instlar nada
driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options=opts)

# elegiumos la pagina
driver.get('https://www.olx.in/')
driver.refresh()   # Solucion de un bug extraño en Windows en donde los anuncios solo cargan al hacerle refresh a la página



for i in range(3):
    sleep(1)
    try:
        # driver y el tiempo max de espera
        # esperar que el boton se cargue antes de dar clic
        boton = WebDriverWait(driver, 10).until(
            # esperamos a q el elemento exista
            EC.presence_of_element_located((By.XPATH, '//button[@data-aut-id="btnLoadMore"]'))
        )

        boton.click()
        nAnuncios = 20 + ((i + 1) * 20)
        # esperar que los skeleton se carguen
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(By.XPATH, '//li[@data-aut-id="itemBox"]//span[@data-aut-id="itemPrice"]')
        ) # esta linea es solo de bloque, no nos hace falta sacar la variable

    except:
        break

# tiene que ser en este punto despues de toda la carga
anuncios = driver.find_elements(By.XPATH, '//li[@data-aut-id="itemBox"]')

for anuncio in anuncios:
    # Por cada anuncio hallo el precio, que en esta pagina principal, rara vez suele no estar, por eso hacemos esta validacion.
    try:
        precio = anuncio.find_element('xpath', './/span[@data-aut-id="itemPrice"]').text
    except:
        precio = 'NO DISPONIBLE'
    print(precio)
    # Por cada anuncio hallo la descripcion
    try:
        descripcion = anuncio.find_element('xpath', './/span[@data-aut-id="itemTitle"]').text
    except:
        descripcion = 'NO DISPONIBLE'
    print(descripcion)
