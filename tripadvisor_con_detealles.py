from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess

class Hotel(Item):
    nombre = Field()
    score = Field()
    descripcion = Field()
    amenities = Field()


class TripAdvisor(CrawlSpider):
    name = 'hotelestripadvisor'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        #definimos el orden de las columnas
        'FEED_EXPORT_FIELDS':  [ 'nombre', 'score', 'amenities', 'descripcion' ],
        # controlar concurrencia, cuantas urls visitamos al mismo tiempo, por defecto son 16
        'CONCURRENT_REQUESTS': 1 # va a ser mas lento
    }

    start_urls = ['https://www.tripadvisor.com/Hotels-g303845-Guayaquil_Guayas_Province-Hotels.html']

    # Va ser un rango entre 0.5 * download_delay y 1.5 * download_delay, NO son 2 segundos
    download_delay = 2


    rules = (
        Rule(
            LinkExtractor(
                allow=r'/Hotel_Review-'
            ), follow=True,
            callback="parse_hotel"),
    )

    # parsear url semilla
    def parse_start_url(self, response):
        sel = Selector(response)
        hoteles = sel.xpath('.//div[@data-ttpn="Hotels_MainList"]')
        print("Numero de resultados ", len(hoteles))



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


        item.add_xpath('descripcion', '//div[@class="ssr-init-26f"]//div[@class="fIrGe _T"]//text()')
        item.add_xpath('amenities','//div[contains(@data-test-target, "amenity_text")]/text()')
        yield item.load_item()

# EJECUCION
process = CrawlerProcess({ #damos formato
    'FEED_FORMAT':'csv',
    'FEED_URI': 'datos_de_salida.csv'
})

# Spider que usaremos
process.crawl(TripAdvisor)
process.start()
