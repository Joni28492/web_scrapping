from scrapy.item import Field, Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup


"""
en este caso en la paginacion no tenemos el href como tal pero tenemos el numero como texto
la solucion para las paginas seria usar varias url semilla


https://urbania.pe/buscar/proyectos-propiedades?page=2
"""

class Departamento(Item):
    nombre = Field()
    direccion = Field()


class Urbaniape(CrawlSpider):
    nombre="Departamentos"
    name = "Departamentos"

    # si nos sale un 403 cambiar el user agent, vpns y demas cosas, crawlear fue vendida y ahora se usa otra plataforma seguir viendo el video
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'CLOSESPIDER_ITEMCOUNT': 100,
        # configuracion para crawlera
        # para no usar nuestra maquina y usar una de la plataforma
        'DOWNLOADER_MIDDLEWARES': {'scrapy_crawlera.CrawleraMiddleware': 610},
        'CRAWLERA_ENABLED': True,
        'CRAWLERA_APIKEY': 'INGRESA_TU_API_KEY'
    }

    start_urls = [
        'https://urbania.pe/buscar/proyectos-propiedades?page=1',
        'https://urbania.pe/buscar/proyectos-propiedades?page=2',
        'https://urbania.pe/buscar/proyectos-propiedades?page=3',
        'https://urbania.pe/buscar/proyectos-propiedades?page=4',
        'https://urbania.pe/buscar/proyectos-propiedades?page=5',
    ]

    allowed_domains = ['urbania.pe']

    download_delay = 1 # si usamos crawlera no debemos utilizarlo

    rules = (
        Rule(
            LinkExtractor(
                allow=r'/proyecto/'
            ), follow=True, callback="parse_depa"
        ),
    )


    def parse_depa(self, response):
        sel = Selector(response)
        item = ItemLoader(Departamento(), sel)

        item.add_xpath('nombre', '//h1[@class="title"]/text()')
        item.add_xpath('direccion', '//p[@class="subtitle"]/text()')

        yield item.load_item()