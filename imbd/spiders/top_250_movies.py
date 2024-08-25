import scrapy
from scrapy.http import Response


class Top250MoviesSpider(scrapy.Spider):
    name = "top_250_movies"
    allowed_domains = ["www.imdb.com"]
    start_urls = ["https://www.imdb.com/chart/top/?ref_=nv_mv_250"]

    def parse(self, response: Response, **kwargs):
        pass
