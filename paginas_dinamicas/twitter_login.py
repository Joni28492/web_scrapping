from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

"""
https://twitter.com/i/flow/login

"""


opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")

driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options=opts)
driver.get('https://twitter.com/login')

# setteamos el usuario y password
user = "monkeylimmit"
password = open('password.txt').readline().strip()

# introducimos el input de usuario, OJO el Xpath esta en una tupla
input_user = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//input[@type='text']")),
)
#rellenamos el input
input_user.send_keys(user)

# boton para continuar al password
next_button = driver.find_element(By.XPATH, '//div[@class="css-901oao r-1awozwy r-6koalj r-18u37iz r-16y2uox r-37j5jr r-a023e6 r-b88u0q r-1777fci r-rjixqe r-bcqeeo r-q4m81j r-qvutc0"]')
next_button.click()

# input de password y password
input_pass = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//input[@type="password"]'))
)
input_pass.send_keys(password)

login_button = driver.find_element(By.XPATH, '//div[@data-testid="LoginForm_Login_Button"]')
login_button.click()

# Espero a los tweets
tweets = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@data-testid="tweetText"]')))

# Imprimo el texto de los tweets
for tweet in tweets:
    print(tweet.text)
