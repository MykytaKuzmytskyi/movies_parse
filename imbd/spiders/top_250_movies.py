import time

import scrapy
from scrapy.http import Response, HtmlResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


class Top250MoviesSpider(scrapy.Spider):
    name = "top_250_movies"
    allowed_domains = ["www.imdb.com"]
    start_urls = ["https://www.imdb.com/chart/top/?ref_=nv_mv_250"]

    def __init__(self, *args, **kwargs):
        super(Top250MoviesSpider, self).__init__(*args, **kwargs)
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(service=Service(), options=chrome_options)

        self.movies_data = []
        self.actors_data = []

    def parse(self, response: Response, **kwargs):
        self.driver.get(response.url)

        wait_time = 0
        while True:
            html = self.driver.page_source
            response = HtmlResponse(url=self.driver.current_url, body=html, encoding='utf-8')
            items = response.css("li.ipc-metadata-list-summary-item")
            if len(items) >= 250:
                self.driver.quit()
                break
            if wait_time >= 30:
                self.driver.quit()
                break
            time.sleep(3)
            wait_time += 3

        if len(items) < 250:
            self.logger.warning("Не удалось найти 250 элементов. Найдено: %d", len(items))

        for movie in items:
            full_title = movie.css("h3.ipc-title__text::text").get().split('. ')
            number = full_title[0]
            title = full_title[-1]
            detail_url = response.urljoin(movie.css('a').attrib['href'])
            rating = movie.css("span.ipc-rating-star--rating::text").get()

            yield scrapy.Request(url=detail_url, callback=self.parse_movie_details,
                                 meta={"number": number, 'title': title, 'rating': rating})

    def parse_movie_details(self, response):
        number = response.meta['number']
        title = response.meta['title']
        rating = response.meta['rating']
        cast_url = response.urljoin(
            response.css("a.ipc-metadata-list-item__icon-link[aria-label='See full cast and crew']").attrib['href'])

        yield scrapy.Request(url=cast_url, callback=self.parse_cast,
                             meta={"number": number, 'title': title, 'rating': rating, 'detail_url': response.url})

    def parse_cast(self, response):
        number = response.meta['number']
        title = response.meta['title']
        rating = response.meta['rating']
        detail_url = response.meta['detail_url']

        cast = response.css("table.cast_list tr")[1:]
        actor_names = []

        for row in cast:
            marker = row.css('td[colspan="4"].castlist_label')
            if marker and 'Rest of cast listed alphabetically:' in row.get():
                break

            name_tag = row.css("td:nth-child(2) a::text").get()
            if name_tag:
                actor_names.append(name_tag.strip())

        self.movies_data.append({
            'number': number,
            'title': title,
            'url': detail_url,
            'rating': rating,
            'cast': ", ".join(actor_names)
        })

        for actor in actor_names:
            self.actors_data.append({
                'actor': actor,
                'movie_title': title,
                'rating': rating
            })
