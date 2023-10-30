import scrapy
from GPscraper.items import GpItem

# to run in command line 'scrapy crawl GPspider -a postcode=ex55ls -o test.csv'


class GpspiderSpider(scrapy.Spider):
    name = "GPspider"
    allowed_domains = ["www.nhs.uk"]

    # # start_urls = ['https://www.nhs.uk/service-search/find-a-gp/results/SW1V2LE?Location=SW1V2LE&Latitude=&Longitude=']
    # postcode = 'ex55ls'
    # postcode_url = 'https://www.nhs.uk/service-search/find-a-gp/results/' + postcode 
    # # + '?Location=' + postcode + '&Latitude=&Longitude='
    # start_urls = [postcode_url]
    

    def __init__(self, postcode, *args, **kwargs):
        super(GpspiderSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f"https://www.nhs.uk/service-search/find-a-gp/results/{postcode}"]

    
    def parse(self, response):

        gps =  response.css('li.results__item') #list of gps
        
        

        for gp in gps:
            gp_item = GpItem()
            relative_url = gp.css('div h2 a ::attr(href)').get() #define url for gp
            gp_item['miles_away'] = gp.css('p[id^="distance_"]::text').get()
            

            yield response.follow(relative_url, callback= self.parse_gp_page, meta={'gp_item': gp_item})
            

    def parse_gp_page(self, response):
        gp_item = response.meta['gp_item']

        gp_item['name'] = response.css('span.nhsuk-caption-xl ::text').get()
        gp_item['accepting_patients'] = response.css('#gp_accepting_patients_banner_text ::text').get()
        gp_item['phone_number'] = response.css('#contact_info_panel_phone_text ::text').get()
        gp_item['gp_website'] = response.css('a#contact_info_panel_website_link ::attr(href)').get()

        yield gp_item


