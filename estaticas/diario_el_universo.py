from typing import Any

from scrapy.http import Response
from scrapy.item import Item
from scrapy.item import Field
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess

from bs4 import BeautifulSoup
"""
scrapy runspider .\diario_el_universo.py -o video.json -t json

scrapy runspider <ruta del script> -o <Archivo_salida> -t <extension>

"""

class Noticia(Item):
    titular = Field()
    descripcion= Field()


class ElUniversoSpider(Spider):
    name = "MiSegundoSpider"
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    }

    start_urls = ["https://www.eluniverso.com/deportes/"]
    # utilizando Scrapy
    def parse(self, response):
        sel = Selector(response)
        noticias = sel.xpath("//div[starts-with(@class, 'card ')]") # no se sigue la del curso
        for noticia in noticias:
            item = ItemLoader(Noticia(), noticia)
            item.add_xpath('titular', './/h2/a/text()')
            item.add_xpath('descripcion', './/h2/following-sibling::p/text()')
            yield item.load_item()


    # utilizando beautifulsoup

    # def parse(self, response):
    #     soup = BeautifulSoup(response.text, 'html.parser')  # en el video lo hace con .body
    #     contenedor_noticias = soup.find_all('div', class_="card")
    #     for contenedor in contenedor_noticias:
    #         noticias = contenedor.find_all('div', class_="card-content", recursive=False)
    #         for noticia in noticias:
    #             # instanciamos con scrapy
    #             item = ItemLoader(Noticia(), response.body)
    #             # pero selecionamos con bs4
    #             titular = noticia.find('h2').text
    #             descripcion = noticia.find('p')
    #
    #             #validacion si no tiene texto
    #             if(descripcion != None):
    #                     descripcion = descripcion.text
    #             else:
    #                 descripcion= 'N/A'
    #
    #             item.add_value('titular', titular)
    #             item.add_value('descripcion', descripcion)
    #
    #             yield item.load_item()


# para ejecutar sin el comando largo

process = CrawlerProcess({ #damos formato
    'FEED_FORMAT':'csv',
    'FEED_URI': 'resultados.csv'
})

# Spider que usaremos
process.crawl(ElUniversoSpider)
process.start()