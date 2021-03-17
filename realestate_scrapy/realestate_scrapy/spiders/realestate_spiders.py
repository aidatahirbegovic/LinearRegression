import scrapy
from scrapy.loader import ItemLoader
from scrapy.http.request import Request
from realestate_scrapy.items import RealestateScrapyItem

class RealEstateSpider(scrapy.Spider):

    name = "realestate"
    start_urls = ['https://www.nekretnine.rs/stambeni-objekti/zemlja/crna-gora/lista/po-stranici/10/stranica/1/' ,
        'https://www.nekretnine.rs/stambeni-objekti/lista/po-stranici/10/stranica/1/',
        'https://www.nekretnine.rs/apartmani/vikendice-i-brvnare/lista/po-stranici/10/stranica/1/',
        'https://www.nekretnine.rs/apartmani/vikendice-i-brvnare/zemlja/crna-gora/lista/po-stranici/10/stranica/1/']
    

    def parse(self, response):

        for offer in response.css('h2.offer-title.text-truncate.w-100 a::attr(href)').extract():
            yield Request(url=response.urljoin(offer), callback=self.parse_type, dont_filter=True)
        next_page = response.css('a.pagination-arrow.arrow-right::attr(href)').get()
        
        if next_page is not None:
            if next_page.find("31") != -1 and next_page.find("srbija") != -1:
                next_page = '/stambeni-objekti/srbija/lista/po-stranici/10/stranica/32/'
                yield response.follow(next_page, callback=self.parse, dont_filter=True)
            elif next_page.find("25") != -1 and next_page.find("crna-gora") != -1:
                next_page = '/stambeni-objekti/srbija/lista/po-stranici/10/stranica/26/'
                yield response.follow(next_page, callback=self.parse, dont_filter=True)
            else:
                yield response.follow(next_page, callback=self.parse, dont_filter=True)

    def parse_type(self, response):
            
        item_loader = ItemLoader(item=RealestateScrapyItem(), response=response)

        #type - vrsta nekretnine - kuca ili stan
        if response.xpath('//a[@class="icon-left"]/@title').extract()[2] == 'Kuće':
            item_loader.add_value('type', 'home')  
            #landArea - povrsina zemljista samo za kuce
            if response.xpath('//li[contains(text(), "Površina zemljišta")]/text()').get() is not None:
                item_loader.add_value('landArea', response.xpath('//li[contains(text(), "Površina zemljišta")]/text()').get().split()[2])
            elif response.css('div.property__main-details ul li:nth-child(5) span::text')[1].get() == '-':
                item_loader.add_value('landArea', None)
            else:
                item_loader.add_value('landArea', response.css('div.property__main-details ul li:nth-child(5) span::text')[1].get())   
        elif response.xpath('//a[@class="icon-left"]/@title').extract()[2] == 'Stanovi':
            item_loader.add_value('type', 'flat')
            #spratnost
            item_loader.add_value('floorInfo', response.css('div.property__main-details ul li:nth-child(5) span::text')[1].get())
        elif response.xpath('//a[@class="icon-left"]/@title').extract()[2] == 'Vikendice i brvnare':
            item_loader.add_value('type', 'cottage')
        else:
            return

        #typeOffer - izdavanje ili prodaja
        if response.css('div.property__amenities li::text').extract_first().find("Izdavanje") != -1:  #li - Transakcija: Prodaja ili Izadvanje
            item_loader.add_value('typeOfOffer', 'rent')
        elif response.css('div.property__amenities li::text').extract_first().find("Prodaja") != -1:
            item_loader.add_value('typeOfOffer', 'sale')

        #city
        item_loader.add_value('city', response.css('div.property__location li:nth-child(3)::text').get()) 

        #municipality
        item_loader.add_value('municipality', response.css('div.property__location li:nth-child(4)::text').get())

        #country
        item_loader.add_value('country', response.css('div.property__location li:nth-child(1)::text').get())

        #squareFootage
        if response.css('div.property__main-details ul li:nth-child(1) span::text')[1].get() is None:
            item_loader.add_value('squareFootage', None)
        elif response.css('div.property__main-details ul li:nth-child(1) span::text')[1].get().split()[0] == '-':
            item_loader.add_value('squareFootage', None)
        else:
            item_loader.add_value('squareFootage', response.css('div.property__main-details ul li:nth-child(1) span::text')[1].get().split()[0])

        #constructionYear
        if response.xpath('//li[contains(text(), "Godina izgradnje")]/text()').get() is not None:
            item_loader.add_value('constructionYear', int(response.xpath('//li[contains(text(), "Godina izgradnje")]/text()').get().split()[2]))

        #registration
        if response.xpath('//li[contains(text(), "Uknjiženo")]/text()').get() is not None:
            item_loader.add_value('registration', response.xpath('//li[contains(text(), "Uknjiženo")]/text()').get().split()[1])

        #heatingType
        if response.css('div.property__main-details ul li:nth-child(3) span::text')[1].get() == '-':
            item_loader.add_value('heatingType', None)
        else:
            item_loader.add_value('heatingType', response.css('div.property__main-details ul li:nth-child(3) span::text')[1].get())

        #roomNo
        if response.css('div.property__main-details ul li:nth-child(2) span::text')[1].get() == '-':
            item_loader.add_value('roomNo', None)
        else:
            item_loader.add_value('roomNo', response.css('div.property__main-details ul li:nth-child(2) span::text')[1].get())

        #bathroomNo
        if response.xpath('//li[contains(text(), "Broj kupatila")]/text()').get() is not None:
            item_loader.add_value('bathroomNo', response.xpath('//li[contains(text(), "Broj kupatila")]/text()').get().split()[2])
        #else:
            #item_loader.add_value('bathroomNo', response.css('div.property__main-details ul li:nth-child(3) span::text')[1].get())

        #price
        if response.css('h4.stickyBox__price::text').get().find("EUR") != -1:
            item_loader.add_value('price', response.css('h4.stickyBox__price::text').get().replace('EUR', '').replace(' ', ''))   
        else:
            item_loader.add_value('price', None)

        #condition - novogradnja ili starogradnja
        if response.xpath('//li[contains(text(), "Stanje nekretnine")]/text()').get() is not None:
           item_loader.add_value('con', response.xpath('//li[contains(text(), "Stanje nekretnine")]/text()').get().split()[2])

        #pool
        details = response.css('div.property__amenities ul li::text').extract()
        if 'Bazen' in details:
            item_loader.add_value('pl', 'yes')

        #pumpaIliKalorimetri
        opis = response.css('div.cms-content-inner').get()
        if 'toplotna pumpa' in opis:
            item_loader.add_value('pumpaIliKalorimetri', 'pumpa')
        elif 'kalorimetri' in opis:
            item_loader.add_value('pumpaIliKalorimetri', 'kalorimetri')

        return item_loader.load_item()
 

#scrapy shell -s USER_AGENT="Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 https://www.nekretnine.rs/stambeni-objekti/lista/po-stranici/10/stranica/3/
#re Safari/537.36"sponse.xpath('//a[contains(@href, "stanovi")]/@href').get()
#godina izgradnje https://www.nekretnine.rs/stambeni-objekti/stanovi/hotel-jugoslavija-dvosoban-id1216/NkPTQk1_Q8M/
#scrapy shell -s USER_AGENT="Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36" https://www.nekretnine.rs/stambeni-objekti/kuce/50-olimp-kninska-131m2-15-ari-kninska/NkDpcIKlDDY/