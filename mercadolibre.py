from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
# from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader



"""
https://listado.mercadolibre.com.ec/animales-mascotas/perros
PAGINACION
https://listado.mercadolibre.com.ec/animales-mascotas/perros_Desde_51_NoIndex_True
https://listado.mercadolibre.com.ec/animales-mascotas/perros_Desde_101_NoIndex_True
https://listado.mercadolibre.com.ec/animales-mascotas/perros_Desde_151_NoIndex_True

PRODUCTOS
https://articulo.mercadolibre.com.ec/MEC-520462963-cocker-spaniel-americano-260-cada-uno-_JM#position=53&search_layout=stack&type=item&tracking_id=22cd8644-6ffa-4d21-9a7a-91cfffe5caba
https://articulo.mercadolibre.com.ec/MEC-528333520-en-140-cada-perrito-french-poodle-mini-toy-_JM#position=54&search_layout=stack&type=item&tracking_id=22cd8644-6ffa-4d21-9a7a-91cfffe5caba
https://articulo.mercadolibre.com.ec/MEC-551294306-cachorros-pequines-minitoy-en250-_JM#position=52&search_layout=stack&type=item&tracking_id=22cd8644-6ffa-4d21-9a7a-91cfffe5caba
 
 
scrapy runspider .\mercadolibre.py  -o mercadolibre.csv -t csv

"""


class Articulo(Item):
    titulo = Field()
    precio = Field()
    descripcion = Field()

class MercadoLibreCrawler(CrawlSpider):
    name = "mercadolibre"
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "CLOSESPIDER_PAGECOUNT": 20 #num max de paginas a visitar y para, OJO a los baneos
    }

    download_delay = 1
    # dominios permitidos
    allowed_domains = ["listado.mercadolibre.com.ec", 'articulo.mercadolibre.com.ec']
    start_urls = ["https://listado.mercadolibre.com.ec/animales-mascotas/perros"]


    rules = (
        # paginacion, estas no tienen callback no queremos extraer datos
        Rule(
            LinkExtractor(
                allow=r'/perros_Desde_'
            ), follow=True
        ),
        # detalle de los productos
        Rule(
            LinkExtractor(
                allow=r'/MEC-'
            ), follow=True, callback='parse_items'
        )



    )

    def limpiar_texto(self, texto=''):

        return (texto.replace('\n',' ')
                .replace('\r',' ')
                .replace('\t',' ')
                .replace(',', ';')
                .replace('*', '')
                .replace('-', '')
                .strip())


    def parse_items(self, response):

        item = ItemLoader(Articulo(), response ) # esta vez lo hacemos sin el Selector
        item.add_xpath('titulo', '//h1/text()', MapCompose(self.limpiar_texto))
        item.add_xpath('descripcion', '//div[@id="description"]//p/text()', MapCompose(self.limpiar_texto))
        item.add_xpath('precio', '//span[@class="andes-visually-hidden"]/text()', MapCompose(self.limpiar_texto))


        yield item.load_item()
