
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy import Request

class Dummy(Item):
  titulo = Field()
  titulo_iframe = Field()


class W3SCrawler(Spider):
  name = 'w3s'
  custom_settings = {
    'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'REDIRECT_ENABLED': True
  }

  allowed_domains = ['w3schools.com']
  start_urls = ['https://www.w3schools.com/html/html_iframe.asp']
  download_delay = 1

  # en esta caso parseamos directamente
  def parse(self, response):
    sel = Selector(response)

    # Extraigo la informacion que me interesa de la pagina que tiene el iframe
    titulo = sel.xpath('//div[@id="main"]//h1/span/text()').get()
    # almacenamos las propiedades para poder retornarla dentro del parse del iframe
    previous_data = {
      'titulo': titulo
    }


    iframe_url = sel.xpath('//div[@id="main"]//iframe[@width="99%"]/@src').get()
    # concatenamos la url base con la del iframe que sale en el src que esta incompleta
    iframe_url = "https://www.w3schools.com/html/" + iframe_url

    # Hago un request forzoso a la URL del iframe
    yield Request(
      iframe_url, # url del iframe a la cual hare el requerimiento
      callback = self.parse_iframe, # funcion dentro de la clase que va a procesar el iframe
      meta=previous_data # atributos de la pagina padre
    )

  def parse_iframe(self, response):

    item = ItemLoader(Dummy(), response)
    item.add_xpath('titulo_iframe', '//div[@id="main"]//h1/span/text()')
    item.add_value('titulo', response.meta.get('titulo'))

    yield item.load_item()

# EJECUCION
# scrapy runspider w3s.py -o w3s.json -t json