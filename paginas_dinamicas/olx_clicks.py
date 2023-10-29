import random
from time import sleep
from selenium.webdriver.common.by import By
from selenium import webdriver # pip install selenium
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

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
driver.get('https://www.olx.in/cars_c84')
sleep(2)
driver.refresh()   # Solucion de un bug extraño en Windows en donde los anuncios solo cargan al hacerle refresh a la página
sleep(2)    # Esperamos que cargue el boton

# hasta que no carga toda la pagina no avanza con el codigo




#daremos clic al boton 3 veces
boton = driver.find_element(By.XPATH, '//button[@data-aut-id="btnLoadMore"]')


for i in range(3):
    try:
        boton.click()
        # randomizamos tiempo de espera para humanizar
        sleep(random.uniform(8.0, 10.0))
        # buscamos de nuevo el nuevo boton de carga
        boton = driver.find_element(By.XPATH, '//button[@data-aut-id="btnLoadMore"]')
    except:
        break

# tiene que ser en este punto despues de toda la carga
autos = driver.find_elements(By.XPATH, '//li[@data-aut-id="itemBox"]')

for auto in autos:
    try:
        precio = auto.find_element(By.XPATH, './/span[@data-aut-id="itemPrice"]').text
        print (precio)
        descripcion = auto.find_element(By.XPATH, './/div[@data-aut-id="itemTitle"]').text
        print (descripcion)
    except Exception as e:
        print ('Anuncio carece de precio o descripcion')
