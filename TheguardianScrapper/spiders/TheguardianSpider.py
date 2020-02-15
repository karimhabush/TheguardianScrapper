import scrapy
from TheguardianScrapper.items import ArticleItem

class TheguardianSpider(scrapy.Spider):
	name = "theguardian"
	start_urls = ['https://www.theguardian.com/world/all']

	def parse(self,response):
		ARTICLE_URL_SELECTOR = '//*[contains(@class,"fc-item__link")]//@href'
		for article_url in response.xpath(ARTICLE_URL_SELECTOR).extract():
			yield scrapy.Request(
				url = article_url,
				callback=self.parsearticle
			)

		NEXT_PAGE_SELECTOR = '//*[contains(@class,"pagination__action--static") and contains(@rel,"next")]//@href'
		next_page = response.xpath(NEXT_PAGE_SELECTOR).extract_first()
		if(next_page):
			yield scrapy.Request(
				response.urljoin(next_page),
                callback=self.parse
				)

	def parsearticle(self,response):
		# Test if the article is already crawled
		if('cached' in response.flags):
			return

		HEADLINE_SELECTOR = '//*[contains(@itemprop,"headline")]//text()'
		CONTENT_SELECTOR = '//*[contains(@class,"content__article-body")]//p//text()'
		STANDFIRST_SELECTOR = '//*[contains(@class,"content__standfirst")]//p//text()'
		AUTHOR_SELECTOR = '//*[contains(@rel,"author")]//*/text()'
		LABEL_SELECTOR = '//*[contains(@class,"label__link-wrapper")]//text()'
		PUBLISHEDAT_SELECTOR = '//*[contains(@class,"content__dateline-wpd")]//@datetime'

		item = ArticleItem()

		item['author'] = response.xpath(AUTHOR_SELECTOR).extract()
		item['headline']= response.xpath(HEADLINE_SELECTOR).extract_first()
		item['content' ]= ''.join(response.xpath(CONTENT_SELECTOR).extract())
		item['standfirst' ]= ''.join(response.xpath(STANDFIRST_SELECTOR).extract())
		item['label' ]= response.xpath(LABEL_SELECTOR).extract()
		item['url']=  response.request.url
		item['published_at'] = response.xpath(PUBLISHEDAT_SELECTOR).extract_first()

		yield item