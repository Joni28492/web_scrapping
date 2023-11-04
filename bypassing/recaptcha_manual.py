from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

"""
http://google.com/recaptcha/api2/demo

al usar navegador automatizado va a ser mucho mas largo y mas complejo
"""


opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36")

driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options=opts)

url = 'http://google.com/recaptcha/api2/demo'
driver.get(url)

try:
    # para cambiar al contexto del iframe del captcha
    driver.switch_to.frame(driver.find_element(By.XPATH, '//iframe'))

    captcha = driver.find_element(By.XPATH, '//div[@class="recaptcha-checkbox-border"]')
    captcha.click()
    # aqui paramaos nuestro codigo, para introducirlo manualmente
    input() # para hasta que le damos al enter en la terminal

    #salimos del iframe
    driver.switch_to.default_content()
    submit = driver.find_element(By.XPATH, '//input[@id="recaptcha-demo-submit"]')
    submit.click()

except Exception as e:
    print(e)

# aqui ya estaremos en la siguiente pagina
contenido = driver.find_element(By.CLASS_NAME, 'recaptcha-success')
print(contenido.text)