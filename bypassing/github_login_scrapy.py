from typing import Any

from scrapy.http import Response
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.crawler import CrawlerProcess
import scrapy


"""
Deprecated, solo ver para login con scrapy
# todo revisar
"""


class LoginSpider(Spider):
    name="GithubLogin"
    start_url = ["https://github.com/login"]


    def parse(self, response):
        # busca un formulario, y lo rellena como si fuera un humano con lo que le pasemos
        return scrapy.FormRequest.from_response(
            response,
            formdata={
                # datos del formulario a rellenar, con su correspondiente name, hay que buscarlos
                'login': 'joni28492',
                'password': open('./password.txt').readline().strip()
            },
            callback=self.after_login
        )

    def after_login(self, response):
        # aqui recibimos en el response la pagina que sale despues de hacer el login
        # pero queremos ir a otra asi que se lo tenemos que indicar
        request = scrapy.Request(
            'https://github.com/Joni28492?tab=repositories',
            callback=self.parse_repositorios
        )
        yield request

    # seguimos anidando
    def parse_repositorios(self, response):
        sel = Selector(response)
        repositorios = sel.xpath('//h3[@class="wb-break-all"]/a/text()')
        for repositorio in repositorios:
            print(repositorio.get())

process = CrawlerProcess()
process.crawl(LoginSpider)
process.start()