#encoding: utf-8
import scrapy
from tutorial.items import DmozItem
from scrapy.http import FormRequest
from scrapy.http import Request

'''
#class1，爬网页信息，并自动生成文件保存
class DmozSpider(scrapy.Spider):
    name = 'dmoz'
    allowed_domains = ['dmoz.org']
    start_urls = [
        "https://www.douban.com/note/625255572/",
        "https://www.douban.com/note/623471280/"
    ]

    def parse(self, response):
        #把url以/为分界线分割开来，取倒数第二个块
        filename = response.url.split('/')[-2]
        #把url的响应体保存进以filename为标题的文件中，设置文件的读写权限为wb，即可写
        with open(filename, 'wb') as f:
            f.write(response.body)

#class2，爬网页里的字段信息，并输出json
class DmozSpider(scrapy.Spider):
    name = 'dmoz'
    allowed_domains = ['www.douban.com']
    start_urls = [
        "https://www.douban.com/note/625255572/",
        "https://www.douban.com/note/694188623/"
    ]
    def parse(self, response):
        for sel in response.xpath('//*[@id="content"]/div/div[1]/div[2]/div[1]'):
            item = DmozItem()
            item['title'] = sel.xpath('string(h1)').extract()
            item['auther'] = sel.xpath('string(div/a[2])').extract()
            item['date'] = sel.xpath('string(div/span)').extract()
            
            yield item

#class3，二手房
class DmozSpider(scrapy.Spider):
    name = 'dmoz'
    allowed_domains = ['dmoz.org']
    start_urls = [
        "https://cn.58.com/chuzu/"
    ]
    def parse(self, response):
        for sel in response.xpath('/html/body/div[5]/div/div[5]/div[2]/ul/li[2]/div[2]'):
            item = DmozItem()
            item['title'] = sel.xpath('h2/a').extract()
            yield item



class DmozSpider(scrapy.Spider):
    name = 'dmoz'
    allowed_domains = ['www.tmsf.com']
    start_urls = [
        "http://www.tmsf.com/esfn/EsfnSearch_csnew.jspx"
    ]
    def parse(self, response):
        for sel in response.xpath('/html/body/div[4]/div[2]/div[2]/div/ul/li[1]/div/div[2]'):
            item = DmozItem()
            item['title'] = sel.xpath('h5/a/text()').extract()
            yield item


'''


