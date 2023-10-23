from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader


class Hotel(Item):
    nombre = Field()
    score = Field() # El precio ahora carga dinamicamente. Por eso ahora obtenemos el score del hotel
    descripcion = Field()
    amenities = Field()

# CLASE CORE - Al querer hacer extraccion de multiples paginas, heredamos de CrawlSpider
class TripAdvisor(CrawlSpider):
    name = 'hotelestripadvisor'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    }


    # Url semilla a la cual se hara el primer requerimiento
    start_urls = ['https://www.tripadvisor.com/Hotels-g303845-Guayaquil_Guayas_Province-Hotels.html']

    # Tiempo de espera entre cada requerimiento. Nos ayuda a proteger nuestra IP.
    download_delay = 2


    rules = (
        Rule( # Regla de movimiento VERTICAL hacia el detalle de los hoteles
            LinkExtractor(
                allow=r'/Hotel_Review-' # hace referencia a la url, seria como una regex
            ), follow=True, # le decimos que si le permitimos ir al link con ese patron
            callback="parse_hotel"), # es la funcion parse que creamos nosotros con el nombre que le daremos
    )

    def quitarSimboloDolar(self, texto):
        nuevoTexto = texto.replace("$", '').replace("\n",'').replace("\r","").replace("\t","")
        return nuevoTexto

    # Callback de la regla
    def parse_hotel(self, response):
        sel = Selector(response)

        item = ItemLoader(Hotel(), sel)
        item.add_xpath('nombre', '//h1[@id="HEADING"]/text()')
        item.add_xpath('score',
                       './/div[@class="grdwI P"]/span/text()',
                       MapCompose(self.quitarSimboloDolar))
        # mapCompose es para prepocesar la info, con una funcion
        # no nos hace falta los () como en JS
        # es preferible evitar clases raras porque cambian con el tiempo

        item.add_xpath('descripcion', '//div[@class="ssr-init-26f"]//div[@class="fIrGe _T"]//text()')
        item.add_xpath('amenities','//div[contains(@data-test-target, "amenity_text")]/text()')
        yield item.load_item()

# EJECUCION
# scrapy runspider 1_tripadvisor.py -o tripadvisor.csv
