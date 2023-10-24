from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
# from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader


"""

otra alternativa
https://www.eneba.com/es/marketplace/playstation-4-juegos?page=1&platforms[]=playstation-4&regions[]=global&regions[]=europe&regions[]=emea&regions[]=spain

https://latam.ign.com/se/?type=video&q=a&order_by=-date

En este caso tenemos varias dimensiones, la pestaña de las categorias de las paginas
y luego en cada una su paginacion correspondiente, y en cada item con propiedaes diferentes

PESTAÑAS
articulo
https://latam.ign.com/se/?type=news&q=a&order_by=-date
review
https://latam.ign.com/se/?type=review&q=a&order_by=-date
video
https://latam.ign.com/se/?type=video&q=a&order_by=-date

PAGINACION
pag 2
https://latam.ign.com/se/?type=news&q=a&order_by=-date&page=2
pag 3
https://latam.ign.com/se/?type=news&q=a&order_by=-date&page=3


ITEMS
articulo, titulo y texto contenido
https://latam.ign.com/batman-a-telltale-game-series/65748/news/batman-el-juego-de-telltale-games-recibiria-dlc
review, titulo del review y calificacion final
https://latam.ign.com/the-walking-dead-season-3-episode-2/34364/review/review-the-walking-dead-the-telltale-series-a-new-frontier-episode-2-ties-that-bind-part-2
video, titulo del video y la fecha de publicacion
https://latam.ign.com/the-walking-dead-season-3-episode-1/43684/trailer/trailer-de-the-walking-dead-the-telltale-series-collection 

"""

class Articulo(Item):
    titulo = Field()
    contenido = Field()

class Review(Item):
    titulo = Field()
    calificacion = Field()

class Video(Item):
    titulo = Field()
    fecha_de_publicacion = Field()


class IGNCrawler(CrawlSpider):
    name = 'ign'
    custom_settings = {
      'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
      'CLOSESPIDER_PAGECOUNT': 20
    }

    allowed_domains = ['latam.ign.com']
    start_urls = ['https://latam.ign.com/se/?model=article&q=ps5']

    download_delay = 1

    rules = (
        # horizontalidad por tipo de informacion (PESTAÑAS)
        Rule(
            LinkExtractor(
                allow=r'type='
            ), follow=True
        ),
        # horizontalidad por paginacion
        Rule(
            LinkExtractor(
                allow=r'&page=\d+' # expresion regular
            ), follow=True
        ),
        # REVIEWS
        Rule(
            LinkExtractor(
                allow=r'/review/'
            ), follow=True, callback='parse_reviews' ),
        # VIDEOS
        Rule(
            LinkExtractor(
                allow=r'/video/'
            ), follow=True, callback='parse_video' ),
        # NEWS
        Rule(
            LinkExtractor(
                allow=r'/news/'
            ), follow=True, callback='parse_news' ),
    )


    def remove_comillas(self, text):
        if(type(text) == 'str'):
            return text.replace('\"', '=|=')
        else:
            return "".join(text).replace('\"', '=|=')

    def parse_news(self, response):
        item = ItemLoader(Articulo(), response)
        item.add_xpath('titulo','//h1/text()')
        item.add_xpath('contenido', '//div[@id="id_text"]//*/text()')

        yield item.load_item()


    def parse_reviews(self,response):
        item = ItemLoader(Review(), response)
        item.add_xpath('titulo', '//h1/text()')
        item.add_xpath('calificacion', "//div[@class='review']//div/text()")
        #todo arreglar calificacion
        yield item.load_item()


    def parse_video(self, response):
        item = ItemLoader(Video(), response)
        item.add_xpath('titulo', '//h1/text()')
        item.add_xpath('fecha_de_publicacion', '//span[@class="publish-date"]/text()', MapCompose(self.remove_comillas()))

        yield item.load_item()