class tmsf(scrapy.Spider):
    name = 'dmoz'
    allowed_domains = ['www.tmsf.com']
    start_urls = [
        "http://www.tmsf.com/esf/esfnSearch_csnew.htm"
    ]


    def __init__(self):
        self.area = str(330102)
        #str(input("请输入编码："))

    def start_requests(self):
        '''
        btn = response.css('div#myTop1 ul li::attr(onclick)').extract()[1]
        btn = btn.split('\'')[-2]
        self.main_url = "http://www.tmsf.com" + btn
        '''
        yield scrapy.FormRequest(url = "http://www.tmsf.com/esfn/EsfnSearch_csnew.jspx",
                            method = 'POST',
                            headers = {"Referer":"http://www.tmsf.com/index.jsp","User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"},
                            cookies = {"Hm_lvt_bbb8b9db5fbc7576fd868d7931c80ee1":"1541766400","gr_user_id":"9a954ad8-baf3-4cc2-8636-7efeb7f35019","grwng_uid":"d365666b-5653-4402-badd-6c414de10685","BSFIT_EXPIRATION":"1541829407937","BSFIT_DEVICEID":"LMpC4nBCTw0Z9n0_L-yNRlUk2g06fCOb_OOL8Ii9m9Br3C8AvUKNt47JLvHbwEXrrIyhTj9TI4MWBJ6hAn2Yac70IXpeOft5SHaYsPqVLQMmGfJdLKec2hivLqwHsUsYcVWpFTWO0d_NO2FLN9nrVb1YjlqWm_G1","b61f24991053b634_gr_session_id":"4ebe5c8f-9cef-4053-986c-84351f216891","b61f24991053b634_gr_session_id_4ebe5c8f-9cef-4053-986c-84351f216891":"true","JSESSIONID":"21C798A09E3CC163523841A49E57E5BA","Hm_lpvt_bbb8b9db5fbc7576fd868d7931c80ee1":"1541769077","BSFIT_8topm":"DL40DLZ2uLDwJjZ2uP,Dp8wDp8wJzmdDP,Dp8TJpDwJzFduP"},
                            formdata = {
                            'aid': self.area
                            })

    def is_spachial(self, n):
        if n == "|":
            return False
        elif n == "[":
            return False
        elif n == "]":
            return False
        elif n == "-":
            return False
        else:
            return True

    def parse(self, response):
        for sel in response.css('div.houseBox2'):
            item = DmozItem()
            item['title'] = sel.css('div.house_listinfo h5 a::attr(title)').extract()
            item['price'] = sel.css('div.house_price_total strong::text').extract()
            item['price'] = [int(i) for i in item['price']]
            item['info'] = sel.css('div.house_listinfo_line span::text').extract()
            item['info'] = list(filter(self.is_spachial, item['info']))
            item['area'] = sel.css('div.house_listinfo_line span a::text').extract()
            item['time'] = sel.css('div.house_listinfo div.line24::text').extract()
            item['unitPrice'] = sel.css('div.house_price_unit::text').extract()
            yield item

        page = response.css('span.nlc_totalpage input::attr(value)').extract()[0]
        page = int(page)
        if page < 2:
            next_page = page+1

        nextPage = FormRequest(url = 'http://www.tmsf.com/esfn/EsfnSearch_csnew.jspx',
                            method = 'POST',
                            headers = {"Referer":"http://www.tmsf.com/index.jsp","User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"},
                            cookies = {"Hm_lvt_bbb8b9db5fbc7576fd868d7931c80ee1":"1541766400","gr_user_id":"9a954ad8-baf3-4cc2-8636-7efeb7f35019","grwng_uid":"d365666b-5653-4402-badd-6c414de10685","BSFIT_EXPIRATION":"1541829407937","BSFIT_DEVICEID":"LMpC4nBCTw0Z9n0_L-yNRlUk2g06fCOb_OOL8Ii9m9Br3C8AvUKNt47JLvHbwEXrrIyhTj9TI4MWBJ6hAn2Yac70IXpeOft5SHaYsPqVLQMmGfJdLKec2hivLqwHsUsYcVWpFTWO0d_NO2FLN9nrVb1YjlqWm_G1","b61f24991053b634_gr_session_id":"4ebe5c8f-9cef-4053-986c-84351f216891","b61f24991053b634_gr_session_id_4ebe5c8f-9cef-4053-986c-84351f216891":"true","JSESSIONID":"21C798A09E3CC163523841A49E57E5BA","Hm_lpvt_bbb8b9db5fbc7576fd868d7931c80ee1":"1541769077","BSFIT_8topm":"DL40DLZ2uLDwJjZ2uP,Dp8wDp8wJzmdDP,Dp8TJpDwJzFduP"},
                            formdata = {
                            'aid': self.area,
                            'page': str(next_page)
                            })
        yield nextPage


class ke(scrapy.Spider):
    name = "dmoz1"
    allowed_domains = ['hz.ke.com']
    start_urls = [
        "https://hz.ke.com/ershoufang/"
    ]


    def __init__(self):
        self.page = 1
        self.area = 'xihu'

    def start_requests(self):
        yield scrapy.FormRequest(url = "https://hz.ke.com/ershoufang/" + self.area)

    def parse(self, response):
        for sel in response.xpath('//*[@id="beike"]/div[4]/div[1]/ul/li/div[1]'):
            item = DmozItem()
            item['title1'] = sel.xpath('div[1]/a/text()').extract()
            item['price1'] = sel.xpath('div[6]/div[1]/span/text()').extract()
            item['price1'] = [int(i) for i in item['price1']]
            item['info1'] = sel.xpath('div[2]/div[1]/text()').extract()
            info1_after = []
            for x in item['info1']:
                index = ' '
                for i in x:
                    if i != "|":
                        index += i
                info1_after.append(index)
            item['info1'] = info1_after
            item['info2'] = sel.xpath('div[3]/div[1]/text()').extract()
            item['area1'] = sel.xpath('div[3]/div[1]/a/text()').extract()
            item['unitPrice1'] = sel.xpath('div[6]/div[2]/span/text()').extract()
            item['name1'] = sel.xpath('div[2]/div[1]/a/text()').extract()
            yield item

        if self.page <2:
            self.page = self.page + 1
            yield response.follow('/ershoufang/' + self.area + '/pg' + str(self.page), callback=self.parse)
