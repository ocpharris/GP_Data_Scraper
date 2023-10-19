import scrapy
from GPscraper.items import GpItem

class GpspiderSpider(scrapy.Spider):
    name = "GPspider"
    allowed_domains = ["www.nhs.uk"]
    start_urls = ['https://www.nhs.uk/service-search/find-a-gp/results/SW1V2LE?Location=SW1V2LE&Latitude=&Longitude=']
   

    def parse(self, response):

        gps =  response.css('li.results__item') #list of gps
        
        

        for gp in gps:
            gp_item = GpItem()
            relative_url = gp.css('div h2 a ::attr(href)').get() #define url for gp
            # gp_item['miles_away'] = gp.xpath('//span[@class="nhsuk-u-visually-hidden" and contains(text(), "is")]/following-sibling::text()').get()
            gp_item['miles_away'] = gp.css('p[id^="distance_"]::text').get()
            

            yield response.follow(relative_url, callback= self.parse_gp_page, meta={'gp_item': gp_item})



       
             
        #USE IF MORE THAN ONE PAGE
        # next_page = response.css('li.next a ::attr(href)').get()

        # # for each new page, define url and call parse to loop through each book 
        # if next_page is not None:

        #     # create next page url 
        #     # accomodates inconsistency in next_page 
        #     if 'catalogue/' in next_page:
        #         next_page_url = 'https://books.toscrape.com/' + next_page
        #     else:
        #         next_page_url = 'https://books.toscrape.com/catalogue/' + next_page

        #     # callback is whats executed once response is recieved
        #     yield response.follow(next_page_url, callback= self.parse)


    #
        
    

    def parse_gp_page(self, response):
        gp_item = response.meta['gp_item']

        gp_item['name'] = response.css('span.nhsuk-caption-xl ::text').get()
        gp_item['accepting_patients'] = response.css('#gp_accepting_patients_banner_text ::text').get()
        gp_item['phone_number'] = response.css('#contact_info_panel_phone_text ::text').get()
        gp_item['gp_website'] = response.css('a#contact_info_panel_website_link ::attr(href)').get()
        print('@@@@@@@@@@@@@@@@@@@@@@@@')
        print(gp_item['phone_number'])
        print(gp_item['gp_website'])


        # gp_item['number'] = len(gps)

        yield gp_item


