import scrapy
import re
def cleaned_data(input_string:str):
        if input_string:
            return re.sub(r'[\\r\\n\\t@]', '',input_string).strip()

class NflSpider(scrapy.Spider):
    name="nfl"
    
    start_urls = ['https://www.nfl.com/players/active/a/']
    
    def parse(self, response):
        linked = "stats/logs/"
        link = response.css('.nfl-o-cta--link::attr(href)').getall()

        #link = response.css('.nfl-o-cta--link::attr(href)').getall()
        for url1 in link:
            url_complete = "https://www.nfl.com" + url1 + linked
            request = scrapy.Request(url=url_complete, callback=self.parse_player)

            yield request


    def parse_player(self, response):
        player_name = response.css('.nfl-c-player-header__title::text').get()

        year = response.css('select option[selected="selected"]::text').get()
        
        for season in response.css("div.d3-o-table--horizontal-scroll > table"):
            for week in season.css("tbody > tr"):
                item = {
                "Player Name" : cleaned_data(player_name),
                "Year" : year,
                'Week Number': cleaned_data(week.css('td:nth-child(1)::text').get()),
                "Date Played": week.css('td:nth-child(2)::text').get(),
                "Opponent": cleaned_data(week.css('td:nth-child(3)::text').get()),
                "Solos" : cleaned_data(week.css('td:nth-child(4)::text').get()),
                "urls": response.url
                }
                yield item