from scrapy.item import Item
from scrapy.item import Field
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader

"""
para correr este archivo hay que usar el siguiente comando

scrapy runspider .\stackoverflow_scrapy.py -o video.csv -t csv
scrapy runspider <ruta del script> -o <Archivo_salida> -t <extension>

de primeras los datos van a venir sucios

"""

class Pregunta(Item):
    """
    esta clase es lo que queremos extraer, y en funcion de
    eso tiene unas props u otras
    """
    id=Field()
    pregunta = Field()
   # descripcion = Field()

class StackoverflosSpider(Spider):
    name = "MiPrimerSpider"
    # definimos el encabezado user-agent
    custom_settings = {
        "USER-AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    }

    start_urls = ["https://stackoverflow.com/questions/"] # aqui podrian ir varias

    def parse(self, response): # hace ya la peticion a la url
        sel = Selector(response)
        # admite selectores Xpath y CSS
        preguntas = sel.xpath('//div[@id="questions"]//div[@class="s-post-summary--content"]')
        i=0
        for pregunta in preguntas:
            item = ItemLoader(Pregunta(), pregunta ) # recibe la clase Pregunta y la seleccion que hicimos
            item.add_xpath('pregunta', './/h3/a/text()') # prop, y xpath a partir de lo ya seleccionado
            #item.add_xpath('descripcion', './/div[@class="s-post-summary--content-excerpt"]/text()')
            item.add_value("id",i) #llenar con un valor
            i += 1
            # todo ver los archivos antes de guardarlos
            yield item.load_item() #yield es como un return, lo manda a un archivo

