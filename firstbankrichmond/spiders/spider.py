import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import FfirstbankrichmondItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class FfirstbankrichmondSpider(scrapy.Spider):
	name = 'firstbankrichmond'
	start_urls = ['https://www.firstbankrichmond.com/press-releases']

	def parse(self, response):
		post_links = response.xpath('//a[@class="more-link"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@class="next-posts-link"]/@href').get()
		if next_page:
			yield response.follow(next_page, self.parse)

	def parse_post(self, response):
		date = ' '.join(response.xpath('//div[@class="post-date"]/text()').get().split()[1:])
		title = response.xpath('//span[@id="hs_cos_wrapper_name"]/text()').get()
		content = response.xpath('(//div[@class="column"])[1]//text() | //span[@id="hs_cos_wrapper_post_body"]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=FfirstbankrichmondItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
