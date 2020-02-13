import scrapy

class TheguardianSpider(scrapy.Spider):
	name = "theguardian"
	start_urls = ['https://www.theguardian.com/world/all']

	def parse(self,response):
		SET_SELECTOR='//*[contains(@class,"fc-item__container")]'
		
		for article in response.xpath(SET_SELECTOR):
			ARTICLE_URL_SELECTOR = '//*[contains(@class,"fc-item__link")]//@href'
			article_url = article.xpath(ARTICLE_URL_SELECTOR).extract_first()
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
		HEADLINE_SELECTOR = '//*[contains(@itemprop,"headline")]//text()'
		CONTENT_SELECTOR = '//*[contains(@class,"content__article-body")]//p//text()'
		STANDFIRST_SELECTOR = '//*[contains(@class,"content__standfirst")]//p//text()'
		AUTHOR_SELECTOR = '//*[contains(@rel,"author")]//*/text()'
		LABEL_SELECTOR = '//*[contains(@class,"label__link-wrapper")]//text()'
		yield {
			'author' : response.xpath(AUTHOR_SELECTOR).extract(),
			'headline' : response.xpath(HEADLINE_SELECTOR).extract_first(),
			'content' : ''.join(response.xpath(CONTENT_SELECTOR).extract()),
			'standfirst' : ''.join(response.xpath(STANDFIRST_SELECTOR).extract()),
			'label' : response.xpath(LABEL_SELECTOR).extract(),
			'url' : response.request.url
		}